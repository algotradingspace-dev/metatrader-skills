---
name: signal-engine
description: >
  Entry and exit signal generation for MQL5 EAs. Use for: STradeSignal contract
  design; signal generation flow with confluence scoring (min 2 factors); SMC/ICT
  concepts (Order Blocks, Fair Value Gaps, CHoCH, BoS, liquidity sweeps);
  multi-timeframe analysis; technical indicator handles (ATR, EMA, RSI, ADX, MACD,
  Bollinger); candlestick pattern detection; breakout and mean reversion entries;
  multi-asset signal profiles; MQL5 Signals subscription API. Every signal requires
  minimum 2 confluence factors. Pair with market-regime to gate signals by market
  state. Trigger: "entry logic", "signal", "Order Block", "FVG", "CHoCH", "SMC",
  "ICT", "buy signal", "sell signal", "confluence", "indicator", "pattern",
  "liquidity sweep", "signal engine".
---

# Signal Engine

Signals are hypotheses. Every entry needs minimum 2 confluence factors
to separate edge from noise. Regime context must be passed in from Layer 2.

---

## Purpose

Defines Layer 3 of the 5-layer EA architecture: generating trade signals
from structured market concepts, technical indicators, and confluence
scoring. Signals are consumed by Layer 4 (TradeManager).

---

## When to Use

- Building or replacing Layer 3 (SignalEngine) in any EA
- Translating a trading strategy concept into MQL5 code
- Adding or removing confluence factors from an existing signal
- Wiring built-in or custom indicators into a signal engine
- Looking up indicator handle signatures and buffer maps
- Using the series copy API (`CopyRates`, `CopyTicks`, `CopyBuffer`)
- Reading or writing MQL5 Signals subscription properties

**Do NOT use** for:
- Post-entry trade management → use `trade-manager`
- Market regime classification → use `market-regime`
- EA architecture / module wiring → use `ea-architect`

---

## Core Guidance

### STradeSignal Contract

The struct is the contract between SignalEngine (Layer 3) and TradeManager (Layer 4).

```mql5
enum SIGNAL_TYPE { SIGNAL_NONE = 0, SIGNAL_BUY, SIGNAL_SELL };

struct STradeSignal {
   SIGNAL_TYPE   type;             // BUY / SELL / NONE
   double        entryPrice;       // Market or limit entry price
   double        stopLoss;         // Absolute SL price
   double        takeProfit;       // Absolute TP price
   double        slDistance;       // SL distance in points (for lot sizing)
   double        rrRatio;          // Calculated R:R ratio
   int           confluenceScore;  // Count of confirming factors (min 2)
   string        reason;           // Log string e.g. "OB+FVG+Session+HTFBias"
   datetime      signalTime;       // Bar open time when signal fired
};

STradeSignal NoSignal() {
   STradeSignal s;
   s.type = SIGNAL_NONE; s.confluenceScore = 0;
   return s;
}
```

### Signal Generation Flow (7-Step)

Every signal function follows this sequence. Return `NoSignal()` at any failed check.

```
1. HTF Bias Check      H4/D1 direction — defines trade bias
2. Liquidity Sweep     BSL or SSL taken on entry timeframe
3. CHoCH Confirmed     Structure shift on M15 confirms reversal
4. OB/FVG Found        Entry zone identified within structure
5. Session Active      Killzone timing verified (from regime layer)
6. Confluence Score    >= 2 = valid signal; <2 = return SIGNAL_NONE
7. Build STradeSignal  Set entry, SL, TP, slDistance, rrRatio, reason
```

### Confluence Scoring

```mql5
if(htfAligned)       confluenceScore += 2;  // HTF alignment = double weight
if(liquiditySwept)   confluenceScore++;
if(chochConfirmed)   confluenceScore++;
if(inFVG)            confluenceScore++;
if(inOrderBlock)     confluenceScore++;
if(sessionActive)    confluenceScore++;
if(indicatorAligned) confluenceScore++;
// Scalp/M15:  2 points minimum
// Swing/H1+:  3 points minimum
```

### CHoCH Detection

