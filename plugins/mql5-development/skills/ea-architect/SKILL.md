---
name: ea-architect
description: >
  Master MQL5 Expert Advisor architecture reference. Use for: wiring the 5-layer
  EA model (risk, regime, signal, trade mgmt, analytics); writing OnInit/OnTick/OnDeinit
  event handlers; setting up IsNewBar gating; designing include file layouts and .mqh
  module interfaces; applying naming conventions across all EA files; reading symbol
  properties in a broker-agnostic way; and integrating CExpert/CExpertSignal/CExpertMoney
  standard-library classes. Trigger: "5-layer architecture", "module wiring", "OnInit",
  "OnTick", "IsNewBar", "include files", "mqh", "CExpert", "event handlers",
  "EA template", "naming conventions", "broker-agnostic", "symbol data access".
---

# EA Architect

Architecture determines destiny. Every EA skill in this suite plugs into this
5-layer model. Read this first before writing any module.

---

## Purpose

Defines the canonical EA structure — the 5-layer module stack, file layout,
event handler wiring, naming conventions, broker-agnostic symbol access,
and standard-library integration contract. Other skills (risk-engine,
signal-engine, market-regime, trade-manager) implement individual layers.

---

## When to Use

- Starting any new EA from scratch
- Deciding how to split strategy logic into modules
- Adding a new layer or module to an existing EA
- Reviewing whether an EA follows the correct architectural pattern
- Debugging incorrect lot sizing caused by hardcoded tick values
- Implementing `OnTradeTransaction` to react to deal/order events
- Implementing `OnChartEvent` for custom dashboard or button interactions

**Do NOT use** for:
- Specific risk/sizing logic → use `risk-engine`
- Entry signal or pattern detection → use `signal-engine`
- Market regime classification → use `market-regime`
- Post-entry trade management → use `trade-manager`
- ENUM_* constant tables → use `constants`

---

## Core Guidance

### Five-Layer Architecture

Every EA follows a strict 5-layer model. Each layer communicates only with
adjacent layers.

```
Layer 5: ANALYTICS & JOURNAL     logging, metrics, performance review
Layer 4: TRADE MANAGEMENT        trailing SL, breakeven, partial close
Layer 3: SIGNAL ENGINE           entry/exit conditions, confluence
Layer 2: MARKET REGIME FILTER    trend/range/dead/volatile classification
Layer 1: RISK ENGINE             position sizing, daily/total DD gates
Layer 0: CORE ARCHITECTURE       wiring, event handlers, module lifecycle
```

**Data flow on each tick:**
1. RiskEngine checks if trading is allowed (DD gates)
2. RegimeFilter classifies market state
3. SignalEngine evaluates entry conditions only if regime permits
4. TradeManager handles post-entry management
5. Analytics logs all activity

This separation means you can swap any layer without touching others.

### File and Folder Layout

```
EA_Name/
├── EA_Name.mq5              # OnInit/OnTick/OnDeinit only
├── include/
│   ├── CoreEngine.mqh       # IModule base interface
│   ├── RiskManager.mqh      # Layer 1
│   ├── RegimeFilter.mqh     # Layer 2
│   ├── SignalEngine.mqh     # Layer 3
│   ├── TradeManager.mqh     # Layer 4
│   ├── SessionFilter.mqh    # Session & news timing
│   ├── SymbolConfig.mqh     # Per-symbol parameters
│   ├── Analytics.mqh        # Layer 5
│   └── Utilities.mqh        # Shared helpers
├── backtest/                # Archived backtest results
├── docs/
│   └── strategy_spec.md     # Strategy documentation
└── CLAUDE.md                # Agent project context
```

**Rules:**
- The `.mq5` main file contains only event handlers and module wiring
- All logic lives inside `.mqh` include files
- No module accesses another module except through the main file or the layer directly below it

### Naming Conventions

```
Classes        PascalCase + C prefix    CRiskManager, CSignalEngine
Interfaces     PascalCase + I prefix    IModule, ISignalProvider
Enums          UPPER_SNAKE              ENUM_REGIME, SIGNAL_TYPE
Structs        PascalCase + S prefix    STradeSignal, SBarData
Global vars    g_ prefix                g_RiskMgr, g_Signal
Input params   Inp prefix               InpRiskPercent, InpMagicNumber
Local vars     camelCase                currentPrice, lotSize
Constants      ALL_CAPS                 MAX_SLIPPAGE, MIN_LOT
Functions      PascalCase               CalculateLotSize(), IsNewBar()
```

