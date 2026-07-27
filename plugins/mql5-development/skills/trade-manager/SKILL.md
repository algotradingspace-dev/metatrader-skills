---
name: trade-manager
description: >
  Post-entry trade lifecycle management for MQL5 EAs. Use for: ATR-based,
  swing-based, and chandelier trailing stops; breakeven logic; partial close
  and scale-out strategies; multi-target take profit; position scaling
  (pyramiding); trade modification via CTrade; managing multiple open positions;
  OrderSend/OrderSendAsync retcode handling; position, order, and history
  iteration APIs; pre-trade margin and profit calculation; standard-library
  trade wrapper classes (CTrade, CPositionInfo, COrderInfo, CDealInfo,
  CSymbolInfo, CAccountInfo). Trigger: "trailing stop", "breakeven", "partial
  close", "scale out", "pyramiding", "take profit", "manage positions",
  "move SL", "CTrade", "position management", "trade modification",
  "multi-target TP", "trail", "BE", "OrderSend", "OrderCheck".
---

# Trade Manager

Trade management is where edge is multiplied. Good entries with poor management
underperform. Average entries with excellent management outperform.

---

## Purpose

Defines Layer 4 of the 5-layer EA architecture: post-entry position management
— trailing stops, breakeven, partial closes, and trade lifecycle. Consumes
`STradeSignal` from Layer 3 (signal-engine) and manages positions until exit.

---

## When to Use

- Building Layer 4 (TradeManager) for any EA
- Adding trailing stops, breakeven, or partial close to an existing EA
- Diagnosing why an EA gives back too much open profit
- Implementing custom position scanners without CTrade wrapper
- Computing lot size from risk % and SL distance
- Validating R:R ratio before entry
- Looking up standard-library wrapper methods by class

**Do NOT use** for:
- Entry signal generation → use `signal-engine`
- Risk/sizing policy or drawdown guards → use `risk-engine`
- EA architecture / module wiring → use `ea-architect`

---

## Core Guidance

### CTradeManager Core Class

```mql5
#include <Trade\Trade.mqh>
#include <Trade\PositionInfo.mqh>

class CTradeManager : public IModule {
private:
   CTrade         m_trade;
   CPositionInfo  m_position;
   int            m_magicNumber;
   int            m_slippage;
   double         m_beActivationRR;
   double         m_trailActivationRR;
   double         m_partialCloseRR;
   double         m_partialCloseSize;

public:
   CTradeManager(int magic, double beRR = 1.0, double trailRR = 1.5,
                 double partialRR = 1.0, double partialSz = 0.5) {
      m_magicNumber = magic; m_slippage = 10;
      m_beActivationRR = beRR; m_trailActivationRR = trailRR;
      m_partialCloseRR = partialRR; m_partialCloseSize = partialSz;
      m_trade.SetExpertMagicNumber(magic);
      m_trade.SetDeviationInPoints(m_slippage);
      m_trade.SetTypeFilling(ORDER_FILLING_IOC);
   }
   bool   IsReady()   { return true; }
   void   Reset()     { }
   string GetStatus() { return "TradeManager: " + IntegerToString(PositionsTotal()) + " open"; }
};
```

### Opening Trades

```mql5
bool OpenTrade(STradeSignal &sig, double lots) {
   if(lots <= 0 || sig.type == SIGNAL_NONE) return false;
   string comment = "M:" + IntegerToString(m_magicNumber) + " " + sig.reason;
   bool result = false;
   if(sig.type == SIGNAL_BUY)
      result = m_trade.Buy(lots, _Symbol, 0, sig.stopLoss, sig.takeProfit, comment);
   else if(sig.type == SIGNAL_SELL)
      result = m_trade.Sell(lots, _Symbol, 0, sig.stopLoss, sig.takeProfit, comment);
   if(!result)
      PrintFormat("OpenTrade FAILED: %d - %s | SL:%.5f TP:%.5f",
                  GetLastError(), _Symbol, sig.stopLoss, sig.takeProfit);
   return result;
}
```

### Management Loop

```mql5
void ManageOpenTrades() {
   for(int i = PositionsTotal() - 1; i >= 0; i--) {
      if(!m_position.SelectByIndex(i)) continue;
      if(m_position.Magic() != m_magicNumber) continue;
      ulong  ticket  = m_position.Ticket();
      double open    = m_position.PriceOpen();
      double sl      = m_position.StopLoss();
      double tp      = m_position.TakeProfit();
      double current = m_position.PriceCurrent();
      double slDist  = MathAbs(open - sl);
      if(slDist <= 0) continue;
      ApplyPartialClose(ticket, open, sl, tp, current, slDist);
      ApplyBreakeven(ticket, open, sl, tp, current, slDist);
      ApplyATRTrail(ticket, open, sl, tp, current, slDist);
   }
}
```

### Breakeven and ATR Trailing Stop

