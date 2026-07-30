# Changelog

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
