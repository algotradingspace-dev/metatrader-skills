"""MT5 journal analyzer — computes health metrics from parsed events.

Given a list of JournalEvents for one or many accounts, compute:
- Connection drop frequency and clusters
- Execution latency distributions (pending, modify, cancel, market)
- Failed/rejected order details
- Fast-SL-hit detection (position opened -> closed-at-SL within N seconds)
- Per-account and per-symbol breakdowns
"""
from __future__ import annotations

import statistics
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Iterable

from parser import JournalEvent


# Thresholds
SLOW_FILL_MS = 100.0
SLOW_MODIFY_MS = 50.0
FAST_SL_HIT_SECONDS = 30       # SL hit within 30s of entry = suspicious
DROP_CLUSTER_SECONDS = 300      # drops within 5 min = one incident


@dataclass
class Anomaly:
    datetime: datetime
    account: str
    severity: str           # info / warn / error
    category: str           # connection_drop / slow_fill / slow_modify / failed_order / fast_sl_hit
    message: str
    detail: dict = field(default_factory=dict)


@dataclass
class AccountReport:
    account: str
    start: datetime
    end: datetime
    total_events: int = 0

    # Connection
    drops: int = 0
    drop_clusters: int = 0
    reauths: int = 0
    drop_times: list[datetime] = field(default_factory=list)

    # Execution latency (ms) by category
    pending_latencies: list[float] = field(default_factory=list)
    modify_latencies: list[float] = field(default_factory=list)
    cancel_latencies: list[float] = field(default_factory=list)
    market_latencies: list[float] = field(default_factory=list)

    # Outcomes
    deals: int = 0
    failed_orders: int = 0
    fast_sl_hits: int = 0

    # Per-symbol
    per_symbol: dict[str, dict] = field(default_factory=dict)

    anomalies: list[Anomaly] = field(default_factory=list)

    def latency_stats(self, category: str) -> dict:
        mapping = {
            "pending": self.pending_latencies,
            "modify":  self.modify_latencies,
            "cancel":  self.cancel_latencies,
            "market":  self.market_latencies,
        }
        vals = mapping.get(category, [])
        if not vals:
            return {"n": 0}
        return {
            "n":     len(vals),
            "min":   round(min(vals), 1),
            "mean":  round(statistics.mean(vals), 1),
            "median":round(statistics.median(vals), 1),
            "p95":   round(_p(vals, 0.95), 1),
            "max":   round(max(vals), 1),
        }


