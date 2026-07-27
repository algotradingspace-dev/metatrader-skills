# Testing Report Metric Definitions

## Drawdown Types — Three Distinct Measures

```
Balance DD Absolute  = InitialDeposit - MinBalance  (peak from deposit, in money)
Balance DD Maximal   = Max(Local_High - Next_Local_Low)  (worst swing, in money)
Balance DD Relative  = Max((Local_High - Local_Low) / Local_High * 100%)  (worst %, also shows money in brackets)

Equity DD variants   = same three calculations applied to equity curve instead of balance curve
```

## Core Performance Metrics

```
Profit Factor    = Gross Profit / Gross Loss  (1.0 = breakeven)
Recovery Factor  = Net Profit / Max DD  (higher = more efficient recovery)
Expected Payoff  = Net Profit / Total Trades  (average profit per trade)
AHPR             = arithmetic mean of per-trade equity % change  (overestimates performance vs GHPR)
GHPR             = geometric mean of per-trade equity change  (more conservative, use this)
```

## Sharpe Ratio — MT5 Interpretation (risk-free rate = 0)

```
< 0    -> unprofitable
0-1    -> risk does not pay off (consider only if no alternatives)
>= 1.0 -> risk pays off, strategy viable
>= 3.0 -> very low probability of loss per individual trade
```

## History Quality

- Calculated as correct/incorrect 1-minute bars ratio, split into 1-199 intervals
- Green = good, red = quality < 50%
- Bars with tick volume = 1 and different OHLC values are marked incorrect
- History gaps also count as incorrect data
