# Tick Generation Internals and Mode Gotchas

## Every Tick Generation Algorithm

```
Tick volume = 1  -> single Close price tick only
Tick volume = 2  -> Open tick, then Close tick only
Tick volume >= 3 -> reference-point algorithm: up to 11 reference points
                    distributed as opening shadow / range / closing shadow (ideal: 3-5-3)
```

Spread in tester is always **floating**, taken from historical data. If historical spread <= 0, the last known spread is used.

## "Open Prices Only" Mode — Hard Limits

```
Cannot use Random Delay execution mode
Cannot access timeframes BELOW the testing timeframe
Cannot access non-multiple timeframes (e.g., testing on M20 -> cannot access M30)
W1 and MN1: bars generated once per day, not once per week/month
Stop Levels and pending orders triggered at specified price (not market — less realistic but avoids false fills)
```

## Real Ticks Mode Specifics

- Stored in TKC files: `\bases\<server>\ticks\<symbol>\YYYYMM.tkc`
- If tick data missing for a bar, tester falls back to generated ticks
- If minute bar missing but tick data present -> tick data is **ignored** (minute bars are authoritative)
- Bars built by **Bid** prices (not Last) in Every Tick mode; Ask = Bid + spread

## Exchange Instrument Order Triggering (Differs from Forex)

```
Stop orders:  triggered by Last price (not Bid/Ask)
Limit orders: triggered by Bid/Ask; executed at order price (no slippage)
Market orders: executed at current Bid/Ask (slippage possible)
```

In "Open prices only" and "1 Minute OHLC" modes: all order types execute at the specified order price regardless of instrument type.
