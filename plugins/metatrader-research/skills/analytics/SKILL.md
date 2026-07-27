---
name: analytics
description: >
  MetaTrader analytics and research workflows in Python. Use for: analysing
  backtest outputs and trade histories; computing performance metrics (drawdown,
  Sharpe, Profit Factor, Calmar, recovery, expectancy); building pandas-based
  evaluation pipelines; comparing EA variants and parameter sets; performing
  portfolio analysis with correlation checks and concentration risk; preparing
  scorecards, reports, and experiment logs; regime segmentation and rolling
  metrics. Trigger: "analytics", "performance metrics", "pandas", "drawdown",
  "Sharpe ratio", "Calmar", "Profit Factor", "backtest analysis",
  "portfolio correlation", "equity curve", "regime detection",
  "rolling metrics", "scorecard", "EA comparison".
---

# Analytics

Research and evaluation guidance for Python-based analysis of MetaTrader
strategy results, trade histories, market data extracts, and experiment runs.

**See also:** For MQL5-based real-time regime classification (ADX/ATR, session
filters, news blocking), see `market-regime` under `mql5-development`. The
Python-based regime detection in `references/rolling-metrics-and-regime-detection.md`
complements that skill by providing post-hoc analysis over historical data.

---

## Purpose

Python-based analytics for MetaTrader trade data: performance metric
computation, portfolio correlation analysis, experiment tracking, rolling
regime detection, and reproducible report generation. Downstream from
execution and data collection.

---

## When to Use

- Analyse MT4 or MT5 backtest outputs in Python
- Compute risk and performance metrics from trades, equity curves, or bar data
- Compare EA variants, symbols, or parameter sets
- Analyse multi-EA portfolios, correlations, and concentration risk
- Build pandas-based scorecards and result summaries
- Prepare trading reports, validation notes, and experiment logs
- Investigate robustness, trade distributions, and regime sensitivity

**Do NOT use** for:
- Direct MT5 terminal integration -> use `python`
- REST execution through mt5-httpapi -> use `httpapi`
- MQL source code or EA coding -> use `ea-architect` or `stdlib-utilities`

---

## Working Model

This skill sits downstream from execution and data collection:

- Data ingestion can come from backtests, MT5 Python scripts, or exported
  trade history
- Analytics code should stay separate from live execution code
- Performance conclusions should be reproducible from stored datasets and
  parameters
- Presentation logic should not redefine the underlying metrics silently

---

## References

| File | Contents | Read when |
|------|----------|-----------|
| `references/data-preparation.md` | Structuring deals, orders, equity curves, candle data; time normalisation; tidy DataFrame preparation | Cleaning or joining raw MT5 export data |
| `references/performance-metrics.md` | Drawdown, Profit Factor, Sharpe, expectancy, Recovery Factor; trade-level and portfolio-level interpretation | Computing or interpreting any trading metric |
| `references/reporting-and-experiments.md` | Scorecards, comparison tables, experiment logging, walk-forward and parameter-set evaluation | Building scorecards; comparing EA variants |
| `references/portfolio-correlation-analysis.md` | Multi-EA aggregation, weighting, correlation, diversification, exposure concentration | Analysing multi-strategy portfolio risk |
| `references/portfolio-recipes.md` | Correlation-matrix pandas workflows, equity-curve merge, allocation/contribution tables | Implementing portfolio analysis in code |
| `references/rolling-metrics-and-regime-detection.md` | Rolling return/volatility/Sharpe/drawdown; regime segmentation by volatility/trend/session; stability checks | Detecting regime changes over time; post-hoc regime analysis |

> For real-time MQL5-based regime classification, see `market-regime`.
