# Performance Metrics

Self-written guidance for evaluating MetaTrader strategy results with defensible trading metrics.

---

## Core Metrics

Use these as the baseline set for most strategy reviews:

- net profit
- gross profit
- gross loss
- profit factor
- max drawdown
- total trades
- win rate
- average win
- average loss
- expectancy
- Sharpe ratio
- recovery factor

No single metric is sufficient on its own.

---

## Metric Interpretation

### Profit Factor

Interpretation:

- below 1.0: losing system
- around 1.0 to 1.3: weak edge or fragile edge
- around 1.3 to 1.8: usable but needs context
- above 1.8: strong on paper, but still validate trade count and stability

High profit factor with low sample size is not strong evidence.

### Max Drawdown

Measure both:

- absolute drawdown
- drawdown as a percentage of balance or equity

Always specify the curve basis. Drawdown on closed balance can understate live pain materially.

### Expectancy

Expectancy per trade is often more informative than win rate alone. A high win rate with negative expectancy is a common failure pattern.

### Sharpe Ratio

Useful for normalized return quality, but only meaningful when return sampling and assumptions are clearly defined.

### Recovery Factor

Useful for understanding how much return the strategy generates relative to its worst drawdown.

---

## Trade-Distribution Checks

Add distribution checks beyond summary metrics:

- median trade outcome
- average duration
- outlier contribution to total P&L
- long vs short asymmetry
- symbol concentration
- weekday or session concentration

A strategy that depends on a tiny number of outlier trades should be flagged even if summary metrics look attractive.

---

## Robustness Questions

For every promising result, ask:

1. Is the trade count high enough?
2. Is performance concentrated in one symbol, month, or regime?
3. Does the edge survive realistic costs?
4. Is drawdown tolerable relative to the claimed risk profile?
5. Are returns smooth for a good reason, or because exits hide tail risk?

---

## Common Analytical Traps

Watch for these failures:

- judging by win rate without expectancy
- using balance drawdown when equity drawdown is what matters
- comparing parameter sets with mismatched date windows
- ignoring spread, commission, or swap assumptions
- over-trusting Sharpe on sparse or irregular return samples
- evaluating strategy quality on too few trades

---

## Practical Rule

A strategy is not strong because one metric is high. It is strong when multiple metrics agree and the trade distribution does not hide a structural weakness.