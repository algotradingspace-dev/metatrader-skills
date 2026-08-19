# mql-developer

Comprehensive MQL4/MQL5 development reference for MetaTrader 4 and 5 —
language syntax for both dialects, OOP and EA architecture patterns,
order/position and risk operations, custom indicators and UI panels,
WebRequest/REST/JSON integration, Strategy Tester and walk-forward
backtesting, code protection and licensing, and MQL4-to-MQL5 migration.

## Usage

```bash
claude plugin install mql-developer@metatrader-skills
```

The skill exposes a routing table in `SKILL.md`; Claude loads only the
reference file relevant to the task (~9,500 lines across 8 references).

## Relationship to `mql5-development`

`mql5-development` is our own opinionated, methodology-first plugin
(EA architecture, risk engine, signal engine, market regime, trade
manager). `mql-developer` is a broad **language and API reference** and is
the only plugin here that covers **MQL4** and MQL4→MQL5 migration. They
overlap by design — prefer `mql5-development` for how to build something,
`mql-developer` for what the language and platform APIs actually provide.

## Vendored — do not edit

Everything under `skills/` and the `LICENSE` in this directory is copied
verbatim from upstream:

> https://github.com/ThomasPraun/mql-developer — MIT, © 2026 Thomas Praun

The pinned commit and file mapping live in
[`UPSTREAM.json`](../../UPSTREAM.json) at the repo root.

**Local edits are overwritten on the next sync and break drift detection.**
To change this content, contribute upstream. To diverge deliberately, fork
upstream and repoint `url` in `UPSTREAM.json`.

### Why vendored instead of a git-subdir source

The `mt5-httpapi` entry uses a `git-subdir` marketplace source because
upstream ships a real plugin layout at `.agents/` (a `.claude-plugin/plugin.json`
plus a `skills/` directory). `mql-developer` publishes a **bare skill** at its
repo root — `SKILL.md` and `references/` with no plugin wrapper — so there is
no path a `git-subdir` source can point at. Vendoring plus a sync check is
the equivalent, and gives us a review gate on upstream changes.

### Syncing

```bash
node ../../scripts/sync-upstream.mjs check
```

See the [root README](../../README.md#vendored-upstream-skills) for the full
workflow. A scheduled GitHub Action runs the check weekly and opens a PR
when upstream moves.

## Conformance note

This skill is third-party content and is **exempt from**
[`docs/SKILL-STANDARD.md`](../../docs/SKILL-STANDARD.md), which governs
skills authored in this repo. It was screened against
[`docs/SCRUB-POLICY.md`](../../docs/SCRUB-POLICY.md) at vendoring time and
contained no broker names, affiliate links, private domains, or
account-specific data. Re-screen on each sync.
