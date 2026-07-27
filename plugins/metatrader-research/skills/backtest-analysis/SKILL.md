---
name: backtest-analysis
description: >
  Backtesting methodology and performance analysis for MQL5 EAs. Use for:
  interpreting backtest metrics (Profit Factor, Sharpe, Calmar, Max DD, Recovery
  Factor); overfitting and curve-fitting detection; walk-forward testing protocol;
  custom OnTester() optimisation criteria; Monte Carlo simulation framework;
  MT5 Strategy Tester configuration (tick modes, modelling, spreads, deposits);
  tester journal patterns; optimisation frames API; full ENUM_STATISTICS reference.
  Trigger: "backtest", "optimise", "walk-forward", "Monte Carlo", "Profit Factor",
  "Sharpe Ratio", "overfitting", "curve fitting", "out of sample",
  "strategy tester", "optimisation criteria", "is this EA prop firm ready",
  "robustness", "OnTester", "TesterStatistics".
---

# Backtest Analysis

Backtesting is hypothesis testing, not validation. Test correctly, interpret
honestly, and avoid the traps that fool most traders.

---

## Purpose

Methodology and interpretation reference for MetaTrader strategy testing —
scoring backtest reports, detecting overfitting, designing walk-forward and
Monte Carlo validation, configuring the MT5 Strategy Tester, and writing
custom optimisation criteria.

---

## When to Use

- Evaluating whether an EA is ready for funded account trading
- Deciding if a backtest result represents real edge or curve-fitting
- Running optimisation in MT5 and needing a better criterion than raw balance
- Designing a validation pipeline
- Looking up a specific `STAT_*` constant or tester configuration option

**Do NOT use** for:
- Writing EA entry/exit logic → use `signal-engine`
- Post-entry trade management → use `trade-manager`
- Performance analytics in Python/pandas → use `analytics`

---

## Core Guidance

### Performance Metric Scorecard

Score any backtest report against this table before drawing conclusions.

```
Metric               Fail      Acceptable   Good       Excellent
Profit Factor (PF)   <1.2      1.2-1.4      1.4-1.7    >1.7
Win Rate (WR)        <35%      35-45%       45-55%     >55%
Sharpe Ratio         <0.5      0.5-0.9      0.9-1.5    >1.5
Calmar Ratio         <0.5      0.5-1.0      1.0-2.0    >2.0
Max Drawdown         >20%      15-20%       10-15%     <10%
Recovery Factor      <1.0      1.0-2.0      2.0-4.0    >4.0
Expected Payoff      <0        0-5          5-15       >15
Total Trades (3yr)   <100      100-200      200-500    >500
Consecutive Losses   >10       8-10         5-7        <5
```

**The 3 metrics that matter most:**
1. **Profit Factor** — PF 1.4+ means earning $1.40 per $1 lost. Under 1.2 is not viable.
2. **Max Drawdown** — must stay inside the firm's hard limit at every point during the test, not just the final figure.
3. **Recovery Factor** — net profit / max DD. Shows recovery efficiency. Target 2.0+ for funded accounts.

### Overfitting Detection Checklist

**Red flags:**
- Backtest PF >3.0 but forward test PF <1.2
- Only one narrow parameter range works (sharp peak on optimisation map)
- Performance collapses outside the tested date range
- WR >70% with very tight SL
- <200 trades in a 3-year test period
- Strategy only works on one specific tick feed
- Results change dramatically with 1-pip spread increase
- All profits from a 2-week period

**Green flags:**
- Stable PF across broad parameter ranges (flat optimisation map)
- Out-of-sample last 12 months show similar metrics to in-sample
- Walk-forward efficiency >70%
- Monte Carlo 95th percentile drawdown < firm limit
- Works on multiple similar symbols with similar parameters
- Performance consistent across different market regimes
- PF is similar for buy-only and sell-only independently

### Walk-Forward Testing Protocol

```
Total data:      5 years minimum (e.g. 2019-2024)
In-sample (IS):  First 3 years — optimise parameters here
Out-of-sample:   Next 1 year — validate only, do not touch
Forward test:    Final year — treated as live proxy

WF Efficiency = Average OOS PF / Average IS PF
  > 0.85  = Excellent
  0.70-0.85 = Acceptable
  0.50-0.70 = Marginal — likely overfit
  < 0.50  = Reject
```

