# Migration Plan

Scanned `legacy/` — 17 unique skill packages (1 duplicate), 42 `.md` files.
Mapping each to its target plugin per `docs/SKILL-STANDARD.md`.

---

## Migration Table

| source path | target plugin | target skill name | SKILL.md lines | refs/ lines | needs refs/ split | internal refs found | notes |
|---|---|---|---|---|---|---|---|
| `legacy/metatrader/metatrader-core/` | metatrader-platform | core | 16 | 631 | N | `openclaw-live-trading.md:46` — "hardcoded named prop-firm account and port" | DEPRECATED. Content folded into platform skill (see §5). Archive after review. |
| `legacy/metatrader/metatrader-analytics/` | metatrader-research | analytics | 68 | 845 | N | — | **MIGRATED.** SKILL.md rewritten with trigger phrases. 6 ref files preserved. Cross-reference to market-regime added. |
| `legacy/metatrader/metatrader-httpapi/` | — | — | 482 | 321 | N | `SKILL.md:93` — "RoboForex/FTMO = UTC+3, TeleTrade = UTC+2"; `setup.md:42` — `server: "RoboForex-Pro"` | **NOT MIGRATED.** Superseded by upstream psyb0t/mt5-httpapi. Bucket A (~580 lines of endpoint docs and setup) discarded as upstream-owned. Bucket B (~12 lines, Live Trading Safety principles) redistributed to risk-engine/references/live-execution-safety.md. Bucket C: none. |
| `legacy/metatrader/metatrader-platform/` | metatrader-platform | platform | 935 | 1394 | Y | `SKILL.md:138` — non-official download URL | **MIGRATED.** SKILL.md 40 lines (Reference variant). 14 ref files. See §5 for core fold-in report. |
| `legacy/metatrader/metatrader-python/` | metatrader-platform | python | 61 | 1179 | N | — | **MIGRATED.** SKILL.md rewritten with trigger phrases. 5 ref files preserved. |
| `legacy/metatrader/mt5-journal-monitor/` | metatrader-platform | journal-monitor | 144 | 286 | N | `journal_format.md:90` — real account ID and order ticket; `:106` — real broker server name; `:115` — real client IP; `:116` — real broker legal name | **MIGRATED.** SKILL.md 152 lines (standard variant). 2 ref files scrubbed. 4 scripts (931 lines) migrated with scrubbed examples. |
| `legacy/mql5-ea/mql5-backtest-analysis/` | metatrader-research | backtest-analysis | 644 | 367 | Y | `SKILL.md:12` — "prop firm ready"; `:43` — "prop firm hard limit"; `:81` — "prop firm limit"; `:134` — "($10,000 for FTMO standard)"; `:135` — "(1:100 typical for prop firms)"; `:463` — "prop firm limit"; `:473` — "safe for FTMO standard ($10K)"; `:634` — "prop firm readiness" | **MIGRATED.** SKILL.md 181 lines (standard variant). 8 ref files. Prop-firm refs genericised per SCRUB-POLICY Rule 3: "FTMO standard" -> "funded account size", "1:100 typical for prop firms" -> "common: 1:30-1:100", "safe for FTMO standard" -> "safe for a 10% total-DD firm". |
| `legacy/mql5-ea/mql5-constants/` | mql5-development | constants | 733 | 670 | Y | — | **MIGRATED.** SKILL.md 63 lines (Reference variant). 9 ref files. Tables moved verbatim — no rows dropped or abbreviated. Frontmatter rewritten for lookup triggers. |
| `legacy/mql5-ea/mql5-ea-architect/` | mql5-development | ea-architect | 1224 | 946 | Y | — | **MIGRATED.** SKILL.md 297 lines (standard variant). 11 ref files. Frontmatter rewritten for trigger quality. |
| `legacy/mql5-ea/mql5-economic-calendar/` | mql5-development | economic-calendar | 80 | 0 | N | — | **MIGRATED.** Single-file Reference variant. Description rewritten with calendar API trigger phrases. |
| `legacy/mql5-ea/mql5-market-regime/` | mql5-development | market-regime | 421 | 0 | N | — | **MIGRATED.** Single-file skill. Description rewritten. Cross-reference to analytics skill added. |
| `legacy/mql5-ea/mql5-multi-asset/` | mql5-development | multi-asset | 389 | 0 | N | — | **MIGRATED.** Single-file skill. Description rewritten. |
| `legacy/mql5-ea/mql5-network/` | mql5-development | network | 99 | 0 | N | — | **MIGRATED.** Single-file Reference variant. Description rewritten with lookup triggers. |
| `legacy/mql5-ea/mql5-risk-engine/` | mql5-development | risk-engine | 506 | 246 | Y | `SKILL.md:6` — "prop firm rule sets (FTMO, MFF, E8, TFT)"; `:9` — "prop firm, FTMO"; `:190-193` — prop firm DD table (FTMO, MFF, E8, TFT); `:195` — "FTMO-safe configuration"; `:197` — "// Stays 1% below FTMO's 5% hard limit"; `:201` — "prop firm rules"; `:496` — "prop firm"; `:503` — "prop firm challenge" | **MIGRATED.** SKILL.md 263 lines (standard variant). 4 ref files. CHUNK 4 refactored per SCRUB-POLICY Rule 3: PropFirmRules struct, no firm names in code, presets isolated to refs/prop-firm-presets.md with dated header. |
| `legacy/mql5-ea/mql5-signal-engine/` | mql5-development | signal-engine | 835 | 561 | Y | — | **MIGRATED.** SKILL.md 259 lines (standard variant). 10 ref files. Frontmatter rewritten. |
| `legacy/mql5-ea/mql5-stdlib-utilities/` | mql5-development | stdlib-utilities | 694 | 535 | Y | — | **MIGRATED.** SKILL.md 69 lines (Reference variant). 14 ref files. Frontmatter rewritten. |
| `legacy/mql5-ea/mql5-trade-manager/` | mql5-development | trade-manager | 978 | 696 | Y | `SKILL.md:974` — "Tuning management parameters for prop firm pass rates" | **MIGRATED.** SKILL.md 239 lines (standard variant). 10 ref files. Frontmatter rewritten. "prop firm" kept in trigger text per SCRUB-POLICY Rule 3. |
| `legacy/mql5-ea/mt5-journal-monitor/` | — | — | 144 | 287 | N | Same as `metatrader/mt5-journal-monitor/` above | **EXACT DUPLICATE** of `metatrader/mt5-journal-monitor/`. Do not migrate. |