Input groups use `===` delimiters. Input comments always include the unit.

### IModule Interface

Every module must implement this interface. The main file uses `IsReady()`
to abort `OnInit()` if any module fails to initialize.

```mql5
// CoreEngine.mqh
class IModule {
public:
   virtual bool   IsReady()   = 0;
   virtual void   Reset()     = 0;
   virtual string GetStatus() = 0;
};
```

### IsNewBar Gating

Almost all EA logic should run once per bar, not on every tick.

```mql5
bool IsNewBar(ENUM_TIMEFRAMES tf = PERIOD_CURRENT) {
   static datetime lastBarTime = 0;
   datetime currentBarTime = iTime(_Symbol, tf, 0);
   if(currentBarTime != lastBarTime) {
      lastBarTime = currentBarTime;
      return true;
   }
   return false;
}
```

**When NOT to use:** Scalping strategies needing tick-level entry precision,
or trailing stop updates that must respond to every price movement.

### Broker-Agnostic Symbol Properties

Never hardcode tick value, lot size, or decimal places. Read at runtime.

```mql5
// In SymbolConfig.mqh — call once in OnInit()
double g_Point    = SymbolInfoDouble(_Symbol, SYMBOL_POINT);
double g_LotStep  = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP);
double g_MinLot   = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN);
double g_MaxLot   = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MAX);
int    g_Digits   = (int)SymbolInfoInteger(_Symbol, SYMBOL_DIGITS);
double g_TickVal  = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_VALUE);
double g_TickSize = SymbolInfoDouble(_Symbol, SYMBOL_TRADE_TICK_SIZE);
double g_Spread   = (double)SymbolInfoInteger(_Symbol, SYMBOL_SPREAD) * g_Point;
```

Both `SYMBOL_TRADE_TICK_VALUE` and `SYMBOL_TRADE_TICK_SIZE` are needed
because `tickSize != _Point` on metals and indices.

```mql5
// Correct
double riskPerLot = slDistancePoints * (g_TickVal / g_TickSize);

// Wrong — breaks on XAUUSD, indices
double riskPerLot = slDistancePoints * g_TickVal;
```

Always use `_Symbol` rather than a hardcoded string.

---

## Code Patterns

### Main EA Template

```mql5
#property copyright "ohwpstudios"
#property version   "1.00"
#property strict

#include "include\RiskManager.mqh"
#include "include\RegimeFilter.mqh"
#include "include\SignalEngine.mqh"
#include "include\TradeManager.mqh"
#include "include\SessionFilter.mqh"
#include "include\Analytics.mqh"

input group "=== RISK SETTINGS ==="
input double InpRiskPercent  = 1.0;   // Risk per trade (%)
input double InpMaxDailyDD   = 2.0;   // Max daily drawdown (%)
input double InpMaxTotalDD   = 8.0;   // Max total drawdown (%)

input group "=== STRATEGY SETTINGS ==="
input int    InpATRPeriod    = 14;    // ATR period
input double InpATRMultiplier = 1.5;  // SL = ATR * multiplier
input double InpRRRatio      = 2.0;   // Risk:Reward ratio

input group "=== SESSION SETTINGS ==="
input int    InpGMTOffset    = 0;     // Broker GMT offset
input bool   InpLondonSession = true;
input bool   InpNYSession    = true;

input group "=== EA SETTINGS ==="
input int    InpMagicNumber  = 10001;
input bool   InpEnableJournal = true;

CRiskManager   *g_RiskMgr;
CRegimeFilter  *g_Regime;
CSignalEngine  *g_Signal;
CTradeManager  *g_TradeMgr;
CSessionFilter *g_Session;
CAnalytics     *g_Analytics;

int OnInit() {
   g_RiskMgr   = new CRiskManager(InpRiskPercent, InpMaxDailyDD, InpMaxTotalDD);
   g_Regime    = new CRegimeFilter();
   g_Signal    = new CSignalEngine();
   g_TradeMgr  = new CTradeManager(InpMagicNumber);
   g_Session   = new CSessionFilter(InpGMTOffset, InpLondonSession, InpNYSession);
   g_Analytics = new CAnalytics(InpMagicNumber, InpEnableJournal);
   if(!g_RiskMgr.IsReady() || !g_Signal.IsReady()) return INIT_FAILED;
   return INIT_SUCCEEDED;
}

void OnTick() {
   if(!IsNewBar(PERIOD_M15)) return;
   if(!g_RiskMgr.IsTradeAllowed())    return;
   if(!g_Session.IsActiveSession())   return;
   ENUM_REGIME regime = g_Regime.GetCurrentRegime();
   if(regime == REGIME_DEAD || regime == REGIME_UNDEFINED) return;
   STradeSignal sig = g_Signal.GetSignal(regime);
   if(sig.type == SIGNAL_NONE) return;
   double lots = g_RiskMgr.CalculateLotSize(sig.slDistance);
   if(lots <= 0) return;
   g_TradeMgr.OpenTrade(sig, lots);
   g_Analytics.LogSignal(sig, lots);
}

void OnTrade() {
   g_TradeMgr.ManageOpenTrades();
   g_Analytics.UpdateMetrics();
}

void OnDeinit(const int reason) {
   g_Analytics.GenerateSummary();
   delete g_Analytics;  delete g_Session;
   delete g_TradeMgr;   delete g_Signal;
   delete g_Regime;     delete g_RiskMgr;
}
```

