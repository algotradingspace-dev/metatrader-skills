# MetaTrader Skills

A curated marketplace of **Claude Code agent skills** for MetaTrader 4/5
and MQL5 development. Each plugin bundles structured expertise that makes
Claude Code proficient in trading-specific domains — from EA architecture
and risk management to platform automation and backtest analytics.

## Quick start

Add the marketplace once, then install plugins from it. `claude plugin install`
takes one plugin at a time, written `<plugin>@metatrader-skills`.

```bash
# 1. Add the marketplace
claude plugin marketplace add algotradingspace-dev/metatrader-skills

# 2. Install the plugins you want
claude plugin install mql5-development@metatrader-skills
claude plugin install mql-developer@metatrader-skills
claude plugin install metatrader-platform@metatrader-skills
claude plugin install metatrader-research@metatrader-skills
claude plugin install mt5-httpapi@metatrader-skills
claude plugin install trading-fundamentals@metatrader-skills
claude plugin install trading-web-systems@metatrader-skills
```

To install all of them in one go:

```bash
# macOS / Linux
for p in mql5-development mql-developer metatrader-platform metatrader-research \
         mt5-httpapi trading-fundamentals trading-web-systems; do
  claude plugin install "$p@metatrader-skills"
done
```

```bat
:: Windows Command Prompt (use %%p instead of %p inside a .bat file)
for %p in (mql5-development mql-developer metatrader-platform metatrader-research mt5-httpapi trading-fundamentals trading-web-systems) do claude plugin install %p@metatrader-skills
```

```powershell
# Windows PowerShell
"mql5-development","mql-developer","metatrader-platform","metatrader-research","mt5-httpapi","trading-fundamentals","trading-web-systems" | ForEach-Object { claude plugin install "$_@metatrader-skills" }
```

Notes:

- Add `--scope user` (every project), `--scope project` or `--scope local` to
  choose where a plugin is installed.
- `mt5-httpapi` installs but declares settings it needs, one of them required.
  Set them with `/plugin configure mt5-httpapi@metatrader-skills` inside Claude
  Code, or pass `--config KEY=VALUE` to `claude plugin install`.
- `claude plugin list` shows what is installed. If a marketplace ever reports
  "already added", run `claude plugin marketplace list` to see what is really
  registered, and `claude plugin marketplace update metatrader-skills` to refresh it.
- Working from a local checkout of this repository? Register it with
  `claude plugin marketplace add ./` from the repo root, then use the same
  `claude plugin install <plugin>@metatrader-skills` commands.

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
