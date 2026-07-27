---
name: market-regime
description: >
  Market regime detection and filtering for MQL5 EAs. Use for all logic that
  determines WHETHER to trade: trend vs range classification via ADX; volatility
  regime via ATR (high/normal/reduced); session filtering (London/NY/Asian
  killzones); news event avoidance; spread spike detection; weekend and holiday
  blocking. This is Layer 2 — signals are never generated without passing through
  regime first. Trigger: "market regime", "trending vs ranging", "session filter",
  "news filter", "volatility filter", "spread filter", "when to trade",
  "ATR regime", "ADX trend strength", "killzone", "dead zone",
  "regime detection", "Layer 2".
---

# Market Regime

The regime filter decides WHETHER to trade. Signals decide WHAT to trade.
Never generate signals without first passing the regime gate.

**See also:** For post-hoc regime analysis in Python/pandas (rolling ATR,
trend-strength metrics, regime classification over historical data), see
the `analytics` skill under `metatrader-research`.

---

## Purpose

Defines Layer 2 of the 5-layer EA architecture: classifying the current market
state (trending bull/bear, ranging, volatile, dead) and gating trade execution
through session, news, spread, and weekend filters. Every signal from Layer 3
must be passed a regime context.

---

## When to Use

- Building the Layer 2 RegimeFilter module for any EA
- Deciding if a particular time/condition should allow trading
- Diagnosing why an EA trades during illiquid or high-spread periods
- Configuring session-specific strategies (London open, NY overlap, etc.)
- Reading tick/bar data structures or querying DOM depth

**Do NOT use** for:
- Entry signal generation -> use `signal-engine`
- Risk/sizing policy -> use `risk-engine`
- EA architecture / module wiring -> use `ea-architect`

---

## Core Guidance

### Regime Classification Enum

All modules share this enum. Define it in `CoreEngine.mqh`.

```mql5
enum ENUM_REGIME {
   REGIME_UNDEFINED = 0,
   REGIME_TRENDING_BULL,
   REGIME_TRENDING_BEAR,
   REGIME_RANGING,
   REGIME_VOLATILE,
   REGIME_DEAD,
};
```

**Regime-to-signal mapping:**

| Regime | Use | Skip |
|--------|-----|------|
| TRENDING_BULL | OB pullback longs, EMA bounce | Mean reversion shorts |
| TRENDING_BEAR | FVG fill shorts, breakdown entries | Mean reversion longs |
| RANGING | BBand bounce, RSI extremes, range boundaries | Breakout signals |
| VOLATILE | Reduce lot 50%, widen SL 50% | Tight scalping signals |
| DEAD | -- | Everything |
| UNDEFINED | -- | Everything, wait for clarity |

### CRegimeFilter — ADX/ATR Detection

```mql5
class CRegimeFilter : public IModule {
private:
   int    m_adxPeriod;
   double m_adxTrendThreshold;
   double m_adxRangeThreshold;
   int    m_atrPeriod;
   double m_volatilityMultiplier;

public:
   CRegimeFilter(int adxPeriod=14, double trendTH=25.0, double rangeTH=20.0,
                 int atrPeriod=14, double volMult=2.0) { ... }

   ENUM_REGIME GetCurrentRegime() {
      if(IsDeadZone())       return REGIME_DEAD;
      if(IsHighVolatility()) return REGIME_VOLATILE;
      double adx=GetADX(PERIOD_H4), plusDI=GetPlusDI(PERIOD_H4), minusDI=GetMinusDI(PERIOD_H4);
      if(adx>=m_adxTrendThreshold) {
         if(plusDI>minusDI) return REGIME_TRENDING_BULL;
         if(minusDI>plusDI) return REGIME_TRENDING_BEAR;
      }
      if(adx<m_adxRangeThreshold) return REGIME_RANGING;
      return REGIME_UNDEFINED;
   }

   bool IsDeadZone() {
      MqlDateTime t; TimeToStruct(TimeGMT(), t);
      return (t.hour>=21||t.hour<1); // 21:00-01:00 UTC thin liquidity
   }

   bool IsHighVolatility() {
      double current=iATR(_Symbol,PERIOD_H1,m_atrPeriod,1);
      double avg=0;
      for(int i=1;i<=20;i++) avg+=iATR(_Symbol,PERIOD_H1,m_atrPeriod,i);
      avg/=20.0;
      return (current>avg*m_volatilityMultiplier);
   }

   bool   IsReady(){return true;}
   void   Reset(){}
   string GetStatus(){return "Regime: "+EnumToString(GetCurrentRegime());}
};
```

