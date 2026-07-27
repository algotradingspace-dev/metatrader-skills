---
name: risk-engine
description: >
  Indestructible risk management for MQL5 EAs. Use for: position sizing (fixed %,
  ATR-based, volatility-scaled, half-Kelly); daily and total drawdown guards;
  equity-stop implementation; configurable prop firm rule sets; consecutive loss
  tracking with auto-risk reduction; correlation-based exposure limits; and any
  "how do I protect the account" question. This module is always Layer 1 — the
  first gate before any trade. Trigger: "position size", "lot size", "drawdown",
  "risk", "prop firm", "daily loss limit", "max DD", "equity stop", "Kelly",
  "correlation risk", "exposure", "account protection", "halt trading".
---

# Risk Engine

The risk engine is the most critical module. All trade execution is gated
through it. If risk fails, everything fails. Never bypass this layer.

---

## Purpose

Defines Layer 1 of the 5-layer EA architecture: capital preservation through
drawdown limits, position sizing, consecutive-loss protection, and configurable
rule-set support for prop firm challenges. Every trade must pass through
`IsTradeAllowed()` before any other layer runs.

---

## When to Use

- Writing or reviewing any EA that manages real positions
- Configuring an EA for a prop firm challenge
- Diagnosing why an EA blew a funded account (usually missing this layer)
- Implementing Kelly or volatility-scaled position sizing
- Looking up order/position/deal property identifiers

**Do NOT use** for:
- Post-entry trade management → use `trade-manager`
- Market regime filtering → use `market-regime`
- Multi-asset correlation books → use `multi-asset`
- EA architecture / module wiring → use `ea-architect`

---

## Core Guidance

### CRiskManager Architecture

The risk manager gates every trade through drawdown checks, halts trading
when limits are breached, and auto-reduces risk after losses or near limits.

```mql5
class CRiskManager : public IModule {
private:
   double   m_riskPercent;
   double   m_maxDailyDD;
   double   m_maxTotalDD;
   double   m_dayStartBalance;
   double   m_peakBalance;
   bool     m_haltTrading;
   bool     m_reducedMode;
   int      m_consecutiveLosses;
   datetime m_lastDayReset;

public:
   CRiskManager(double riskPct, double maxDailyDD, double maxTotalDD) {
      m_riskPercent = riskPct; m_maxDailyDD = maxDailyDD; m_maxTotalDD = maxTotalDD;
      m_dayStartBalance = AccountInfoDouble(ACCOUNT_BALANCE);
      m_peakBalance = m_dayStartBalance;
      m_haltTrading = false; m_reducedMode = false;
      m_consecutiveLosses = 0; m_lastDayReset = TimeCurrent();
   }
   bool   IsReady()   { return true; }
   void   Reset()     { DailyReset(); }
   bool   IsHalted()  { return m_haltTrading; }
   bool   IsReduced() { return m_reducedMode; }
   string GetStatus() { /* daily/total DD strings */ }
};
```

### Drawdown Guards

```mql5
void DailyReset() {
   MqlDateTime now, last;
   TimeToStruct(TimeCurrent(), now);
   TimeToStruct(m_lastDayReset, last);
   if(now.day != last.day) {
      m_dayStartBalance = AccountInfoDouble(ACCOUNT_BALANCE);
      m_haltTrading = false; m_reducedMode = false;
      m_consecutiveLosses = 0;
      m_lastDayReset = TimeCurrent();
   }
}

bool IsTradeAllowed() {
   DailyReset();
   if(m_haltTrading) return false;
   double balance = AccountInfoDouble(ACCOUNT_BALANCE);
   double equity  = AccountInfoDouble(ACCOUNT_EQUITY);
   if(balance > m_peakBalance) m_peakBalance = balance;
   double dailyDD = (m_dayStartBalance - equity) / m_dayStartBalance * 100.0;
   if(dailyDD >= m_maxDailyDD) {
      m_haltTrading = true;
      Alert("DAILY DD LIMIT HIT — trading halted. DD: ", DoubleToString(dailyDD, 2), "%");
      return false;
   }
   m_reducedMode = (dailyDD >= m_maxDailyDD * 0.6);
   double totalDD = (m_peakBalance - equity) / m_peakBalance * 100.0;
   if(totalDD >= m_maxTotalDD) {
      m_haltTrading = true;
      Alert("TOTAL DD LIMIT HIT — trading halted. DD: ", DoubleToString(totalDD, 2), "%");
      return false;
   }
   return true;
}
```

### Prop Firm Rule Set (Configurable Struct)

Prop firm rules use a generic struct loaded from configuration. Concrete
presets live in `references/prop-firm-presets.md`.

```mql5
struct PropFirmRules {
   double daily_dd_limit;
   double total_dd_limit;
   double halt_daily_buffer;   // EA halts this % before the hard limit
   double halt_total_buffer;
   bool   no_weekend_hold;
   bool   news_restricted;
   int    min_trading_days;
};

PropFirmRules LoadDefaultRules() {
   PropFirmRules r = {};
   r.daily_dd_limit    = 5.0;   // set per firm from presets
   r.total_dd_limit    = 10.0;
   r.halt_daily_buffer = 1.0;   // stays below the configured hard limit
   r.halt_total_buffer = 2.0;
   r.no_weekend_hold   = false;
   r.news_restricted   = false;
   r.min_trading_days  = 0;
   return r;
}
```