---

## 1. Proposed Migration Order

### Phase 1 — Foundation (no dependencies)

| Order | Skill | Plugin | Rationale |
|-------|-------|--------|-----------|
| 1 | ea-architect | mql5-development | Defines 5-layer EA structure; all other MQL5 skills reference it |
| 2 | stdlib-utilities | mql5-development | Language/runtime utils; other MQL5 skills depend on patterns here |
| 3 | platform | metatrader-platform | Base platform knowledge: installation, config, filesystem |
| 4 | backtest-analysis | metatrader-research | MT5 Tester config is prerequisite for analytics |

### Phase 2 — Build

| Order | Skill | Plugin | Rationale |
|-------|-------|--------|-----------|
| 5 | risk-engine | mql5-development | Layer 1 — position sizing, DD guards |
| 6 | signal-engine | mql5-development | Layer 2 — entry/exit logic |
| 7 | market-regime | mql5-development | Layer 2 — filters signals |
| 8 | multi-asset | mql5-development | Depends on risk-engine concepts |
| 9 | trade-manager | mql5-development | Layer 4 — post-entry management |
| 10 | constants | mql5-development | Standalone reference |

### Phase 3 — Integration

| Order | Skill | Plugin | Rationale |
|-------|-------|--------|-----------|
| 11 | economic-calendar | mql5-development | Standalone API reference |
| 12 | network | mql5-development | Standalone API reference |
| 13 | python | metatrader-platform | Depends on platform terminal setup |
| 14 | httpapi | metatrader-platform | Depends on platform terminal setup |
| 15 | journal-monitor | metatrader-platform | Depends on platform + python concepts |
| 16 | analytics | metatrader-research | Depends on backtest-analysis (reads its outputs) |

