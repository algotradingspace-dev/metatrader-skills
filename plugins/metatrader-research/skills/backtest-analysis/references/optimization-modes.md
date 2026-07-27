# Optimisation Modes and Criteria

## Three Optimisation Types

| Type | Description | Best For |
|------|-------------|----------|
| Slow Complete Algorithm | All combinations exhaustively | Small parameter space, final validation |
| Fast Genetic Algorithm | Evolutionary search, population 64-256 | Large parameter space, initial exploration |
| All Symbols in Market Watch | Same parameters, different symbols | Robustness check across instruments |

## Genetic Algorithm Internals

```
Runs = Population Size * (Unconditional generations + Convergence generations)
Population: 64-256 (based on combination count)
Unconditional generations: 15-31
Convergence generations: unconditional_generations / 3
Auto-starts when combinations > 1,000,000 (32-bit) or > 100,000,000 (64-bit)
Cache: platform_data\tester\cache\*.gen — survives power failure, resumes from last generation
```

## Optimisation Criteria (Genetic Mode Only)

| Criterion | Description |
|-----------|-------------|
| Balance max | Maximise final balance (chases equity, ignores risk) |
| Profit Factor max | Maximise PF (good proxy for edge quality) |
| Expected Payoff max | Maximise avg profit/trade |
| Drawdown min | Minimise relative balance DD% |
| Recovery Factor max | Maximise net profit / max DD |
| Sharpe Ratio max | Maximise risk-adjusted return |
| Custom max | Use return value of `OnTester()` — preferred for prop-firm criteria |
| Complex Criterion | Composite score across Trades, DD, Recovery, Payoff, Sharpe |

**Which criterion to use:**
- Use **Custom max** with your own `OnTester()` function for any serious optimisation
- Use **Complex Criterion** when you don't have a custom function yet
- Never use **Balance max** alone — it ignores drawdown entirely

## Forward Optimisation Behaviour

- Top **10%** of in-sample passes (full search) or **25%** (genetic) are retested on forward period
- Compare "Optimisation Results" vs "Forward Results" tabs — degradation > 30% is a red flag
