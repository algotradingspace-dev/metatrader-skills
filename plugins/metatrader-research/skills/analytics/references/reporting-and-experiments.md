# Reporting And Experiments

Self-written guidance for turning MetaTrader analysis into reproducible reports and experiment comparisons.

---

## Scorecard Pattern

Keep scorecards compact and comparable. A practical template includes:

- strategy name and version
- symbol and timeframe
- test window
- parameter-set label
- trade count
- profit factor
- max drawdown
- expectancy
- Sharpe ratio
- recovery factor
- verdict and notes

This is enough for decision review without burying the reader in raw logs.

---

## Comparison Tables

Use comparison tables when evaluating:

- multiple parameter sets
- multiple symbols
- multiple timeframes
- multiple broker datasets
- in-sample vs out-of-sample windows

Keep the key dimensions explicit. Do not compare unlike-for-like runs in the same ranking table.

---

## Experiment Logging

For each run, capture:

- run ID
- timestamp
- code or EA version
- dataset or broker source
- symbol and timeframe
- parameter-set name
- test period
- assumptions such as deposit, leverage, spread model, or costs
- resulting headline metrics

If a result cannot be tied back to an exact configuration, it is not reliable enough for decision-making.

---

## Walk-Forward Structure

For walk-forward analysis, keep these windows separate and labeled:

- optimization window
- validation window
- test window

Do not report a single blended score as if all windows had the same meaning.

---

## A/B And Variant Testing

When comparing two EA variants:

- hold symbol, timeframe, and test dates constant
- change one meaningful variable at a time where possible
- compare both headline and distribution metrics
- keep notes on why a variant exists

This prevents result tables from turning into untraceable parameter soup.

---

## Reporting Boundary

Keep these concerns separate:

- raw analytical tables
- derived metric tables
- narrative conclusions
- launch or rejection recommendations

A report should make it possible to see which statements are calculated facts and which are human judgment.

---

## Practical Rule

The best experiment log is boring: exact inputs, exact assumptions, exact outputs, and an obvious path to reproduce the result later.