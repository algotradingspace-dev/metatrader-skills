# Pre-Trade Margin and Profit Calculation

> Use before sending an order to validate sizing and expected outcome.

## OrderCalcMargin / OrderCalcProfit

```mql5
// Margin required for an order
bool OrderCalcMargin(ENUM_ORDER_TYPE action, string symbol,
                     double volume, double price, double& margin);

// Estimated profit for a closed trade
bool OrderCalcProfit(ENUM_ORDER_TYPE action, string symbol,
                     double volume, double price_open, double price_close,
                     double& profit);
```

## Lot Sizing by Risk %

```mql5
double RiskToLots(string symbol, double riskPct, double slPoints) {
   double accountBalance = AccountInfoDouble(ACCOUNT_BALANCE);
   double riskAmount     = accountBalance * riskPct / 100.0;
   double tickValue      = SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_VALUE);
   double tickSize       = SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_SIZE);
   double lotStep        = SymbolInfoDouble(symbol, SYMBOL_VOLUME_STEP);
   double minLot         = SymbolInfoDouble(symbol, SYMBOL_VOLUME_MIN);
   double maxLot         = SymbolInfoDouble(symbol, SYMBOL_VOLUME_MAX);

   if(tickValue == 0 || tickSize == 0 || slPoints == 0) return minLot;
   double valuePerLotPerPoint = tickValue / tickSize;
   double lots = riskAmount / (slPoints * valuePerLotPerPoint);
   lots = MathFloor(lots / lotStep) * lotStep;
   return MathMax(minLot, MathMin(maxLot, lots));
}

// Validate with margin check before sending
double margin = 0;
double ask = SymbolInfoDouble(symbol, SYMBOL_ASK);
if(OrderCalcMargin(ORDER_TYPE_BUY, symbol, lots, ask, margin)) {
   if(margin > AccountInfoDouble(ACCOUNT_MARGIN_FREE) * 0.5)
      lots = lots * 0.5;
}
```

## Expected R:R Validation

```mql5
double entryPrice = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
double slPrice    = entryPrice - 50 * _Point;
double tpPrice    = entryPrice + 100 * _Point;
double profitIfTP = 0, lossIfSL = 0;

OrderCalcProfit(ORDER_TYPE_BUY, _Symbol, lots, entryPrice, tpPrice, profitIfTP);
OrderCalcProfit(ORDER_TYPE_BUY, _Symbol, lots, entryPrice, slPrice, lossIfSL);

double actualRR = (lossIfSL != 0) ? MathAbs(profitIfTP / lossIfSL) : 0;
if(actualRR < 1.5) return;  // skip trades below minimum R:R
```
