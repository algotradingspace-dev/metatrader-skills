# MetaTrader Skills

A curated marketplace of **Claude Code agent skills** for MetaTrader 4/5
and MQL5 development. Each plugin bundles structured expertise that makes
Claude Code proficient in trading-specific domains — from EA architecture
and risk management to platform automation and backtest analytics.

## Quick start

```bash
# Install all plugins
claude plugin install . --all

# Or install individual plugins
claude plugin install ./plugins/mql5-development
claude plugin install ./plugins/metatrader-platform
claude plugin install ./plugins/metatrader-research
claude plugin install ./plugins/trading-fundamentals
```

## Available plugins

| Plugin | Description |
|--------|-------------|
| [mql5-development](./plugins/mql5-development) | EA architecture, risk engine, signal generation, market regime, trade management |
| [metatrader-platform](./plugins/metatrader-platform) | MT4/5 platform ops, Python API, journal monitoring |
| [mt5-httpapi](./plugins/mt5-httpapi) | HTTP API bridge for MetaTrader 5 (git-subdir from psyb0t/mt5-httpapi) |
| [metatrader-research](./plugins/metatrader-research) | Backtest methodology, performance analytics, experiment tracking |
| [trading-fundamentals](./plugins/trading-fundamentals) | Forex macro fundamentals reference (CPI, NFP, GDP, PMI, rate decisions) |

## Adding skills

See [CONTRIBUTING.md](./CONTRIBUTING.md) and the
[SKILL-STANDARD.md](./docs/SKILL-STANDARD.md) authoring contract.

## License

MIT — see [LICENSE](./LICENSE).

## Disclaimer

Educational purposes only. No financial advice. See [DISCLAIMER.md](./DISCLAIMER.md).