### Session Filter — London, NY, Asian Killzones

```mql5
class CSessionFilter {
private:
   int  m_gmtOffset;
   bool m_london, m_ny, m_asian;
public:
   CSessionFilter(int gmtOffset, bool london=true, bool ny=true, bool asian=false) { ... }

   bool IsActiveSession() {
      if(IsWeekend())         return false;
      if(IsPreWeekendClose()) return false;
      MqlDateTime t; TimeToStruct(TimeGMT(), t);
      int h=t.hour;
      if(m_london&&h>=7&&h<9)    return true;  // London killzone
      if(m_ny    &&h>=12&&h<16)  return true;  // London-NY overlap
      if(m_ny    &&h>=19&&h<21)  return true;  // NY close hunt
      if(m_asian &&h>=0&&h<2)    return true;  // Asian killzone
      return false;
   }
   bool IsWeekend(){MqlDateTime t;TimeToStruct(TimeGMT(),t);return(t.day_of_week==0||t.day_of_week==6);}
   bool IsPreWeekendClose(){MqlDateTime t;TimeToStruct(TimeGMT(),t);return(t.day_of_week==5&&t.hour>=20);}
};
```

### Spread Monitor and News Filter

```mql5
bool IsSpreadAcceptable(double maxSpreadPoints) {
   double spread=(double)SymbolInfoInteger(_Symbol,SYMBOL_SPREAD);
   return(spread<=maxSpreadPoints);
}

class CNewsFilter {
   int m_bufferMinutes;
public:
   CNewsFilter(int bufferMin=30){m_bufferMinutes=bufferMin;}
   bool IsSafeToTrade(){
      MqlDateTime t; TimeToStruct(TimeGMT(),t);
      int h=t.hour, m=t.min;
      // Simplified: avoid 12:20-13:00 UTC on weekdays (catches most USD releases)
      if(t.day_of_week>=1&&t.day_of_week<=5)
         if(h==12&&m>=20)return false;
         if(h==13&&m<10)return false;
      return true;
   }
};
```

### Wiring Regime Into OnTick

```mql5
void OnTick() {
   if(!IsNewBar(PERIOD_M15)) return;
   if(!g_RiskMgr.IsTradeAllowed()) return;       // Layer 1
   if(!g_Session.IsActiveSession())    return;    // Session timing
   if(!g_NewsFilter.IsSafeToTrade())   return;    // News avoidance
   if(!IsSpreadAcceptable(50))         return;    // Spread check
   ENUM_REGIME regime=g_Regime.GetCurrentRegime();
   if(regime==REGIME_DEAD||regime==REGIME_UNDEFINED) return;
   double lotMultiplier=(regime==REGIME_VOLATILE)?0.5:1.0;
   STradeSignal sig=g_Signal.GetSignal(regime);
   if(sig.type==SIGNAL_NONE) return;
   double lots=g_RiskMgr.CalculateLotSize(sig.slDistance)*lotMultiplier;
   g_TradeMgr.OpenTrade(sig,lots);
}
```

---

## References

Market data structures (`MqlTick`, `MqlRates`, `MqlBookInfo`), `ENUM_BOOK_TYPE`,
`ENUM_SERIES_INFO_INTEGER`, `ENUM_TIMEFRAMES`, `ENUM_APPLIED_PRICE`, and
`ENUM_MA_METHOD` are documented in the MQL5 Reference:
- `docs/mql5_com_-_docs/constants-structures-mqltick.md`
- `docs/mql5_com_-_docs/constants-structures-mqlrates.md`
- `docs/mql5_com_-_docs/constants-structures-mqlbookinfo.md`
- `docs/mql5_com_-_docs/constants-tradingconstants-enum_series_info_integer.md`
- `docs/mql5_com_-_docs/constants-chartconstants-enum_timeframes.md`
- `docs/mql5_com_-_docs/constants-indicatorconstants-prices.md`
- `docs/mql5_com_-_docs/constants-indicatorconstants-enum_ma_method.md`

For post-hoc regime analysis in Python, see `analytics` under
`metatrader-research`.
