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
claude plugin install ./plugins/mql-developer
claude plugin install ./plugins/metatrader-platform
claude plugin install ./plugins/metatrader-research
claude plugin install ./plugins/trading-fundamentals
claude plugin install ./plugins/trading-web-systems
```

## Available plugins

| Plugin | Description |
|--------|-------------|
| [mql5-development](./plugins/mql5-development) | EA architecture, risk engine, signal generation, market regime, trade management |
| [mql-developer](./plugins/mql-developer) | MQL4 **and** MQL5 language/API reference, indicators & UI, migration (vendored from ThomasPraun/mql-developer) |
| [metatrader-platform](./plugins/metatrader-platform) | MT4/5 platform ops, Python API, journal monitoring |
| [mt5-httpapi](./plugins/mt5-httpapi) | HTTP API bridge for MetaTrader 5 (git-subdir from psyb0t/mt5-httpapi) |
| [metatrader-research](./plugins/metatrader-research) | Backtest methodology, performance analytics, experiment tracking |
| [trading-fundamentals](./plugins/trading-fundamentals) | Forex macro fundamentals reference (CPI, NFP, GDP, PMI, rate decisions) |
| [trading-web-systems](./plugins/trading-web-systems) | TypeScript/React fintech engineering, WebSocket market data, trading dashboards |

## Adding skills

See [CONTRIBUTING.md](./CONTRIBUTING.md) and the
[SKILL-STANDARD.md](./docs/SKILL-STANDARD.md) authoring contract.

## Vendored upstream skills

Third-party skills that do not ship a plugin layout are **vendored** —
copied verbatim into `plugins/<name>/skills/` and pinned to an upstream
commit in [`UPSTREAM.json`](./UPSTREAM.json). Vendored files are never
edited locally; edits are overwritten on sync and break drift detection.

```bash
# Report drift against the pinned upstream commits (exit 1 if drifted)
node scripts/sync-upstream.mjs check

# Re-vendor and re-pin, then review the diff before committing
node scripts/sync-upstream.mjs apply
```

The [Upstream Sync](./.github/workflows/upstream-sync.yml) workflow runs
`check` every Monday (and on demand via **Run workflow**). When upstream
moves it re-vendors, validates the marketplace, and opens a PR on
`chore/upstream-sync` for review — so upstream changes land as a reviewed
diff rather than silently.

Skills that *do* ship a plugin layout upstream — currently `mt5-httpapi` —
are wired with a `git-subdir` marketplace source instead and need no
vendoring or sync.

Vendored content is exempt from [SKILL-STANDARD.md](./docs/SKILL-STANDARD.md)
but must be screened against [SCRUB-POLICY.md](./docs/SCRUB-POLICY.md) on
every sync.

## License

MIT — see [LICENSE](./LICENSE).

## Disclaimer

Educational purposes only. No financial advice. See [DISCLAIMER.md](./DISCLAIMER.md).
