---
name: journal-monitor
description: >
  Parse MT5 terminal journal logs (JournalLog-*.log) and surface execution
  anomalies — connection drops, slow fills, slow SL/TP modifies, failed orders,
  and fast SL hits — across one or many broker accounts. Trigger this skill
  whenever the user asks to analyse, compare, or monitor MT5 journals;
  investigate broker execution quality; compare latency or drops across brokers;
  set up nightly journal monitoring or alerts; debug why an EA performed
  differently on different accounts; or uploads files named
  JournalLog-<account>-<date>.log. Also trigger when the user mentions MT5
  journal logs, broker execution quality, connection drops, slow fills, or fast
  SL hits, even if they do not explicitly say "journal".
---

# MT5 Journal Monitor

Parse MetaTrader 5 terminal journal logs and surface execution anomalies
across one or many broker accounts. Built for algo traders running the same EA
on multiple brokers who want to detect when a broker's execution is degrading
the strategy.

---

## Purpose

Detects broker-level execution problems by parsing MT5 journal logs: connection
drops, slow order fills, slow SL/TP modifications, failed/rejected orders, and
suspiciously fast SL hits. Ships three Python scripts that automate the full
pipeline from parsing to reporting.

---

## When to Use

- Analyse MT5 journal logs from one or many accounts
- Compare broker execution quality (latency, drops, failures) side by side
- Investigate why an EA performs differently on different brokers
- Detect connection instability on a specific VPS-to-broker route
- Find fast SL hits that suggest spread spikes or bad feeds
- Set up nightly monitoring with CSV/JSON exports and optional webhook alerts
- Debug failed or rejected orders (stops-too-close, requotes, off-quotes)

**Do NOT use** for:
- Real-time trade management → use `trade-manager`
- Risk/sizing policy → use `risk-engine`
- EA architecture → use `ea-architect`

---

## Core Guidance

### What It Detects

| Anomaly | Default threshold | Severity |
|---------|-------------------|----------|
| Connection drops | every drop | `warn` |
| Slow pending/market fills | > 100 ms | `warn` (> 1 s = `error`) |
| Slow SL/TP modifies | > 50 ms | `warn` (> 500 ms = `error`) |
| Failed/rejected orders | every failure | `error` |
| Fast SL hits (position round-trip) | <= 30 s | `warn` |

All thresholds are configurable via CLI flags or YAML config.

### Quick Start

The skill ships three Python scripts in `scripts/`:

- `parser.py` — parses MT5 journal files into structured events (UTF-16/UTF-8
  auto-detected, tab-separated)
- `analyzer.py` — consumes parsed events, produces per-account reports with
  latency stats and anomaly lists
- `monitor.py` — end-to-end CLI: reads files/dirs, writes markdown report +
  optional CSV/JSON/webhook

```bash
python scripts/monitor.py \
  --path /path/to/journals \
  --label ACCOUNT_ID_1=BrokerA \
  --label ACCOUNT_ID_2=BrokerB \
  --out ./report.md --csv ./anomalies.csv --json ./summary.json
```

For recurring monitoring use `--config monitor.yaml`. See
`scripts/config.example.yaml` to specify paths, labels, thresholds, and
optional webhook URL.

### How It Works

**Parsing.** MT5 writes one line per event. Files use UTF-16 LE with BOM (most
common) or UTF-8. Dates come from the filename, not the line content. The
parser classifies each line into event types and extracts symbol, order_id,
side, volume, price, duration_ms where present.

**Analysis.** Events are grouped by account. For each account the analyser
computes: drop count and cluster count, latency stats for
pending/modify/cancel/market categories, deal count, failed order count, fast
SL hits via same-symbol opposite-side deals with equal volume within a time
window, and per-symbol breakdowns.

**Output.** Markdown report for humans, CSV for spreadsheet analysis, JSON for
integration. Optional Discord-compatible webhook fires when any `error` anomaly
exists or `warn` count exceeds threshold.

### Common Workflows

**Workflow A — "I uploaded some journal files, what do they show?"**
1. Run `monitor.py --path <upload_dir> --label ...=Broker ...`
2. Read the generated report and summarise the worst 2-3 anomalies per account
3. Offer to present the report file if it's long

**Workflow B — "Compare execution across my brokers"**
1. Gather journal files for the time window of interest
2. Run monitor with labels for every account
3. Emphasise the summary table (cross-broker latency + drop comparison)

**Workflow C — "Set up nightly monitoring"**
1. Ask how journals are collected from their MT5 terminals
2. Point them at `references/collecting_journals.md` for the matching setup
3. Help them populate `monitor.yaml` from `scripts/config.example.yaml`
4. Provide the cron entry and verify by running once manually

**Workflow D — "Extend the detection"**
1. New anomaly types go in `analyzer.py` — add detection in `analyze()`
2. New event classifications go in `parser.py` — extend `_classify()`
3. New output formats go in `monitor.py` — add a CLI flag and write logic

---

## Common Mistakes

- **Misleading pending latency.** The parser distinguishes pending vs market by
  scanning back up to 10 events. If the log is sparse, this can misclassify.
- **Fast SL false positives.** A hedged EA that opens both sides simultaneously
  will trigger false positives. Filter by symbol or increase the time threshold.
- **Connection drops during maintenance.** Normal during broker maintenance
  windows. A healthy broker should have under ~3 drops per week outside those.
- **Mojibake in the report.** If the file is not UTF-16 or UTF-8, the parser
  falls back to Latin-1 which preserves bytes but may garble non-ASCII.

---

## References

| File | Contents | Read when |
|------|----------|-----------|
| `references/journal_format.md` | Detailed line format, key message patterns (pending, deal, modify, cancel, failed, connection, auth), important gotchas | Parsing logic understanding; debugging misclassified events; learning every message pattern |
| `references/collecting_journals.md` | Centralising journals from Wine prefixes, Docker containers, Backtest Manager; rsync scripts; cron entries; retention | Setting up journal collection on Linux; configuring nightly monitoring |
| `scripts/parser.py` | `parse_paths()` → list of `JournalEvent` objects | Core parsing logic |
| `scripts/analyzer.py` | `analyze()` → dict of `AccountReport`; `format_report()` → markdown | Analysis and reporting logic |
| `scripts/monitor.py` | CLI entry point; supports files, dirs, `--days`, labels, thresholds, YAML config, webhook | Running the monitor |
| `scripts/config.example.yaml` | Annotated config template | Creating a production config |
