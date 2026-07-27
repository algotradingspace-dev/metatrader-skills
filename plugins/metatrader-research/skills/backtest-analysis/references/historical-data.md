# Historical Data Requirements and Start Date Shifts

The tester always preloads a "pre-start history buffer" before the test begins.

## Minimum Buffer by Timeframe

| Timeframe | Buffer Loaded | Possible Start Shift |
|-----------|---------------|---------------------|
| M1 | >=100 bars (~1h 40m) | Virtually none |
| M15 | >100 bars (~25h) | Minimal |
| H1 | >=100 bars (~4 days) | Minimal |
| D1 | >=100 bars (~5 months) | Up to 5 months |
| W1 | >=100 weeks (~2 years) | Up to 2 years |
| MN1 | >=100 months (~8 years) | Up to 8 years |

For D1 and below, the terminal also downloads data from the start of the previous calendar year (e.g., test start 2023-03-01 -> download from 2022-01-01).

## Journal Message — NOT an Error

```
start time changed to 2024.03.15 00:00 to provide data at beginning
```

This means insufficient history was available; the tester shifted the start date forward automatically.

## Tick Storage Paths (for manual inspection)

```
History: \Program Files\MetaTrader 5 Strategy Tester\Tester\bases\<server>\history\<symbol>
Ticks:   \Program Files\MetaTrader 5 Strategy Tester\Tester\bases\<server>\ticks\<symbol>
Ticks per-agent: tester_catalog\Agent-IP-Port\bases\<server>\history\<symbol>
```

## Multi-Currency Test Setup

1. Open charts for all required symbols in Market Watch before testing
2. Scroll charts to history beginning to trigger download
3. First run will pause to download cross-rate history (e.g., testing EURCHF with USD deposit -> EURUSD + USDCHF downloaded automatically)