```mql5
bool DetectCHoCH(ENUM_TIMEFRAMES tf, int expectedDirection) {
   double swingHighs[], swingLows[];
   ArrayResize(swingHighs, 10); ArrayResize(swingLows, 10);
   int hIdx = 0, lIdx = 0;
   for(int i = 2; i < 50 && (hIdx < 3 || lIdx < 3); i++) {
      double hi = iHigh(_Symbol, tf, i);
      double lo = iLow(_Symbol, tf, i);
      bool isSwingHigh = (hi > iHigh(_Symbol, tf, i-1) && hi > iHigh(_Symbol, tf, i+1));
      bool isSwingLow  = (lo < iLow(_Symbol, tf, i-1) && lo < iLow(_Symbol, tf, i+1));
      if(isSwingHigh && hIdx < 10) swingHighs[hIdx++] = hi;
      if(isSwingLow  && lIdx < 10) swingLows[lIdx++]  = lo;
   }
   if(expectedDirection == MODE_BULLISH && hIdx >= 2)
      return (swingHighs[0] > swingHighs[1]);
   if(expectedDirection == MODE_BEARISH && lIdx >= 2)
      return (swingLows[0] < swingLows[1]);
   return false;
}
```

### FVG Detection

```mql5
struct SFairValueGap {
   bool   isValid; double high; double low; double mid; int barIndex;
};

SFairValueGap FindFVG(ENUM_TIMEFRAMES tf, int direction, int lookback) {
   SFairValueGap fvg; fvg.isValid = false;
   for(int i = 1; i < lookback; i++) {
      double c1_high = iHigh(_Symbol, tf, i+1);
      double c1_low  = iLow(_Symbol, tf, i+1);
      double c3_high = iHigh(_Symbol, tf, i-1);
      double c3_low  = iLow(_Symbol, tf, i-1);
      if(direction == FVG_BULLISH) {
         if(c3_low > c1_high) {
            fvg.isValid = true; fvg.low = c1_high; fvg.high = c3_low;
            fvg.mid = (fvg.high + fvg.low) / 2.0; fvg.barIndex = i; return fvg;
         }
      } else {
         if(c3_high < c1_low) {
            fvg.isValid = true; fvg.high = c1_low; fvg.low = c3_high;
            fvg.mid = (fvg.high + fvg.low) / 2.0; fvg.barIndex = i; return fvg;
         }
      }
   }
   return fvg;
}
```

---

## Code Patterns

### Gold London Open SMC

```mql5
STradeSignal CSignalEngine::GetGoldLondonSignal() {
   STradeSignal sig = NoSignal();
   double h4_ema50 = iMA(_Symbol, PERIOD_H4, 50, 0, MODE_EMA, PRICE_CLOSE, 1);
   double h4_close = iClose(_Symbol, PERIOD_H4, 1);
   bool htfBullish = (h4_close > h4_ema50);
   bool htfBearish = (h4_close < h4_ema50);
   if(htfBullish || htfBearish) sig.confluenceScore += 2;
   double asianHigh = GetAsianRangeHigh();
   double asianLow  = GetAsianRangeLow();
   double m15_high = iHigh(_Symbol, PERIOD_M15, 1);
   double m15_low  = iLow(_Symbol, PERIOD_M15, 1);
   bool bslSwept   = (m15_high > asianHigh);
   bool sslSwept   = (m15_low  < asianLow);
   if(!bslSwept && !sslSwept) return NoSignal();
   sig.confluenceScore++;
   int expectedDir  = bslSwept ? MODE_BEARISH : MODE_BULLISH;
   bool choch = DetectCHoCH(PERIOD_M15, expectedDir);
   if(!choch) return NoSignal();
   sig.confluenceScore++;
   int fvgDir  = bslSwept ? FVG_BEARISH : FVG_BULLISH;
   SFairValueGap fvg = FindFVG(PERIOD_M15, fvgDir, 5);
   if(!fvg.isValid) return NoSignal();
   sig.confluenceScore++;
   if(sig.confluenceScore < 3) return NoSignal();
   double atr = iATR(_Symbol, PERIOD_H1, 14, 1);
   if(bslSwept && htfBearish) {
      sig.type = SIGNAL_SELL; sig.entryPrice = fvg.mid;
      sig.stopLoss = fvg.high + atr * 0.3; sig.takeProfit = fvg.high - atr * 3.0;
   } else if(sslSwept && htfBullish) {
      sig.type = SIGNAL_BUY; sig.entryPrice = fvg.mid;
      sig.stopLoss = fvg.low - atr * 0.3; sig.takeProfit = fvg.low + atr * 3.0;
   } else return NoSignal();
   sig.slDistance = MathAbs(sig.entryPrice - sig.stopLoss) / _Point;
   sig.rrRatio = MathAbs(sig.takeProfit - sig.entryPrice) / MathAbs(sig.stopLoss - sig.entryPrice);
   sig.reason = "LiqSweep+CHoCH+FVG+HTFBias";
   sig.signalTime = TimeCurrent();
   return sig;
}
```

### EMA Pullback Continuation

