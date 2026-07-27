# MT5 Strategy Tester Configuration

## Tester Settings

```
Mode:          Every Tick Based on Real Ticks  (most accurate — always use for M15 and below)
               Every Tick                       (faster; acceptable for H1+ strategies)
               OHLC Only                        (never use — misses intrabar SL hits)

Modelling:     Real ticks for M5 or lower
               Every Tick sufficient for H1+

Spread:        Use current OR set realistic fixed spread:
               XAUUSD: 25-35 | EURUSD: 8-12 | GBPUSD: 12-18 | US500: 30

Deposit:       Match actual funded account size (e.g., $10K, $50K, $100K)
Leverage:      Match the firm's maximum allowed leverage (common: 1:30-1:100)

Minimum test period:   3 years (2021-2024 covers Covid recovery + rate hike cycle)
Recommended period:    5 years (2019-2024 covers multiple market regimes)

Optimisation method:
  Genetic Algorithm   -> fast initial scan across large parameter space
  Exhaustive          -> final validation of best 5-10 parameter combinations only

Commission:    Always include! Typical: $7 per round-trip per standard lot
```

## Common Mistakes

- Running "Open Prices Only" and missing intrabar SL hits
- Not including commission — always include $5-8/lot round-trip
- Testing on a single year with one market regime
- Accepting the first optimisation pass without OOS validation
