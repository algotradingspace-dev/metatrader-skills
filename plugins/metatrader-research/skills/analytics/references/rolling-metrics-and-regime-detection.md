# Rolling Metrics And Regime Detection

Self-written guidance for evaluating how MetaTrader strategies and portfolios behave across time, not just across full-sample summaries.

---

## Why This Matters

Full-period metrics can hide structural decay. A strategy can look strong over the entire test window while degrading badly in later segments or failing under specific market conditions.

Rolling and regime analysis helps answer:

- Is the edge stable over time?
- Does drawdown cluster in specific windows?
- Does the strategy depend on one market regime?
- Does diversification persist during difficult periods?

---

## Rolling Window Metrics

Useful rolling metrics include:

- rolling mean return
- rolling volatility
- rolling Sharpe ratio
- rolling max drawdown
- rolling win rate
- rolling profit factor when trade windows are large enough

Use rolling windows that match the data frequency and trade density. Windows that are too short produce noise; windows that are too long hide transitions.

---

## Example: Rolling Return And Volatility

```python
window = 60

rolling = pd.DataFrame(index=portfolio_returns.index)
rolling["rolling_mean_return"] = portfolio_returns.rolling(window).mean()
rolling["rolling_volatility"] = portfolio_returns.rolling(window).std()
```

If the return series is daily, a `window` of 60 is roughly a quarterly view. Adjust the window to the true cadence of the data.

---

## Example: Rolling Sharpe

```python
annualization = 252 ** 0.5

rolling["rolling_sharpe"] = (
    rolling["rolling_mean_return"] /
    rolling["rolling_volatility"]
) * annualization
```

Interpret the rolling Sharpe as a stability signal, not as a standalone verdict. A strategy that alternates between strong positive and strongly negative rolling Sharpe is structurally different from one with a steady moderate profile.

---

## Example: Rolling Drawdown

```python
equity_curve = (1.0 + portfolio_returns).cumprod()
rolling_peak = equity_curve.cummax()
drawdown = equity_curve / rolling_peak - 1.0

rolling["drawdown"] = drawdown
rolling["rolling_max_drawdown_60"] = drawdown.rolling(60).min()
```

This helps reveal whether risk is concentrated in a few bad windows rather than spread evenly over time.

---

## Regime Segmentation

Useful regime labels include:

- high-volatility vs low-volatility periods
- trend vs range conditions
- bullish vs bearish higher-timeframe phases
- London, New York, and Asia session slices
- event-heavy vs quiet macro periods

The exact segmentation method matters less than consistency. The point is to compare behavior across meaningful states, not to invent perfect market labels.

---

## Volatility Regime Example

```python
volatility = portfolio_returns.rolling(20).std()
threshold = volatility.median()

regime = pd.Series("low_vol", index=portfolio_returns.index)
regime[volatility > threshold] = "high_vol"
```

Once labeled, compare returns, drawdowns, and hit rates by regime.

---

## Session And Calendar Slices

If the strategy is intraday or trade-level, segment by:

- weekday
- trading session
- month or quarter
- pre-news and post-news windows where applicable

This helps distinguish a genuine edge from a narrow timing dependency.

---

## Portfolio Stability Checks

For portfolios, examine:

- rolling correlation between sleeves
- rolling contribution to returns
- rolling contribution to drawdown
- whether a previously diversifying sleeve becomes synchronized with the rest

Diversification should be treated as time-varying, not static.

---

## Practical Comparison Questions

Use rolling and regime analysis to ask:

1. Does the portfolio still diversify in bad months?
2. Which sleeve becomes dangerous in high-volatility windows?
3. Does one strategy only work in one regime?
4. Is the latest period meaningfully worse than the historical average?
5. Are strong full-sample metrics being carried by one exceptional window?

---

## Warning Signs

Be skeptical when you see:

- steadily worsening rolling Sharpe
- repeated new drawdown lows in recent windows
- regime dependence that disappears outside one narrow market state
- diversification that breaks exactly when losses begin
- a portfolio whose recent behavior is much worse than its long-run summary

---

## Rule Of Thumb

If a strategy or portfolio only looks good when everything is averaged together, the analysis is incomplete. Time-segmented and regime-segmented views are often where the real story appears.