Use in `IsTradeAllowed()`:
```mql5
if((equity_peak - equity) / equity_peak * 100.0 >= total_dd_limit - halt_total_buffer)
   HaltTrading("Close to total DD limit");
```

### Consecutive Loss Tracking

```mql5
void RecordTradeResult(bool isWin) {
   if(isWin) {
      m_consecutiveLosses = 0;
      if(m_reducedMode && GetDailyDD() < m_maxDailyDD * 0.3)
         m_reducedMode = false;
   } else {
      m_consecutiveLosses++;
      if(m_consecutiveLosses >= 3) m_reducedMode = true;
      if(m_consecutiveLosses >= 6) {
         m_haltTrading = true;
         Alert("6 consecutive losses — halting EA for review.");
      }
   }
}
```

### Correlation-Based Exposure Guard

```mql5
bool IsCorrelatedPositionOpen(string sym1, string sym2, int magic) {
   for(int i = 0; i < PositionsTotal(); i++) {
      if(!PositionGetTicket(i)) continue;
      string s = PositionGetString(POSITION_SYMBOL);
      long   m = PositionGetInteger(POSITION_MAGIC);
      if(m != magic) continue;
      if(s == sym1 || s == sym2) return true;
   }
   return false;
}
```

---

## Code Patterns — Position Sizing

### Method 1: Fixed Percentage Risk (default)

```mql5
double CalculateLotSize(double slDistancePoints) {
   if(slDistancePoints <= 0) return 0;
   double effectiveRisk = m_reducedMode ? m_riskPercent * 0.5 : m_riskPercent;
   double balance    = AccountInfoDouble(ACCOUNT_BALANCE);
   double riskAmount = balance * effectiveRisk / 100.0;
   double tickValue  = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_VALUE);
   double tickSize   = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE);
   double lotStep    = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP);
   double minLot     = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN);
   double maxLot     = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MAX);
   double riskPerLot = slDistancePoints * (tickValue / tickSize);
   if(riskPerLot <= 0) return 0;
   double rawLot  = riskAmount / riskPerLot;
   double lotSize = MathFloor(rawLot / lotStep) * lotStep;
   return MathMax(minLot, MathMin(maxLot, lotSize));
}
```

### Method 2: ATR-Based Dynamic SL

```mql5
double atr = iATR(_Symbol, PERIOD_H1, 14, 1);
double slPoints = atr * 1.5 / _Point;
double lots = CalculateLotSize(slPoints);
```

### Method 3: Volatility-Scaled Risk

```mql5
double currentATR  = iATR(_Symbol, PERIOD_H1, 14, 1);
double historicATR = iATR(_Symbol, PERIOD_H1, 14, 20);
double volRatio    = currentATR / historicATR;
double adjustedRisk = MathMax(0.25, MathMin(m_riskPercent, m_riskPercent / volRatio));
```

### Method 4: Half-Kelly Criterion

```
Kelly% = WinRate - (1 - WinRate) / AvgWin_AvgLoss_Ratio
Half-Kelly = Kelly% / 2
Example: 55% WR, 1.8 RR -> Kelly = 0.55 - (0.45/1.8) = 0.30 -> use 15%
```

---

## Common Mistakes

- **Bypassing risk for "quick" trades** — every trade must pass `IsTradeAllowed()`.
  Skipping it even once defeats the layer.
- **Hardcoding tick value assumptions** — `SYMBOL_TRADE_TICK_VALUE` and
  `SYMBOL_TRADE_TICK_SIZE` differ per symbol. Read at runtime.
- **Using `ACCOUNT_BALANCE` for intraday DD** — balance only changes on settled
  trades; use equity for true intraday drawdown.
- **Full Kelly instead of half-Kelly** — full Kelly is too aggressive for
  sequential trading; half-Kelly preserves capital during drawdowns.
- **Not resetting daily limits after a new trading day** — `DailyReset()` must
  run on the first tick of each new day or the DD accumulator holds stale values.

---

## References

| File | Contents | Read when |
|------|----------|-----------|
| `references/live-execution-safety.md` | Bridge-agnostic governance rules for live trading: per-action confirmation, demo-first, no credential harvesting, no mass action, surface account identity | Governing agent-driven or programmatic trade execution on live accounts |
| `references/prop-firm-presets.md` | Concrete daily/total DD limits for common prop firm challenges, weekend/news restrictions, minimum trading days | Setting up EA for a specific prop firm evaluation; verifying current limits |
| `references/order-property-enums.md` | `ENUM_ORDER_PROPERTY_*`, `ENUM_ORDER_TYPE`, `ENUM_ORDER_STATE`, `ENUM_ORDER_TYPE_FILLING`, filling compatibility matrix, `ENUM_ORDER_TYPE_TIME` | Reading/writing order properties; choosing fill policy |
| `references/position-property-enums.md` | `ENUM_POSITION_PROPERTY_*`, `ENUM_POSITION_TYPE`, `ENUM_POSITION_REASON` | Reading open position state; iterating positions |
| `references/deal-property-enums.md` | `ENUM_DEAL_PROPERTY_*`, `ENUM_DEAL_TYPE` (19 values), `ENUM_DEAL_ENTRY`, `ENUM_DEAL_REASON` | Analysing deal history; filtering P&L by deal type |