### Monte Carlo Simulation Framework

Run 1,000 simulations before live deployment:

1. **Sequence shuffle** — randomly reorder trades
2. **Trade skip** — randomly skip 10% of trades (missed signals)
3. **Result noise** — adjust each trade result by +/-20% (slippage)

```
Required outputs:
  95th percentile Max DD   -> must be < firm limit
  5th percentile Net Profit -> must still be positive
  Probability of ruin       -> P(DD > hard limit) must be < 5%

Tools:
  MT5 built-in Monte Carlo (optimisation results tab)
  Quant Analyzer (standalone)
  Manual: export trades to CSV, run in Python/Excel
```

---

## Code Patterns

### Custom Optimisation Criterion (OnTester)

```mql5
double OnTester() {
   double pf             = TesterStatistics(STAT_PROFIT_FACTOR);
   double maxDD          = TesterStatistics(STAT_EQUITY_DD);
   double netProfit      = TesterStatistics(STAT_PROFIT);
   double totalTrades    = TesterStatistics(STAT_TRADES);
   double sharpe         = TesterStatistics(STAT_SHARPE_RATIO);
   double recoveryFactor = TesterStatistics(STAT_RECOVERY_FACTOR);
   double balance        = TesterStatistics(STAT_INITIAL_DEPOSIT)
                         + TesterStatistics(STAT_PROFIT);

   if(totalTrades < 100)   return 0;
   if(pf < 1.1)            return 0;
   if(netProfit <= 0)      return 0;
   if(maxDD > balance * 0.08) return 0;  // exceed configurable DD limit

   double ddPenalty = 1.0 - (maxDD / (balance * 0.08));
   double score     = pf * recoveryFactor * sharpe * ddPenalty;
   double tradeBonus = MathMin(totalTrades / 500.0, 1.0);
   return score * (0.8 + 0.2 * tradeBonus);
}
```

---

## Common Mistakes

- Running "Open Prices Only" and missing intrabar SL hits
- Not including commission — always include $5-8/lot round-trip
- Testing on a single year with one market regime
- Accepting the first optimisation pass without OOS validation
- Using `ACCOUNT_BALANCE` for DD limits instead of equity
- Full Kelly instead of half-Kelly
- Not resetting daily drawdown limits on a new trading day

---

## References

| File | Contents | Read when |
|------|----------|-----------|
| `references/tester-configuration.md` | Tick generation modes, execution delay, forward period, spread/deposit/leverage config, common mistakes | Setting up a Strategy Tester run; choosing tick mode |
| `references/metric-definitions.md` | Drawdown types (balance vs equity DD, absolute/maximal/relative), Profit Factor, Recovery Factor, Sharpe, History Quality | Interpreting the Results tab; understanding MT5 metric calculations |
| `references/historical-data.md` | Pre-start buffer requirements per timeframe, start date shift journal message, tick/history storage paths, multi-currency setup | Fixing "start time changed" warnings; preparing data for a test |
| `references/optimization-modes.md` | Slow/Genetic/All Symbols types, genetic algorithm internals, optimisation criteria (Balance/PF/DD/Sharpe/Custom/Complex), forward behaviour | Choosing optimisation method; selecting the right criterion |
| `references/tick-generation.md` | Every Tick algorithm, Open Prices Only limits, Real Ticks specifics, exchange instrument order triggering, spread handling | Understanding tick modelling accuracy; debugging tick-related anomalies |
| `references/tester-journal-agents.md` | Journal message patterns, local/remote/cloud agent architecture, agent limitations, global variables during tests | Interpreting tester journal output; configuring remote/cloud agents |
| `references/optimization-frames-api.md` | FrameAdd/FrameNext/FrameFilter, ParameterSetRange, controller pattern, MQL5 Cloud limits, full function reference | Passing custom data from test agents to controller; dynamic parameter ranges |
| `references/enum-statistics.md` | Full `ENUM_STATISTICS` table — all `STAT_*` constants with types and descriptions | Looking up `TesterStatistics()` constants for `OnTester()` or frame output |
