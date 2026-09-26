# MQL Development Standards

## EA Structure (Required)

```mql5
//+------------------------------------------------------------------+
//| EA Name                                                           |
//| Version: X.Y                                                      |
//| Author: [name]                                                    |
//| Description: [purpose]                                            |
//| Changelog:                                                        |
//|   vX.Y - [date] - [changes]                                      |
//+------------------------------------------------------------------+
```

## Input Parameters

Group and comment all inputs clearly:

```mql5
//--- Trade Settings
input double   InpLotSize       = 0.01;   // Base lot size
input int      InpMagicNumber   = 123456; // Magic number for this EA
input int      InpSlippage      = 3;      // Max slippage in points

//--- Risk Management
input double   InpRiskPercent   = 1.0;    // Risk per trade (%)
input double   InpMaxDrawdown   = 20.0;   // Max drawdown before halt (%)

//--- Exit Settings
input int      InpStopLoss      = 50;     // Stop loss in points
input int      InpTakeProfit    = 100;    // Take profit in points
input bool     InpUseTrailing   = true;   // Enable trailing stop
input int      InpTrailingStart = 30;     // Trailing start (points)
input int      InpTrailingStep  = 10;     // Trailing step (points)
```

## Mandatory EA Components

1. **Magic number support** — isolate trades from other EAs
2. **Error handling** — handle `OrderSend` failures, reconnection, invalid stops
3. **Lot size validation** — respect `MODE_MINLOT`, `MODE_MAXLOT`, `MODE_LOTSTEP`, account leverage
4. **Spread filter** — skip entries during abnormal spreads
5. **Multi-timeframe awareness** — if strategy requires it, sync across timeframes
6. **Logging** — `Print()` key events for journal debugging

### Error Handling Pattern

```mql5
int ticket = OrderSend(Symbol(), OP_BUY, lots, Ask, slippage, sl, tp, comment, magic);
if(ticket < 0)
{
   int err = GetLastError();
   PrintFormat("OrderSend failed: error %d - %s", err, ErrorDescription(err));

   if(err == ERR_REQUOTE || err == ERR_PRICE_CHANGED)
   {
      RefreshRates();
      // retry once
   }
}
```

### .set File Presets

Provide three presets per EA:

| Preset | Risk | Description |
|--------|------|-------------|
| `conservative` | Low | Smaller lots, wider stops, lower frequency |
| `moderate` | Medium | Balanced risk/reward |
| `aggressive` | High | Larger lots, tighter stops, higher frequency |

### MQL5 Directory Deployment

```
MQL5/
├── Experts/          # EA .ex5 and .mq5 files
├── Indicators/       # Custom indicator files
├── Include/          # Shared .mqh header files
├── Libraries/        # Shared .ex5 library files
├── Scripts/          # One-shot scripts
├── Files/            # Runtime data files (read/write sandbox)
└── Presets/          # .set parameter files
```

## Key Differences: MQL4 vs MQL5

> Canonical MQL5 reference: [OnTick](https://www.mql5.com/en/docs/event_handlers/ontick) · [OnTimer](https://www.mql5.com/en/docs/event_handlers/ontimer) · [OnTrade](https://www.mql5.com/en/docs/event_handlers/ontrade) · [OrderSend](https://www.mql5.com/en/docs/trading/ordersend)

| Feature | MQL4 | MQL5 |
|---------|------|------|
| Order model | Direct execution | Positions + deals + orders |
| Event handler | `start()` | `OnTick()`, `OnTimer()`, `OnTrade()` |
| Order functions | `OrderSend()`, `OrderModify()` | `CTrade` class or `OrderSend()` with `MqlTradeRequest` |
| Indicator buffers | `SetIndexBuffer()` | `SetIndexBuffer()` with `INDICATOR_DATA` type |
| Tester | Strategy Tester | Multi-currency, multi-timeframe tester |
| OOP | Limited | Full OOP with classes, interfaces, inheritance |