### Phase 4 — Deprecation & Cleanup

| Order | Skill | Plugin | Rationale |
|-------|-------|--------|-----------|
| 17 | core | metatrader-platform | Absorb remaining content into platform, then archive |
| 18 | (duplicate) | — | Delete `mql5-ea/mt5-journal-monitor/` after confirming identical |

---

## 2. Skills Recommended Against Publishing

### Do not publish: `metatrader-core`

SKILL.md frontmatter explicitly says **DEPRECATED** — "use metatrader-platform or mql5-stdlib-utilities instead." Its 6 reference files (631 lines) cover platform setup, internals, security, account management, and keyboard shortcuts — all already covered by `metatrader-platform`. Before archiving, check `references/openclaw-live-trading.md` for any content not yet in the platform skill; fold it in, then drop the rest.

### Do not publish (as standalone skill): `mql5-constants`

732 lines of pure `ENUM_*` value tables and property identifier catalogs. It is a **reference**, not a skill in the SKILL-STANDARD sense — it has no "Core guidance", "Code patterns", or "Common mistakes" sections. Rather than force it into an ill-fitting template, consider publishing it as `plugins/mql5-development/references/constants.md` or as a single plugin-level reference. If kept as a skill, either add proper sections or restructure it.

### Do not publish: duplicate `mql5-ea/mt5-journal-monitor`

Exact content copy of `metatrader/mt5-journal-monitor/`. Keep the original under metatrader-platform, delete the redundant copy.

---

## 3. Overlap — Candidate Merges

| Skill A | Skill B | Overlap | Recommendation |
|---------|---------|---------|----------------|
| `metatrader-platform` (935 lines) | `core` (16+631 lines, deprecated) | Platform setup, internals, security, keyboard shortcuts, account mgmt — all duplicated | Absorb core refs into platform's new `references/` after split. Do not keep core as a separate skill. |
| `market-regime` (421 lines, MQL5) | `analytics` refs/rolling-metrics-and-regime-detection.md (158 lines, Python) | Both describe regime detection (trend/range, volatility). MQL5 gates trades; Python does post-hoc analysis. | Keep separate — different implementation domain (dev vs research). Add cross-reference in both SKILL.md References sections. |

---

## 4. Scrub Summary Before Publishing

All 17 packages must pass through this filter before migration:

- [x] non-official download mirror URL in platform skill → replaced with `<official-mt5-linux-installer-url>` placeholder
- [x] `openclaw-live-trading.md` — "FTMO challenge account" -> "prop firm challenge account"
- [x] risk-engine CHUNK 4: firm names removed from code; presets isolated to `references/prop-firm-presets.md` with dated header. `PropFirmRules` struct uses generic fields
- [x] backtest-analysis: "FTMO standard" -> "funded account size", "1:100 typical for prop firms" -> "common: 1:30-1:100", "safe for FTMO standard ($10K)" -> "safe for a 10% total-DD firm". Generic "prop firm" terms kept.
- [ ] Replace `RoboForex`, `TeleTrade` with generic examples in 1 file (httpapi)
- [ ] Scrub real account ID, order ticket, client IP, broker server name, and broker legal name from both copies of `journal_format.md`
- [ ] Verify no `help.algotradingspace.com`, `github.com/algotradingspace-dev/`, or affiliate links (none found, but re-check on migration)

---

## 5. Platform Migration — Core Fold-In Report

metatrader-core was recovered from `git show HEAD~1:` and compared against
the new `plugins/metatrader-platform/skills/platform/references/`.

### `platform-setup.md`
- **Folded in:** Wine version check (log example), SSE2 CPU requirement,
  silent install `/auto` switch example, uninstallation section, CLI switch
  table expanded, data paths summary table by OS
