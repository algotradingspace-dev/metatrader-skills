# Helper Patterns

Reusable abstraction patterns for the official `MetaTrader5` Python module.

This reference is about code organization, not just one-off examples. Use it when MT5 Python code is starting to repeat connection setup, request assembly, or result normalization logic.

---

## Design Goal

The `MetaTrader5` module is stateful and terminal-bound. Good helper abstractions should make that explicit rather than hiding it.

Prefer helpers that:

- make session boundaries obvious
- keep request construction explicit
- normalize MT5 return values predictably
- preserve access to `last_error()` and raw result objects

Avoid helpers that:

- open and close terminals implicitly in unrelated utility functions
- hide the exact request sent to `order_send()`
- silently coerce `None` results into empty collections
- blur the boundary between market-data reads and live trading actions

---

## Session Wrapper Pattern

Wrap `initialize()` and `shutdown()` in a small context manager when multiple scripts or services need the same safety behavior.

```python
from contextlib import contextmanager

import MetaTrader5 as mt5


@contextmanager
def mt5_session(*, path=None, login=None, password=None, server=None, timeout=60000, portable=False):
    kwargs = {"timeout": timeout, "portable": portable}
    if path is not None:
        kwargs["path"] = path
    if login is not None:
        kwargs["login"] = login
    if password is not None:
        kwargs["password"] = password
    if server is not None:
        kwargs["server"] = server

    if not mt5.initialize(**kwargs):
        raise RuntimeError(f"MT5 initialize failed: {mt5.last_error()}")

    try:
        yield mt5
    finally:
        mt5.shutdown()
```

Why this works:

- the lifecycle is still explicit at the call site
- failures stay close to initialization
- `shutdown()` is guaranteed in normal and exceptional flows

---

## Account Guard Pattern

If a script is sensitive to account identity, guard it immediately after session start.

```python
def require_account(mt5_module, *, login=None, server=None):
    account = mt5_module.account_info()
    if account is None:
        raise RuntimeError(f"account_info failed: {mt5_module.last_error()}")

    if login is not None and account.login != login:
        raise RuntimeError(f"unexpected account login: {account.login}")
    if server is not None and account.server != server:
        raise RuntimeError(f"unexpected account server: {account.server}")

    return account
```

This is especially useful on workstations with remembered credentials or multiple installed terminals.

---

## Request Builder Pattern

Build trade requests through explicit functions that return plain dictionaries. Do not bury request assembly inside large service methods.

```python
def build_market_buy_request(*, symbol, volume, price, deviation, magic, comment):
    return {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "deviation": deviation,
        "magic": magic,
        "comment": comment,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
```

Why this is preferable:

- requests are testable before sending
- logging the outbound request is straightforward
- strategy logic can decide parameters without owning MT5 request constants directly

For more complex systems, pair builders with validation helpers rather than with implicit send helpers.

---

## Validation Layer Pattern

Split validation into separate functions before `order_check()` and `order_send()`.

Useful layers:

- account guard
- symbol tradability guard
- volume guard
- stop-distance guard
- request shape validation

Example layout:

```python
def validate_symbol_for_trade(symbol_info):
    if symbol_info is None:
        raise RuntimeError("symbol info missing")
    if symbol_info.volume_min <= 0 or symbol_info.volume_step <= 0:
        raise RuntimeError("symbol volume constraints are invalid")


def validate_volume(symbol_info, volume):
    if volume < symbol_info.volume_min or volume > symbol_info.volume_max:
        raise RuntimeError("volume is outside broker limits")
```

Keep validation deterministic and side-effect free where possible.

---

## DataFrame Normalization Pattern

MT5 return values often arrive as named tuples, structured arrays, or `None`. Normalize them in one place.

```python
import pandas as pd


def to_frame(rows):
    if rows is None:
        return None
    if len(rows) == 0:
        return pd.DataFrame()
    return pd.DataFrame(list(rows), columns=rows[0]._asdict().keys())


def normalize_time_columns(frame, columns):
    if frame is None or frame.empty:
        return frame
    for column in columns:
        if column in frame.columns:
            frame[column] = pd.to_datetime(frame[column], unit="s", utc=True)
    return frame
```

Practical rule:

- `None` means failure
- empty collection means valid query with no rows
- DataFrame normalization should preserve that distinction

---

## Repository Layout Pattern

When Python MT5 code grows beyond a single file, split by responsibility:

```text
mt5_client/
  session.py          # initialize/shutdown wrappers
  guards.py           # account, symbol, and permission checks
  requests.py         # request builders
  data.py             # symbol/rates/ticks/history retrieval
  normalize.py        # pandas conversion helpers
  trading.py          # order_check/order_send workflows
```

This keeps strategy code from becoming tangled with MT5 transport code.

---

## Separation Of Concerns

Keep these layers distinct:

- strategy logic: signals, entries, exits, risk intent
- MT5 validation layer: symbol and account constraints
- MT5 execution layer: request build, check, send, inspect result
- data normalization layer: convert MT5 outputs into analysis-friendly structures

If those layers collapse into one function, debugging gets expensive quickly.

---

## Logging Pattern

For reliable debugging, log at least:

- terminal path or target account
- symbol
- request payload
- `order_check()` result when used
- `order_send()` result fields such as `retcode`, `order`, `deal`, and `comment`
- `last_error()` when any call returns `None` or `False`

Keep raw MT5 data available in logs before transforming it into business-level summaries.

---

## Rule Of Thumb

Use wrappers to reduce repetition, not to conceal state. The best MT5 Python helpers make lifecycle, account identity, request contents, and failure paths easier to inspect.