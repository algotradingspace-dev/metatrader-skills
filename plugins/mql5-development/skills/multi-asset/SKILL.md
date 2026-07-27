---
name: multi-asset
description: >
  Multi-asset and multi-pair EA management for MQL5. Use for all logic involving
  trading more than one instrument: per-symbol configuration profiles (SSymbolConfig
  struct); 17 pre-built asset profiles across forex, metals, indices, and crypto CFDs;
  portfolio-level risk with correlation group limits; CMultiAssetManager class for
  position discovery, group counting, and total-risk enforcement; magic number assignment
  per symbol; multi-symbol OnTick architecture that processes each symbol independently.
  Trigger: "multi-pair", "portfolio EA", "multiple symbols", "all pairs",
  "forex and gold", "symbol manager", "asset class", "per-pair settings",
  "correlation management", "basket trading", "run on all symbols",
  "trade everything", "SymbolInfoInteger", "SymbolSelect".
---

# Multi-Asset

A true trading system trades multiple instruments with proper portfolio-level
risk controls. One brain, many markets — with isolation per symbol and
correlation limits across the portfolio.

---

## Purpose

Defines the infrastructure for running a single EA across multiple instruments:
per-symbol configuration profiles, correlation-based position limits, total
portfolio risk caps, and a multi-symbol OnTick processing loop. Also catalogs
the `SymbolInfo*` API surface for symbol discovery and metadata access.

---

## When to Use

- Building an EA designed to trade multiple pairs simultaneously
- Adding a new asset class or symbol to an existing multi-asset EA
- Diagnosing over-correlated position stacking
- Enforcing total portfolio risk limit across all open positions
- Checking symbol trading conditions (stops level, fill mode, execution mode)
- Looking up symbol property identifiers or API signatures

**Do NOT use** for:
- Single-symbol EA architecture -> use `ea-architect`
- Market regime detection -> use `market-regime`
- Risk/sizing for a single position -> use `risk-engine`

---

## Core Guidance

### SSymbolConfig — Per-Symbol Parameter Profile

```mql5
struct SSymbolConfig {
   string          symbol;
   int             magicNumber;
   double          maxSpreadPoints;
   double          atrMultiplierSL;
   double          atrMultiplierTP;
   int             atrPeriod;
   ENUM_TIMEFRAMES entryTF;
   ENUM_TIMEFRAMES htfTF;
   int             sessionStartUTC;
   int             sessionEndUTC;
   double          correlationGroup;
   string          assetClass;        // "forex" | "metal" | "index" | "crypto"
};
```

### Pre-Built Asset Profile Table (17 instruments)

Factory defaults for 17 instruments across forex majors, metals, US/EU indices,
and crypto CFDs. Each has a unique magic number, asset-appropriate spread and
ATR settings, session windows, and correlation group IDs.

### Correlation Groups and Position Limits

```
Group 1.0 — USD Majors (EUR/GBP/CHF):        EURUSD, GBPUSD, USDCHF  -> max 2
Group 2.0 — JPY pairs:                       USDJPY, EURJPY, GBPJPY  -> max 2
Group 3.0 — Commodity currencies:             AUDUSD, NZDUSD          -> max 1
Group 4.0 — CAD:                             USDCAD                  -> max 1
Group 5.0 — Metals:                          XAUUSD, XAGUSD          -> max 1
Group 6.0 — US Indices (0.95 correlation):   US500, US100, US30      -> max 1
Group 7.0 — EU Indices:                      GER40, UK100            -> max 1
Group 8.0 — Crypto:                          BTCUSD, ETHUSD          -> max 1
Portfolio:                                   all groups              -> max 5% total open risk
```

### CMultiAssetManager

```mql5
class CMultiAssetManager {
   bool GetSymbolConfig(string symbol, SSymbolConfig &cfg);
   bool IsNewPositionAllowed(SSymbolConfig &cfg);
   int  CountPositionsInGroup(double groupId);
   double GetTotalOpenRiskPct();
};
```

### Multi-Symbol OnTick

```mql5
void OnTick() {
   if(!IsNewBar(PERIOD_M15)) return;
   for(int i=0;i<ArraySize(g_SymbolProfiles);i++)
      ProcessSymbol(g_SymbolProfiles[i]);
}

void ProcessSymbol(SSymbolConfig &cfg) {
   // Spread check -> risk gate -> portfolio check -> session -> signal -> lot size -> trade
   double spread=(double)SymbolInfoInteger(cfg.symbol,SYMBOL_SPREAD);
   if(spread>cfg.maxSpreadPoints) return;
   if(!g_RiskMgr.IsTradeAllowed()) return;
   if(!g_AssetMgr.IsNewPositionAllowed(cfg)) return;
   if(!IsSymbolSessionActive(cfg)) return;
   STradeSignal sig=g_Signal.GetSignalForSymbol(cfg.symbol,cfg);
   if(sig.type==SIGNAL_NONE) return;
   double atr=iATR(cfg.symbol,cfg.entryTF,cfg.atrPeriod,1);
   double slDist=atr*cfg.atrMultiplierSL/SymbolInfoDouble(cfg.symbol,SYMBOL_POINT);
   double lots=g_RiskMgr.CalculateLotSizeSymbol(cfg.symbol,slDist);
   if(lots<=0) return;
   g_TradeMgr.OpenTradeOnSymbol(cfg.symbol,sig,lots,cfg.magicNumber);
}
```

---

## References

Symbol info enum reference (`ENUM_SYMBOL_INFO_INTEGER/DOUBLE/STRING`), symbol
discovery API (`SymbolsTotal`, `SymbolName`, `SymbolSelect`), tick/session/margin
helpers (`SymbolInfoTick`, `SymbolInfoMarginRate`, `SymbolInfoSession*`), and
DOM API (`MarketBookAdd/Get/Release`) are documented in the MQL5 Reference:
- `docs/mql5_com_-_docs/constants-environment_state-marketinfoconstants.md`
- `docs/mql5_com_-_docs/marketinformation-symbolstotal.md`
- `docs/mql5_com_-_docs/marketinformation-symbolname.md`
- `docs/mql5_com_-_docs/marketinformation-symbolselect.md`
- `docs/mql5_com_-_docs/marketinformation-symbolinfotick.md`
- `docs/mql5_com_-_docs/marketinformation-marketbookadd.md`
