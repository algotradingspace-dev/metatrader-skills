# Portfolio Correlation Analysis

Self-written guidance for evaluating multiple MetaTrader strategies as a portfolio rather than as isolated systems.

---

## When Portfolio Analysis Matters

Use portfolio analysis when you have any of the following:

- multiple EAs on the same account
- the same EA traded across multiple symbols or timeframes
- multiple parameter variants competing for capital
- several strategies that may share market regimes or tail risk

Single-strategy scorecards are not enough in those cases. A portfolio can fail even when each component looks acceptable in isolation.

---

## Core Questions

A usable portfolio review should answer:

1. How correlated are the strategies?
2. Which strategies dominate returns?
3. Which strategies dominate drawdown?
4. Are exposures diversified by symbol, direction, regime, and holding style?
5. Does combining the strategies improve the return-to-drawdown profile?

If the analysis cannot answer those questions, it is not yet a portfolio analysis. It is only a stack of individual backtests.

---

## Minimum Portfolio Dataset

For each strategy or sleeve, keep:

- strategy name and version
- symbol and timeframe
- test window
- per-trade results or periodic return series
- capital allocation assumption
- major settings or parameter-set label

Portfolio work becomes unreliable when the component datasets use different timestamps, different cost assumptions, or different sample windows without being labeled clearly.

---

## Aggregation Model

Choose the aggregation method explicitly:

- equal-weight by strategy
- capital-weighted by intended allocation
- risk-weighted by volatility or drawdown budget
- capped-weight model to prevent one strategy from dominating

Do not mix these implicitly. The same group of strategies can look conservative or reckless depending on weighting.

---

## Correlation Checks

Start with return correlation between strategy series, but do not stop there.

Check:

- pairwise correlation of daily or weekly returns
- correlation during down periods specifically
- correlation of drawdown phases
- overlap in symbols and sessions traded
- overlap in holding time and trade direction bias

Low overall correlation can still hide synchronized losses during the exact periods that matter.

---

## Concentration Risk

Measure concentration along several axes:

- symbol concentration
- strategy concentration
- timeframe concentration
- regime concentration
- calendar concentration such as weekday or session dependence

If 70% of the portfolio's profit comes from one symbol or one EA, treat the portfolio as concentrated even if the dashboard looks diversified.

---

## Drawdown Interaction

Portfolio drawdown should be measured on the combined curve, not by averaging standalone strategy drawdowns.

Look for:

- max portfolio drawdown
- time spent under water
- contribution of each strategy to the worst drawdown period
- whether the worst portfolio window is caused by one strategy or by synchronized weakness

This is usually where a seemingly diversified portfolio reveals its real structure.

---

## Multi-EA Comparison Table

A useful portfolio comparison table should include:

- strategy name
- allocation weight
- net profit contribution
- drawdown contribution
- trade count
- profit factor
- expectancy
- correlation to the portfolio or to the benchmark sleeve
- notes on concentration or overlap

This helps separate good standalone systems from genuinely helpful portfolio components.

---

## Practical Portfolio Checks

Before approving a portfolio configuration, check:

1. Does the combined curve improve recovery factor versus the top single strategy?
2. Does the combined drawdown stay inside the intended account risk budget?
3. Are returns driven by multiple sleeves or by one dominant engine?
4. Are there hidden duplicates, such as the same logic traded on highly related symbols?
5. Does diversification persist across different market windows?

---

## Reporting Pattern

A portfolio report should separate:

- component scorecards
- allocation assumptions
- combined portfolio metrics
- diversification findings
- concentration warnings
- recommended changes

Do not bury allocation assumptions in footnotes. Allocation is part of the result.

---

## Rule Of Thumb

Portfolio analysis is not about proving that many strategies can coexist. It is about proving that their combination improves the overall risk-adjusted outcome without hiding concentration or synchronized failure.