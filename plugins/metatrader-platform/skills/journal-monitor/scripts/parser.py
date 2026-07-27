"""MT5 journal log parser.

MT5 journal logs are tab-separated, usually UTF-16 LE with BOM.
Line format:
    <code>\t<level>\t<HH:MM:SS.mmm>\t<source>\t<message>

Examples:
    RO  0   06:00:01.328    Trades  'ACCOUNT_ID': buy stop 0.16 XAUUSD at 4772.25 sl: ...
    JL  1   04:32:42.423    Network 'ACCOUNT_ID': connection to <broker-server> lost

Filenames usually encode account + date: JournalLog-<account>-<YYYYMMDD>.log
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Iterable, Iterator


FILENAME_RE = re.compile(
    r"JournalLog-(?P<account>\d+)-(?P<date>\d{8})\.log$", re.IGNORECASE
)
LINE_RE = re.compile(
    r"^(?P<code>\S+)\t(?P<level>\d+)\t"
    r"(?P<time>\d{2}:\d{2}:\d{2}\.\d{3})\t"
    r"(?P<source>[^\t]+)\t"
    r"(?P<message>.+)$"
)

# Message patterns we care about
DONE_IN_RE = re.compile(r"done in ([\d.]+) ms")
ORDER_ID_RE = re.compile(r"#(\d+)")
DEAL_RE = re.compile(
    r"deal #(\d+) (buy|sell) ([\d.]+) (\S+) at ([\d.]+)"
    r"(?: done \(based on order #(\d+)\))?"
)
PENDING_RE = re.compile(
    r"(?:buy|sell) (?:stop|limit) ([\d.]+) (\S+) at ([\d.]+)(?: sl: ([\d.]+))?(?: tp: ([\d.]+))?"
)
MODIFY_RE = re.compile(r"modify #(\d+) (?:buy|sell) ([\d.]+) (\S+)")
ACCEPT_RE = re.compile(r"accepted ")
CONN_LOST_RE = re.compile(r"connection to (\S+) lost")
CONN_AUTH_RE = re.compile(r"authorized on (\S+)")
FAILED_RE = re.compile(r"(failed|rejected|invalid|not enough money|requote|off quotes)", re.IGNORECASE)


@dataclass
class JournalEvent:
    """One parsed journal line."""

    datetime: datetime
    account: str
    source: str  # Trades / Network / Experts / etc.
    message: str
    level: int   # 0 = info, 1 = warn, 2 = error
    raw: str
    file: str

    # Parsed fields (populated by classifier)
    event_type: str = "other"   # connection_drop / connection_auth / pending / accepted /
                                 # deal / modify / cancel / done_in / failed / other
    symbol: str | None = None
    order_id: str | None = None
    deal_id: str | None = None
    volume: float | None = None
    price: float | None = None
    sl: float | None = None
    tp: float | None = None
    side: str | None = None       # buy / sell
    duration_ms: float | None = None
    server: str | None = None     # for connection events


def _read_journal(path: Path) -> str:
    """Read a journal file, auto-detecting UTF-16 BOM."""
    raw = path.read_bytes()
    if raw[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return raw.decode("utf-16", errors="replace")
    # Some MT5 builds write UTF-8 without BOM
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("latin-1", errors="replace")


def _classify(event: JournalEvent) -> None:
    """Populate event_type and parsed fields based on message and source."""
    msg = event.message
    src = event.source

    if src == "Network":
        if m := CONN_LOST_RE.search(msg):
            event.event_type = "connection_drop"
            event.server = m.group(1)
            return
        if m := CONN_AUTH_RE.search(msg):
            event.event_type = "connection_auth"
            event.server = m.group(1)
            return
        event.event_type = "network_other"
        return

    if src != "Trades":
        event.event_type = "other"
        return

    # Trades lines - classify most-specific first
    if FAILED_RE.search(msg):
        event.event_type = "failed"
    elif "deal #" in msg:
        event.event_type = "deal"
        if m := DEAL_RE.search(msg):
            event.deal_id = m.group(1)
            event.side = m.group(2)
            event.volume = float(m.group(3))
            event.symbol = m.group(4)
            event.price = float(m.group(5))
            if m.group(6):
                event.order_id = m.group(6)
    elif "done in" in msg and ("order #" in msg or "modify" in msg or "cancel" in msg):
        # Completion notice with latency
        if "modify" in msg:
            event.event_type = "modify_done"
            if m := MODIFY_RE.search(msg):
                event.order_id = m.group(1)
                event.volume = float(m.group(2))
                event.symbol = m.group(3)
        elif "cancel" in msg:
            event.event_type = "cancel_done"
        else:
            event.event_type = "order_done"
    elif "accepted " in msg:
        # Broker accepted the request (preceeds done)
        if "cancel " in msg:
            event.event_type = "accepted_cancel"
        elif "modify" in msg:
            event.event_type = "accepted_modify"
        else:
            event.event_type = "accepted"
    elif "modify #" in msg:
        event.event_type = "modify_request"
        if m := MODIFY_RE.search(msg):
            event.order_id = m.group(1)
            event.volume = float(m.group(2))
            event.symbol = m.group(3)
    elif "cancel " in msg or "cancel #" in msg:
        event.event_type = "cancel_request"
    elif "buy stop" in msg or "sell stop" in msg or "buy limit" in msg or "sell limit" in msg:
        event.event_type = "pending_request"
        if m := PENDING_RE.search(msg):
            event.volume = float(m.group(1))
            event.symbol = m.group(2)
            event.price = float(m.group(3))
            if m.group(4):
                event.sl = float(m.group(4))
            if m.group(5):
                event.tp = float(m.group(5))
            event.side = "buy" if msg.lstrip().startswith(tuple(["'"])) and "buy" in msg.split("':")[1].split()[0:2] else ("buy" if " buy " in msg else "sell")
    elif "market buy" in msg or "market sell" in msg:
        event.event_type = "market_request"
    elif "placed for execution" in msg:
        event.event_type = "placed"
    else:
        event.event_type = "trades_other"

    # Grab duration if present
    if m := DONE_IN_RE.search(msg):
        event.duration_ms = float(m.group(1))

    # Extract order_id if missing
    if not event.order_id:
        if m := ORDER_ID_RE.search(msg):
            event.order_id = m.group(1)

    # Extract symbol if missing (fallback token scan)
    if not event.symbol:
        for token in msg.split():
            stripped = token.rstrip(",.:")
            if re.fullmatch(r"[A-Z]{3,6}p?\d?", stripped) and stripped.isupper():
                event.symbol = stripped
                break


def parse_file(path: str | Path) -> list[JournalEvent]:
    """Parse one MT5 journal log file."""
    path = Path(path)
    m = FILENAME_RE.search(path.name)
    if not m:
        raise ValueError(f"Filename doesn't match JournalLog-<account>-<YYYYMMDD>.log: {path.name}")
    account = m.group("account")
    date_str = m.group("date")
    file_date = datetime.strptime(date_str, "%Y%m%d").date()

    text = _read_journal(path)
    events: list[JournalEvent] = []
    for line in text.splitlines():
        line = line.rstrip("\r\n")
        if not line:
            continue
        lm = LINE_RE.match(line)
        if not lm:
            continue
        time_part = lm.group("time")
        hh, mm, rest = time_part.split(":")
        ss, ms = rest.split(".")
        dt = datetime(file_date.year, file_date.month, file_date.day,
                      int(hh), int(mm), int(ss), int(ms) * 1000)
        event = JournalEvent(
            datetime=dt,
            account=account,
            source=lm.group("source"),
            message=lm.group("message"),
            level=int(lm.group("level")),
            raw=line,
            file=path.name,
        )
        _classify(event)
        events.append(event)

    events.sort(key=lambda e: e.datetime)
    return events


def parse_directory(directory: str | Path, pattern: str = "JournalLog-*.log") -> list[JournalEvent]:
    """Parse every MT5 journal in a directory."""
    directory = Path(directory)
    events: list[JournalEvent] = []
    for f in sorted(directory.glob(pattern)):
        try:
            events.extend(parse_file(f))
        except ValueError:
            continue  # skip files that don't match naming convention
    events.sort(key=lambda e: e.datetime)
    return events


def parse_paths(paths: Iterable[str | Path]) -> list[JournalEvent]:
    """Parse a list of specific files (or directories)."""
    events: list[JournalEvent] = []
    for p in paths:
        p = Path(p)
        if p.is_dir():
            events.extend(parse_directory(p))
        elif p.is_file():
            events.extend(parse_file(p))
    events.sort(key=lambda e: e.datetime)
    return events


if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) < 2:
        print("usage: parser.py <journal_file_or_dir> [...]")
        sys.exit(1)
    evs = parse_paths(sys.argv[1:])
    counts: dict[str, int] = {}
    for e in evs:
        counts[e.event_type] = counts.get(e.event_type, 0) + 1
    print(f"Parsed {len(evs)} events")
    for k in sorted(counts):
        print(f"  {k}: {counts[k]}")
