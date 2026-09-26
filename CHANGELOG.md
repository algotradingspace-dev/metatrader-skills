# Changelog

## [Unreleased]

### Added
- **mql5-docs-lookup** skill in `mql5-development` — how to query the official
  MQL5 reference through the Algo Trading Space MCP tools
  (`platform_search_mql5_docs`, `platform_resolve_mql5_symbol`): when to resolve
  an identifier versus search a phrase, how to cite the canonical `mql5.com` URL,
  how to read each tool error code, and how to answer from the local references
  when the service is unavailable.

## [0.4.0] - 2026-08-19

### Added
- **mql-developer** plugin — MQL4/MQL5 language and API reference vendored
  verbatim from [ThomasPraun/mql-developer](https://github.com/ThomasPraun/mql-developer)
  (MIT), pinned at `3b5e358`. First plugin here covering MQL4 and
  MQL4→MQL5 migration. Vendored rather than sourced via `git-subdir`
  because upstream publishes a bare skill at its repo root, with no
  plugin layout for a subdir source to target.
- `UPSTREAM.json` — manifest of vendored third-party sources (URL, ref,
  pinned commit, license, file mapping)
- `scripts/sync-upstream.mjs` — dependency-free drift check (`check`) and
  re-vendor (`apply`) for every source in the manifest
- **Upstream Sync** workflow — weekly and on-demand drift check that
  re-vendors, validates the marketplace, and opens a review PR when
  upstream moves

## [0.3.0] - 2026-07-31

### Added
- **trading-fundamentals** plugin — forex-fundamentals-reference skill for
  interpreting macro releases (CPI, GDP, NFP, PMI, rate decisions, etc.)
  across USD, EUR, GBP, GER, JPY, CAD, AUD, NZD, CHF, CNY
- **trading-web-systems** plugin — fintech-web-systems skill for
  TypeScript/React trading infrastructure (decimal-safe arithmetic, trading
  metrics, WebSocket market data, OHLCV ingestion)

## [0.2.1] - 2026-07-30

### Fixed
- **.claude-plugin/marketplace.json**: use full git URL for mt5-httpapi
  subdir source (Claude Code requires `https://` not `owner/repo` shorthand)
- **.claude/settings.json**: remove stale `enabledPlugins` block

## [0.2.0] - 2026-07-30

### Added
- **mt5-httpapi** plugin — REST API bridge for MetaTrader 5 trading,
  sourced via git-subdir from psyb0t/mt5-httpapi (no vendoring)
- **metatrader-research** plugin — imported-backtest skill for MT5 HTML
  report parsing and equity reconstruction from uploaded reports

### Changed
- **metatrader-research** description updated to include imported-backtest

## [0.1.1] - 2026-07-28

### Fixed
- CI: install Claude Code CLI before running `claude plugin validate` to
  resolve `claude: command not found` on runner

## [0.1.0] - 2026-07-28

### Added

- **mql5-development** plugin — 10 skills: ea-architect, risk-engine,
  signal-engine, trade-manager, market-regime, multi-asset, stdlib-utilities,
  constants, economic-calendar, network
- **metatrader-platform** plugin — 3 skills: platform, python,
  journal-monitor
- **metatrader-research** plugin — 2 skills: backtest-analysis, analytics
- Marketplace governance: SKILL-STANDARD.md, SCRUB-POLICY.md,
  CONTRIBUTING.md, DISCLAIMER.md, LICENSE, CI validation workflow
- Documentation: MIGRATION.md (legacy→marketplace migration record)