- **Discarded as duplicate:** Windows/macOS/Linux install steps (already in
  PS-1 with same detail), portable mode description, main mode data directories
- **Scrubbed:** non-official download mirror URL → `<official-mt5-linux-installer-url>`

### `security-auth.md`
- **Folded in:** Certificate transfer steps (export/transfer/import to new
  machine), desktop setup step-by-step, iPhone/Android detailed setup flows,
  compatible authenticator apps list (includes MT5 mobile app), OTP fund
  transfer note, "Bind to account" unbind process
- **Discarded as duplicate:** SSL architecture, certificate file naming, 2FA
  30-second window, encryption details, platform-level security measures

### `platform-internals.md`
- **Folded in:** Bases subdirectories (alerts, favorites, hotkeys, request-queues),
  crash dump file naming pattern (`yyyymmdd_hhmmss.dmp`), `interface.dat` and
  `servers.dat` in Config, log entry fields table, journal commands table,
  Task Manager header stats (thread count, handle count, RAM consumed), MQL5
  Programs management (Show/Properties/Remove), manual updates section
- **Discarded as duplicate:** file tree structure (overlaps but core had more
  detail — folded the extra branches), log types, Task Manager thread types,
  Live Update process

### `account-management.md`
- **Folded in:** Account type table (demo vs live), account operations table
  (open/connect/change password/delete/favorites/hosting), safety settings
  detail ("Disable automated trading when switching accounts"), mailbox
  attachment limits table, transfer process steps broken out
- **Discarded as duplicate:** fund transfer constraints, switching accounts

### `keyboard-shortcuts.md`
- **Folded in:** All 19 shortcuts from core not present in the original PS-6
  selection — notably Ctrl+M (Task Manager), Ctrl+E (EA properties), Ctrl+G
  (chart list), Ctrl+H (arrange indicators), Ctrl+B (objects list), Ctrl+L/V
  (OHLC/volume toggle), Ctrl+Y (period separators), Home/End (chart
  navigation), Data Window section, Toolbox section (10 entries), full
  Navigator section
- **Discarded as duplicate:** subset that was already in PS-6

### `openclaw-live-trading.md`
- **Folded in:** ALL 132 lines — completely new content not present in
  source SKILL.md (had only a routing entry). Full prompt patterns,
  separation of concerns, task structure, account routing, metadata
  conventions, safety defaults, Python integration boundary
- **Scrubbed:** "hardcoded named prop-firm account and port" →
  "Use the prop firm challenge account" (generalized per SCRUB-POLICY Rule 2)

### Summary

| Core reference | Lines | Folded in | Duplicate | Scrubbed |
|----------------|-------|-----------|-----------|----------|
| `platform-setup.md` | 139 | ~30 lines | ~109 lines | 1 URL |
| `security-auth.md` | 93 | ~50 lines | ~43 lines | 0 |
| `platform-internals.md` | 181 | ~50 lines | ~131 lines | 0 |
| `account-management.md` | 70 | ~25 lines | ~45 lines | 0 |
| `keyboard-shortcuts.md` | 99 | ~80 lines | ~19 lines | 0 |
| `openclaw-live-trading.md` | 132 | 132 lines | 0 lines | 1 brand name |
| **Total** | **714** | **~367 lines** | **~347 lines** | **2** |

---

## 6. Future Skills — Not Present in Legacy

The following operational knowledge exists only as tribal knowledge and has no
legacy source file. These should be authored fresh when needed:

- **Fleet routing and multi-terminal operations** — mapping ports to broker
  accounts, managing N terminals under Docker/QEMU, nginx sidecar routing,
  MT5 instance lifecycle (install, credential injection, health monitoring,
  restarts), cross-terminal trade coordination
- **Backtest Manager integration patterns** — orchestrating the backtest API
  across a fleet, queuing strategies, collecting results, managing `assets/`
  expert and set file pools
- **Wickworks TA sidecar deployment** — configuring the server-side TA stack,
  indicator catalog versioning, resource constraints per VM
