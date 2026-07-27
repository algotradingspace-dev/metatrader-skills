# Portfolio Recipes

Concrete pandas-oriented recipes for portfolio analysis across multiple MetaTrader strategies.

---

## Recipe: Build A Strategy Return Matrix

Use this when each strategy already has a periodic return series and you want a common matrix for correlation and portfolio aggregation.

```python
import pandas as pd


def build_return_matrix(strategy_frames):
    series = []
    for strategy_name, frame in strategy_frames.items():
        data = frame[["time", "return"]].copy()
        data = data.rename(columns={"return": strategy_name})
        series.append(data.set_index("time"))

    matrix = pd.concat(series, axis=1).sort_index()
    return matrix.fillna(0.0)
```

Notes:

- Use UTC-normalized timestamps before merging
- Filling missing returns with `0.0` is appropriate only when the interpretation is “strategy had no return event in that period”
- If missing data means “unknown,” do not fill blindly

---

## Recipe: Compute A Correlation Matrix

Use a normalized return matrix, not raw trade P&L rows.

```python
correlation = return_matrix.corr()
print(correlation.round(3))
```

If you care about stress behavior, also compute correlation on filtered down periods:

```python
down_mask = return_matrix.mean(axis=1) < 0
stress_correlation = return_matrix.loc[down_mask].corr()
print(stress_correlation.round(3))
```

Notes:

- overall correlation can hide synchronized losses
- inspect both full-period and adverse-period correlation

---

## Recipe: Build A Combined Portfolio Curve

Use explicit weights rather than averaging strategy returns implicitly.

```python
weights = {
    "ea_trend": 0.35,
    "ea_mean_reversion": 0.40,
    "ea_breakout": 0.25,
}

weight_series = pd.Series(weights)
portfolio_returns = return_matrix.mul(weight_series, axis=1).sum(axis=1)

portfolio_curve = pd.DataFrame({
    "portfolio_return": portfolio_returns,
})
portfolio_curve["equity_curve"] = (1.0 + portfolio_curve["portfolio_return"]).cumprod()
```

Notes:

- weights should sum to 1.0 unless you are modeling leverage or idle cash explicitly
- store the weight set with the result so the portfolio can be reproduced later

---

## Recipe: Merge Equity Curves By Strategy

If each strategy is already represented as an equity curve instead of periodic returns, merge them first and derive comparisons from there.

```python
def merge_equity_curves(curves):
    prepared = []
    for strategy_name, frame in curves.items():
        data = frame[["time", "equity"]].copy()
        data = data.rename(columns={"equity": strategy_name})
        prepared.append(data.set_index("time"))

    merged = pd.concat(prepared, axis=1).sort_index()
    return merged.ffill()
```

Notes:

- `ffill()` is appropriate for equity snapshots carried forward through time
- make sure all curves share a comparable base capital before direct comparison

---

## Recipe: Calculate Portfolio Drawdown

Always calculate drawdown on the combined portfolio curve, not on averaged component drawdowns.

```python
portfolio_curve["rolling_peak"] = portfolio_curve["equity_curve"].cummax()
portfolio_curve["drawdown"] = (
    portfolio_curve["equity_curve"] / portfolio_curve["rolling_peak"] - 1.0
)

max_drawdown = portfolio_curve["drawdown"].min()
print({"max_drawdown": float(max_drawdown)})
```

This is the number that matters for portfolio-level risk tolerance.

---

## Recipe: Build An Allocation Table

Use a flat allocation table when comparing what each sleeve contributes.

```python
allocation_table = pd.DataFrame(
    {
        "weight": weight_series,
        "mean_return": return_matrix.mean(),
        "volatility": return_matrix.std(),
        "total_return": (1.0 + return_matrix).prod() - 1.0,
    }
)

allocation_table["weighted_mean_return"] = (
    allocation_table["weight"] * allocation_table["mean_return"]
)

print(allocation_table.sort_values("weight", ascending=False))
```

Useful extensions:

- add drawdown contribution estimates
- add trade count per sleeve
- add concentration warnings for oversized sleeves

---

## Recipe: Compare Standalone Vs Portfolio Results

This is useful when deciding whether an additional strategy improves the portfolio or only adds noise.

```python
summary = pd.DataFrame(
    {
        "standalone_total_return": (1.0 + return_matrix).prod() - 1.0,
        "standalone_volatility": return_matrix.std(),
        "correlation_to_portfolio": return_matrix.corrwith(portfolio_returns),
    }
)

print(summary.sort_values("correlation_to_portfolio"))
```

Interpretation:

- low or moderate correlation can be valuable if the standalone profile is acceptable
- high correlation with weaker returns usually means duplication, not diversification

---

## Recipe: Contribution During Worst Portfolio Window

When the portfolio suffers, identify who caused it.

```python
worst_timestamp = portfolio_curve["drawdown"].idxmin()
worst_contributors = return_matrix.loc[worst_timestamp].sort_values()
print(worst_contributors)
```

For longer stress windows, slice a date range around the worst drawdown period and sum contributions by strategy.

---

## Practical Rule

Portfolio analytics should make the combination clearer than the components. If the combined view is harder to reason about than the standalone scorecards, the portfolio analysis layer is not structured well enough yet.