def _p(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    s = sorted(values)
    k = int(round((len(s) - 1) * pct))
    return s[k]


def analyze(
    events: list[JournalEvent],
    slow_fill_ms: float = SLOW_FILL_MS,
    slow_modify_ms: float = SLOW_MODIFY_MS,
    fast_sl_seconds: int = FAST_SL_HIT_SECONDS,
) -> dict[str, AccountReport]:
    """Group events by account and build a report per account."""
    by_account: dict[str, list[JournalEvent]] = defaultdict(list)
    for e in events:
        by_account[e.account].append(e)

    reports: dict[str, AccountReport] = {}
    for account, evs in by_account.items():
        evs.sort(key=lambda e: e.datetime)
        report = AccountReport(
            account=account,
            start=evs[0].datetime,
            end=evs[-1].datetime,
            total_events=len(evs),
        )

        # Connection drops + clusters
        last_drop: datetime | None = None
        for e in evs:
            if e.event_type == "connection_drop":
                report.drops += 1
                report.drop_times.append(e.datetime)
                if last_drop is None or (e.datetime - last_drop).total_seconds() > DROP_CLUSTER_SECONDS:
                    report.drop_clusters += 1
                last_drop = e.datetime
                report.anomalies.append(Anomaly(
                    datetime=e.datetime, account=account,
                    severity="warn", category="connection_drop",
                    message=f"Connection to {e.server or 'broker'} lost",
                    detail={"server": e.server},
                ))
            elif e.event_type == "connection_auth":
                report.reauths += 1

        # Latency by category
        for e in evs:
            if e.duration_ms is None:
                continue
            if e.event_type == "order_done":
                category = "pending"  # default
                if e.order_id:
                    for prev in reversed(evs[:evs.index(e)][-10:]):
                        if prev.order_id == e.order_id:
                            if prev.event_type == "market_request":
                                category = "market"
                            break
                lat_list = report.market_latencies if category == "market" else report.pending_latencies
                lat_list.append(e.duration_ms)
                if e.duration_ms > slow_fill_ms:
                    report.anomalies.append(Anomaly(
                        datetime=e.datetime, account=account,
                        severity="warn" if e.duration_ms < 1000 else "error",
                        category=f"slow_{category}_fill",
                        message=f"{category.title()} order took {e.duration_ms:.0f} ms "
                                f"(threshold {slow_fill_ms:.0f} ms)",
                        detail={"order_id": e.order_id, "symbol": e.symbol,
                                "duration_ms": e.duration_ms},
                    ))
            elif e.event_type == "modify_done":
                report.modify_latencies.append(e.duration_ms)
                if e.duration_ms > slow_modify_ms:
                    report.anomalies.append(Anomaly(
                        datetime=e.datetime, account=account,
                        severity="warn" if e.duration_ms < 500 else "error",
                        category="slow_modify",
                        message=f"SL/TP modify took {e.duration_ms:.0f} ms "
                                f"(threshold {slow_modify_ms:.0f} ms)",
                        detail={"order_id": e.order_id, "symbol": e.symbol,
                                "duration_ms": e.duration_ms},
                    ))
            elif e.event_type == "cancel_done":
                report.cancel_latencies.append(e.duration_ms)

        # Deals and failed orders
        for e in evs:
            if e.event_type == "deal":
                report.deals += 1
                sym = e.symbol or "unknown"
                bucket = report.per_symbol.setdefault(sym, {"deals": 0, "failed": 0, "fast_sl_hits": 0})
                bucket["deals"] += 1
            elif e.event_type == "failed":
                report.failed_orders += 1
                report.anomalies.append(Anomaly(
                    datetime=e.datetime, account=account,
                    severity="error", category="failed_order",
                    message=f"Order failed/rejected",
                    detail={"message": e.message[:200]},
                ))
                sym = e.symbol or "unknown"
                bucket = report.per_symbol.setdefault(sym, {"deals": 0, "failed": 0, "fast_sl_hits": 0})
                bucket["failed"] += 1

        # Fast SL hits
        opens: dict[str, JournalEvent] = {}
        for e in evs:
            if e.event_type != "deal":
                continue
            sym = e.symbol or ""
            if sym in opens:
                prev = opens[sym]
                dt_diff = (e.datetime - prev.datetime).total_seconds()
                if (0 < dt_diff <= fast_sl_seconds and
                        prev.side and e.side and prev.side != e.side and
                        prev.volume == e.volume):
                    report.fast_sl_hits += 1
                    report.per_symbol.setdefault(sym, {"deals": 0, "failed": 0, "fast_sl_hits": 0})
                    report.per_symbol[sym]["fast_sl_hits"] += 1
                    move = (e.price - prev.price) if (prev.price and e.price) else None
                    report.anomalies.append(Anomaly(
                        datetime=e.datetime, account=account,
                        severity="warn", category="fast_sl_hit",
                        message=f"Position closed within {dt_diff:.0f}s on {sym} "
                                f"(open {prev.price} -> close {e.price}, move {move:+.2f})"
                                if move is not None else
                                f"Position closed within {dt_diff:.0f}s on {sym}",
                        detail={"symbol": sym, "open_price": prev.price,
                                "close_price": e.price, "duration_sec": dt_diff,
                                "open_side": prev.side, "close_side": e.side,
                                "volume": prev.volume},
                    ))
                    opens.pop(sym, None)
                else:
                    opens[sym] = e
            else:
                opens[sym] = e

        reports[account] = report

    return reports


def format_report(reports: dict[str, AccountReport],
                  account_labels: dict[str, str] | None = None) -> str:
    """Produce a human-readable markdown report from analysis results."""
    account_labels = account_labels or {}
    lines: list[str] = []
    lines.append("# MT5 Journal Monitor — Report")
    lines.append("")
    if reports:
        starts = [r.start for r in reports.values()]
        ends = [r.end for r in reports.values()]
        lines.append(f"**Period:** {min(starts).isoformat(sep=' ')} -> {max(ends).isoformat(sep=' ')}")
        lines.append(f"**Accounts analyzed:** {len(reports)}")
    lines.append("")

    # Summary table
    lines.append("## Summary")
    lines.append("")
    lines.append("| Account | Label | Deals | Drops | Failed | Fast-SL | Pending p95 | Modify p95 | Market p95 |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for acc, r in sorted(reports.items()):
        label = account_labels.get(acc, "")
        ps = r.latency_stats("pending")
        ms = r.latency_stats("modify")
        mk = r.latency_stats("market")
        lines.append(
            f"| {acc} | {label} | {r.deals} | {r.drops} | {r.failed_orders} | "
            f"{r.fast_sl_hits} | "
            f"{ps.get('p95', '\u2014') if ps['n'] else '\u2014'} | "
            f"{ms.get('p95', '\u2014') if ms['n'] else '\u2014'} | "
            f"{mk.get('p95', '\u2014') if mk['n'] else '\u2014'} |"
        )
    lines.append("")

    # Per-account detail
    for acc, r in sorted(reports.items()):
        label = account_labels.get(acc, "")
        header = f"## Account {acc}"
        if label:
            header += f" \u2014 {label}"
        lines.append(header)
        lines.append("")
        lines.append(f"- Events parsed: {r.total_events}")
        lines.append(f"- Deals: {r.deals}")
        lines.append(f"- Connection drops: {r.drops} "
                     f"(in {r.drop_clusters} cluster{'s' if r.drop_clusters != 1 else ''})")
        if r.drops:
            lines.append(f"  - Drop times: " + ", ".join(d.strftime("%m-%d %H:%M:%S") for d in r.drop_times))
        lines.append(f"- Failed/rejected orders: {r.failed_orders}")
        lines.append(f"- Fast SL hits (<={FAST_SL_HIT_SECONDS}s round trip): {r.fast_sl_hits}")

        lines.append("")
        lines.append("### Execution latency (ms)")
        lines.append("")
        lines.append("| Category | n | min | median | mean | p95 | max |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|")
        for cat in ("pending", "modify", "cancel", "market"):
            s = r.latency_stats(cat)
            if s["n"] == 0:
                lines.append(f"| {cat} | 0 | \u2014 | \u2014 | \u2014 | \u2014 | \u2014 |")
            else:
                lines.append(
                    f"| {cat} | {s['n']} | {s['min']} | {s['median']} | "
                    f"{s['mean']} | {s['p95']} | {s['max']} |"
                )
        lines.append("")

        if r.per_symbol:
            lines.append("### Per-symbol activity")
            lines.append("")
            lines.append("| Symbol | Deals | Failed | Fast-SL |")
            lines.append("|---|---:|---:|---:|")
            for sym, stats in sorted(r.per_symbol.items()):
                lines.append(
                    f"| {sym} | {stats['deals']} | {stats['failed']} | {stats['fast_sl_hits']} |"
                )
            lines.append("")

        if r.anomalies:
            lines.append(f"### Anomalies ({len(r.anomalies)})")
            lines.append("")
            shown = r.anomalies[:20]
            for a in shown:
                sev = {"info": "\u2139\ufe0f", "warn": "\u26a0\ufe0f", "error": "\u274c"}.get(a.severity, "\u2022")
                lines.append(f"- {sev} `{a.datetime.strftime('%Y-%m-%d %H:%M:%S')}` "
                             f"**{a.category}** \u2014 {a.message}")
            if len(r.anomalies) > 20:
                lines.append(f"- \u2026 and {len(r.anomalies) - 20} more (see CSV)")
            lines.append("")

    return "\n".join(lines)


def anomalies_to_rows(reports: dict[str, AccountReport]) -> list[dict]:
    """Flatten anomalies to rows for CSV export."""
    rows = []
    for acc, r in reports.items():
        for a in r.anomalies:
            row = {
                "datetime": a.datetime.isoformat(sep=" "),
                "account":  a.account,
                "severity": a.severity,
                "category": a.category,
                "message":  a.message,
            }
            row.update({f"detail_{k}": v for k, v in a.detail.items()})
            rows.append(row)
    return rows


if __name__ == "__main__":
    import sys
    from parser import parse_paths

    if len(sys.argv) < 2:
        print("usage: analyzer.py <journal_file_or_dir> [...]")
        sys.exit(1)
    events = parse_paths(sys.argv[1:])
    reports = analyze(events)
    print(format_report(reports))
