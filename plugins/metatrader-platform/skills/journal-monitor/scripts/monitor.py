#!/usr/bin/env python3
"""MT5 Journal Monitor — main CLI entrypoint.

Usage examples:

  # Analyze all journals in a directory, write a markdown report
  python monitor.py --path ./journals --out ./report.md

  # Same, with CSV of anomalies and JSON summary
  python monitor.py --path ./journals --out ./report.md --csv ./anomalies.csv --json ./summary.json

  # Label accounts with broker names (for readable reports)
  python monitor.py --path ./journals --out ./report.md \\
      --label ACCOUNT_ID_1=BrokerA --label ACCOUNT_ID_2=BrokerB

  # Only analyze files from the last 2 days (by filename date)
  python monitor.py --path ./journals --days 2 --out ./report.md

  # Set custom thresholds
  python monitor.py --path ./journals --slow-fill-ms 50 --slow-modify-ms 25 --fast-sl-seconds 60

  # Push alerts to a Discord/generic webhook
  python monitor.py --path ./journals --webhook https://discord.com/api/webhooks/... \\
      --alert-threshold 5

  # Read from a config file instead of flags (see config.example.yaml)
  python monitor.py --config ./monitor.yaml

Runs nightly via cron:

  0 2 * * *  cd /home/user/mt5-monitor && python monitor.py --config monitor.yaml
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from urllib import request as urlrequest
from urllib.error import URLError

# Add script directory to path so parser/analyzer imports resolve
sys.path.insert(0, str(Path(__file__).parent))

from parser import parse_paths, parse_file, FILENAME_RE  # noqa: E402
from analyzer import (  # noqa: E402
    analyze, format_report, anomalies_to_rows, AccountReport,
)


def _gather_files(paths: list[Path], days: int | None) -> list[Path]:
    """Expand directories, filter by filename date if requested."""
    files: list[Path] = []
    cutoff = None
    if days is not None:
        cutoff = (datetime.now() - timedelta(days=days)).date()

    for p in paths:
        if p.is_dir():
            files.extend(sorted(p.glob("JournalLog-*.log")))
        elif p.is_file():
            files.append(p)

    if cutoff:
        filtered = []
        for f in files:
            m = FILENAME_RE.search(f.name)
            if not m:
                continue
            file_date = datetime.strptime(m.group("date"), "%Y%m%d").date()
            if file_date >= cutoff:
                filtered.append(f)
        files = filtered

    return files


def _load_config(path: Path) -> dict:
    """Load YAML or JSON config file."""
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in (".yaml", ".yml"):
        try:
            import yaml  # type: ignore
        except ImportError:
            raise SystemExit(
                "PyYAML is required to read YAML config. "
                "Install with: pip install pyyaml"
            )
        return yaml.safe_load(text) or {}
    if path.suffix.lower() == ".json":
        return json.loads(text)
    raise SystemExit(f"Unsupported config format: {path.suffix}")


def _severity_counts(reports: dict[str, AccountReport]) -> dict[str, int]:
    counts = {"info": 0, "warn": 0, "error": 0}
    for r in reports.values():
        for a in r.anomalies:
            counts[a.severity] = counts.get(a.severity, 0) + 1
    return counts


def _should_alert(reports: dict[str, AccountReport], threshold: int) -> bool:
    counts = _severity_counts(reports)
    return counts["error"] > 0 or counts["warn"] >= threshold


def _format_webhook_message(
    reports: dict[str, AccountReport],
    labels: dict[str, str],
) -> str:
    """Short, channel-ready text for Discord / generic webhook."""
    lines = ["**MT5 Monitor Alert**"]
    for acc, r in sorted(reports.items()):
        label = labels.get(acc, acc)
        errors = sum(1 for a in r.anomalies if a.severity == "error")
        warns  = sum(1 for a in r.anomalies if a.severity == "warn")
        if errors == 0 and warns == 0 and r.drops == 0:
            continue
        lines.append(
            f"\u2022 `{label}` \u2014 {r.drops} drops, {r.failed_orders} failed, "
            f"{r.fast_sl_hits} fast-SL, {errors} errors, {warns} warnings"
        )
    return "\n".join(lines) if len(lines) > 1 else ""


def _post_webhook(url: str, content: str) -> bool:
    """POST a Discord-compatible payload to a webhook URL."""
    payload = json.dumps({"content": content}).encode("utf-8")
    req = urlrequest.Request(
        url, data=payload,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urlrequest.urlopen(req, timeout=10) as resp:
            return 200 <= resp.status < 300
    except URLError as e:
        print(f"[webhook] POST failed: {e}", file=sys.stderr)
        return False


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="mt5-journal-monitor",
        description="Analyze MT5 journal logs and surface anomalies.",
    )
    parser.add_argument("--config", type=Path,
                        help="YAML/JSON config file (overridden by CLI flags)")
    parser.add_argument("--path", type=Path, action="append", default=[],
                        help="Journal file or directory (repeatable)")
    parser.add_argument("--days", type=int,
                        help="Only include files from the last N days")
    parser.add_argument("--out", type=Path, default=Path("./mt5-report.md"),
                        help="Markdown report output path")
    parser.add_argument("--csv", type=Path,
                        help="Anomalies CSV output path")
    parser.add_argument("--json", type=Path, dest="json_out",
                        help="Summary JSON output path")
    parser.add_argument("--label", action="append", default=[],
                        help="Account label, e.g. ACCOUNT_ID=BrokerName (repeatable)")
    parser.add_argument("--slow-fill-ms", type=float, default=100.0)
    parser.add_argument("--slow-modify-ms", type=float, default=50.0)
    parser.add_argument("--fast-sl-seconds", type=int, default=30)
    parser.add_argument("--webhook", type=str,
                        help="Discord-compatible webhook URL")
    parser.add_argument("--alert-threshold", type=int, default=5,
                        help="Warning count that triggers a webhook alert")
    parser.add_argument("--quiet", action="store_true",
                        help="Suppress stdout")
    args = parser.parse_args(argv)

    cfg: dict = {}
    if args.config:
        cfg = _load_config(args.config)

    paths = [Path(p) for p in (cfg.get("paths") or [])] + list(args.path)
    if not paths:
        parser.error("at least one --path or config 'paths' entry required")

    days = args.days if args.days is not None else cfg.get("days")
    files = _gather_files(paths, days)
    if not files:
        print("No journal files found.", file=sys.stderr)
        return 2

    # Labels
    labels: dict[str, str] = dict(cfg.get("labels") or {})
    for s in args.label:
        if "=" in s:
            k, v = s.split("=", 1)
            labels[k.strip()] = v.strip()

    events = parse_paths(files)
    if not args.quiet:
        print(f"[monitor] Parsed {len(events)} events from {len(files)} file(s)")

    reports = analyze(
        events,
        slow_fill_ms=args.slow_fill_ms,
        slow_modify_ms=args.slow_modify_ms,
        fast_sl_seconds=args.fast_sl_seconds,
    )

    # Markdown report
    md = format_report(reports, account_labels=labels)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(md, encoding="utf-8")
    if not args.quiet:
        print(f"[monitor] Wrote markdown report -> {args.out}")

    # CSV of anomalies
    if args.csv:
        rows = anomalies_to_rows(reports)
        args.csv.parent.mkdir(parents=True, exist_ok=True)
        if rows:
            fieldnames = sorted({k for row in rows for k in row.keys()})
            with args.csv.open("w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
        else:
            args.csv.write_text("datetime,account,severity,category,message\n", encoding="utf-8")
        if not args.quiet:
            print(f"[monitor] Wrote anomalies CSV -> {args.csv} ({len(rows)} rows)")

    # JSON summary
    if args.json_out:
        summary = {
            "generated_at": datetime.now().isoformat(),
            "file_count": len(files),
            "event_count": len(events),
            "severity_counts": _severity_counts(reports),
            "accounts": {
                acc: {
                    "label": labels.get(acc, ""),
                    "start": r.start.isoformat(),
                    "end":   r.end.isoformat(),
                    "deals": r.deals,
                    "drops": r.drops,
                    "drop_clusters": r.drop_clusters,
                    "failed_orders": r.failed_orders,
                    "fast_sl_hits": r.fast_sl_hits,
                    "latency": {
                        "pending": r.latency_stats("pending"),
                        "modify":  r.latency_stats("modify"),
                        "cancel":  r.latency_stats("cancel"),
                        "market":  r.latency_stats("market"),
                    },
                    "per_symbol": r.per_symbol,
                    "anomaly_count": len(r.anomalies),
                }
                for acc, r in reports.items()
            },
        }
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(
            json.dumps(summary, indent=2, default=str),
            encoding="utf-8",
        )
        if not args.quiet:
            print(f"[monitor] Wrote JSON summary -> {args.json_out}")

    # Webhook alert
    webhook = args.webhook or cfg.get("webhook")
    if webhook and _should_alert(reports, args.alert_threshold):
        content = _format_webhook_message(reports, labels)
        if content:
            ok = _post_webhook(webhook, content)
            if not args.quiet:
                print(f"[monitor] Webhook alert {'sent' if ok else 'FAILED'}")

    # Exit code reflects severity
    sev = _severity_counts(reports)
    if sev["error"]:
        return 2
    if sev["warn"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