```mql5
STradeSignal GetEMAPullbackSignal(ENUM_REGIME regime) {
   STradeSignal sig = NoSignal();
   if(regime != REGIME_TRENDING_BULL && regime != REGIME_TRENDING_BEAR) return sig;
   double ema21 = iMA(_Symbol, PERIOD_H1, 21, 0, MODE_EMA, PRICE_CLOSE, 1);
   double close = iClose(_Symbol, PERIOD_H1, 1);
   double atr   = iATR(_Symbol, PERIOD_H1, 14, 1);
   if(regime == REGIME_TRENDING_BULL && close > ema21
   && iLow(_Symbol, PERIOD_H1, 1) <= ema21 + atr * 0.2) {
      sig.type = SIGNAL_BUY; sig.entryPrice = close;
      sig.stopLoss = ema21 - atr * 1.0; sig.takeProfit = close + atr * 2.5;
      sig.confluenceScore = 3; sig.reason = "EMA21Pullback+HTFTrend";
   }
   sig.slDistance = MathAbs(sig.entryPrice - sig.stopLoss) / _Point;
   sig.signalTime = TimeCurrent();
   return sig;
}
```

---

## Common Mistakes

- **Reading the current bar instead of the last closed bar** — `start_pos=0` is
  the current forming bar. For stable signals, copy 2+ values and read `[1]`.
- **Skipping `INVALID_HANDLE` guard** — always check handle creation and
  `BarsCalculated()` before `CopyBuffer()`.
- **Forgetting `ArraySetAsSeries()` after `CopyBuffer()`** — copied arrays are
  stored oldest-first; timeseries indexing requires `ArraySetAsSeries(array, true)`.
- **Assuming 1:1 bar count between indicator and price** — compare
  `BarsCalculated(handle)` against `rates_total` before assuming alignment.
- **Not calling `HistorySelect()` before reading deal data in `OnTradeTransaction`**.
- **Confusing `CopyTicks` direction with `CopyRates` direction** — ticks are
  oldest-to-newest (index 0 = oldest), rates are newest-first after
  `ArraySetAsSeries`.
- **Copying only 1 element for crossover detection** — need at least 3
  (current, previous closed, and the bar before) to detect a fresh cross.

---

## References

| File | Contents | Read when |
|------|----------|-----------|
| `references/multi-asset-profiles.md` | Per-asset strategy table (XAUUSD, GBPUSD, EURUSD, US500, XAGUSD, BTCUSD) | Tuning signals for a specific instrument or market type |
| `references/signals-marketplace-enums.md` | `ENUM_SIGNAL_BASE_*` and `ENUM_SIGNAL_INFO_*` property tables | Reading MQL5 Signals marketplace subscription properties |
| `references/indicator-constants.md` | `ENUM_INDICATOR`, draw types (`DRAW_LINE`...`DRAW_COLOR_CANDLES`), `ENUM_INDEXBUFFER_TYPE`, buffer line constants | Looking up `IndicatorCreate` types or plot configuration |
| `references/timeseries-copy-api.md` | `CopyRates`, `CopyOpen/High/Low/Close/Time`, `CopyTicks`, `CopyTicksRange`, indexing rules, history gotchas | Copying price/tick data; understanding timeseries direction |
| `references/indicator-lifecycle.md` | Handle creation/validation/release, `BarsCalculated`, `CopyBuffer`, `prev_calculated` delta-copy pattern, CopyBuffer rules | Wiring indicator handles; fixing stale buffer or misaligned signal bugs |
| `references/indicators-trend.md` | `iMA`, `iBands`, `iATR`, `iADX`, `iIchimoku`, `iSAR`, `iEnvelopes`, adaptive MA variants — signatures and buffer maps | Trend-following or volatility-based signal components |
| `references/indicators-oscillators.md` | `iRSI`, `iMACD`, `iStochastic`, `iCCI`, `iMomentum`, `iRVI`, `iOsMA`, `iBullsPower`, `iBearsPower` — signatures and buffer maps | Oscillator-based divergence, crossover, or threshold signals |
| `references/indicators-volume.md` | `iAD`, `iMFI`, `iOBV`, `iChaikin`, `iForce`, `iVolumes` — signatures and buffer maps | Volume/money-flow confirmation signals |
| `references/indicators-bill-williams.md` | `iAlligator`, `iFractals`, `iGator`, `iAO`, `iAC`, `iBWMFI`, `iCustom` — signatures, buffer maps, shift rules | Bill Williams system or custom indicator integration |
| `references/trade-signals-api.md` | `SignalBaseTotal`, `SignalBaseSelect`, `SignalBaseGetDouble`/`Integer`/`String`, `SignalInfoGetDouble`/`Integer`/`String`, `SignalInfoSetDouble`/`Integer`, `SignalSubscribe/Unsubscribe` | Programmatic signal subscription management |