```mql5
void ApplyBreakeven(ulong ticket, double open, double sl, double tp,
                    double current, double slDist) {
   double spread = (double)SymbolInfoInteger(_Symbol, SYMBOL_SPREAD) * _Point;
   if(m_position.PositionType() == POSITION_TYPE_BUY) {
      double rr = (current - open) / slDist;
      double newSL = open + spread;
      if(rr >= m_beActivationRR && sl < newSL - _Point)
         m_trade.PositionModify(ticket, newSL, tp);
   } else {
      double rr = (open - current) / slDist;
      double newSL = open - spread;
      if(rr >= m_beActivationRR && sl > newSL + _Point)
         m_trade.PositionModify(ticket, newSL, tp);
   }
}

void ApplyATRTrail(ulong ticket, double open, double sl, double tp,
                   double current, double slDist) {
   double atr   = iATR(_Symbol, PERIOD_H1, 14, 1);
   double trail = atr * 1.5;
   if(m_position.PositionType() == POSITION_TYPE_BUY) {
      double rr = (current - open) / slDist;
      double newSL = current - trail;
      if(rr >= m_trailActivationRR && newSL > sl + _Point)
         m_trade.PositionModify(ticket, newSL, tp);
   } else {
      double rr = (open - current) / slDist;
      double newSL = current + trail;
      if(rr >= m_trailActivationRR && newSL < sl - _Point)
         m_trade.PositionModify(ticket, newSL, tp);
   }
}
```

### Partial Close

```mql5
void ApplyPartialClose(ulong ticket, double open, double sl, double tp,
                       double current, double slDist) {
   static ulong s_done[];
   for(int i = 0; i < ArraySize(s_done); i++)
      if(s_done[i] == ticket) return;
   double rr = (m_position.PositionType() == POSITION_TYPE_BUY)
               ? (current - open) / slDist : (open - current) / slDist;
   if(rr < m_partialCloseRR) return;
   double totalLots = m_position.Volume();
   double lotStep   = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_STEP);
   double minLot    = SymbolInfoDouble(_Symbol, SYMBOL_VOLUME_MIN);
   double lotsToClose = MathFloor(totalLots * m_partialCloseSize / lotStep) * lotStep;
   if(lotsToClose < minLot) return;
   if(lotsToClose >= totalLots) lotsToClose = totalLots - minLot;
   if(m_trade.PositionClosePartial(ticket, lotsToClose)) {
      int sz = ArraySize(s_done);
      ArrayResize(s_done, sz + 1);
      s_done[sz] = ticket;
   }
}

void CloseAllPositions(string reason = "") {
   for(int i = PositionsTotal() - 1; i >= 0; i--) {
      if(!m_position.SelectByIndex(i)) continue;
      if(m_position.Magic() != m_magicNumber) continue;
      m_trade.PositionClose(m_position.Ticket());
   }
   if(reason != "") Print("CloseAll reason: ", reason);
}
```

---

## Code Patterns — Strategy Profiles

```mql5
// Sniper (high R:R, low WR): no partial, BE at 1.5, trail at 2.0
g_TradeMgr = new CTradeManager(magic, 1.5, 2.0, 99.0, 0.0);
// Scalper (quick profit): 50% partial at 1.0, BE at 0.8, tight trail at 1.2
g_TradeMgr = new CTradeManager(magic, 0.8, 1.2, 1.0, 0.5);
// Swing (multi-day): 33% partial at 1.0 and 2.0, wide trail at 2.0
g_TradeMgr = new CTradeManager(magic, 1.0, 2.0, 1.0, 0.33);
```

---

## Common Mistakes

- **Iterating positions forward when closing** — closing a position shifts
  indices; always iterate `total-1` to `0`
- **Forgetting `HistorySelect()` before reading history** — deal/order history
  is not available without first selecting a time range
- **Not rounding volume to lot step** — sending unrounded volume causes
  `TRADE_RETCODE_INVALID_VOLUME`
- **Redundant modify calls** — check current SL/TP before sending a modify;
  unnecessary calls burn rate limits and generate log noise
- **Hardcoding slippage or fill policy** — use `SetTypeFillingBySymbol()`
  instead of assuming `ORDER_FILLING_IOC` works on every broker
- **Not guarding `INVALID_HANDLE` on `PositionClose()`** — a closed or
  stale ticket returns false with no error; verify ticket validity first

---

## References

| File | Contents | Read when |
|------|----------|-----------|
| `references/strategy-profiles.md` | Sniper/scalper/swing profile RR configs, constructor examples | Choosing management parameters for a strategy type |
| `references/raw-ordersend-api.md` | `MqlTradeRequest`/`MqlTradeResult` fields, `TRADE_RETCODE_*`, `OrderSend` vs `OrderSendAsync`, `OrderCheck` | Using raw API instead of CTrade; debugging retcode failures |
| `references/trade-access-api.md` | Position selection patterns, `ENUM_POSITION_PROPERTY_*`, pending order iteration, `ENUM_ORDER_PROPERTY_*` | Iterating positions or pending orders; reading property enums |
| `references/history-access-api.md` | `HistorySelect` patterns, deal/order iteration, `ENUM_DEAL_ENTRY`, `ENUM_DEAL_PROPERTY_*` | Analysing past trades; duplicate-open prevention |
| `references/margin-profit-calculation.md` | `OrderCalcMargin`, `OrderCalcProfit`, `RiskToLots`, R:R validation | Pre-trade sizing and risk validation |
| `references/ctrade-class.md` | Full `CTrade` method table (70+ methods: open/modify/close, request/result/check introspection) | Any CTrade wrapper usage |
| `references/cpositioninfo-class.md` | Full `CPositionInfo` method table (25+ methods: select, read price/SL/TP, snapshot) | Reading open position state |
| `references/corderinfo-class.md` | `COrderInfo` + `CHistoryOrderInfo` method tables | Reading active or historical pending orders |
| `references/cdealinfo-class.md` | Full `CDealInfo` method table (20+ methods: ticket, time, type, entry, profit, commission) | Analysing filled deal records |
| `references/csymbolinfo-accountinfo.md` | `CSymbolInfo` (70+ methods) + `CAccountInfo` (30+ methods) method tables | Reading symbol properties, margin rules, account state |