---

## Common Mistakes

- **Skipping layers** — a signal should never bypass the regime filter to
  open a trade directly. Each layer enforces a specific concern.
- **Hardcoding symbol properties** — `Point`, `Digits`, `TickValue` differ
  per symbol and per broker. Always read them at runtime.
- **Using `OnTradeTransaction` without `HistorySelect()`** — the deal/order
  data is not automatically available; call `HistorySelect()` first.
- **Assuming 1:1 `OnTradeTransaction` to `OnTrade` ratio** — one `OrderSend`
  can produce multiple `OnTradeTransaction` calls and one or several
  `OnTrade` calls.
- **Forgetting `EventKillTimer()` in `OnDeinit()`** — though auto-destroyed,
  explicit cleanup prevents ambiguity.
- **One-based vs zero-based confusion in indicators** — preprocessor
  numbering is 1-based, runtime `PlotIndexSet*` calls are 0-based.
- **Calling `IsNewBar()` without a static variable** — the `static datetime`
  is essential; without it, every tick sees a "new" bar.

---

## References

| File | Contents | Read when |
|------|----------|-----------|
| `references/event-handlers.md` | All event handler signatures, dedup rules, `OnInit`/`OnDeinit` codes, `OnTradeTransaction` lifecycle, tester event chain | Writing or debugging event handlers; implementing `OnTradeTransaction`; setting up tester optimization criteria |
| `references/predefined-variables.md` | `_Symbol`, `_Period`, `_Digits`, `_Point`, `_LastError`, `_StopFlag`, `_UninitReason`, `_RandomSeed`, `_IsX64`, `_AppliedTo` | Accessing built-in read-only variables in any EA or indicator |
| `references/event-system.md` | `EventSetTimer`, `EventSetMillisecondTimer`, `EventKillTimer`, `EventChartCustom`, timer lifecycle and dedup rules | Implementing periodic execution or cross-chart custom events |
| `references/trade-transactions.md` | `ENUM_TRADE_TRANSACTION_TYPE` values, `MqlTradeTransaction` struct fields, `OnTradeTransaction` switch pattern | Building transaction-aware order/position tracking |
| `references/chart-events.md` | `CHARTEVENT_*` constants, `OnChartEvent` switch pattern, custom event ID range | Implementing mouse/keyboard/UI event handling |
| `references/language-basics.md` | Types, variables, scope, operators, functions, OOP, templates, memory model, preprocessor directives | Understanding MQL5 language fundamentals that underpin EA architecture |
| `references/cexpert-base.md` | `CExpertBase` method reference — series access, symbol/timeframe identity, magic routing | Using the standard-library base class for expert modules |
| `references/cexpert-orchestration.md` | `CExpert` full method reference — init/deinit, event forwarding, open/close/reverse, trailing, trade events | Wiring standard-library EAs; overriding open/close/check methods |
| `references/cexpert-signal.md` | `CExpertSignal` method reference — voting, filters, thresholds, open/close params | Building signal classes with the standard library |
| `references/cexpert-money.md` | `CExpertMoney` method reference — percent risk, volume for open/reverse/close | Implementing money-management classes |
| `references/custom-indicators.md` | `SetIndexBuffer`, `IndicatorSet*`, `PlotIndexSet*`, draw types, buffer setup rules | Building custom indicators with correct buffer/plot configuration |
