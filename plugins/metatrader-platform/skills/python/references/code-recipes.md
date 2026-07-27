# Code Recipes

Concrete `MetaTrader5` Python module recipes for common integration tasks.

---

## Recipe: Connect And Inspect Session

Use this when you want the smallest useful sanity check against a local MT5 terminal.

```python
from pathlib import Path

import MetaTrader5 as mt5

terminal_path = Path(r"C:\Program Files\MetaTrader 5\terminal64.exe")

if not mt5.initialize(path=str(terminal_path)):
    raise RuntimeError(f"initialize failed: {mt5.last_error()}")

try:
    version = mt5.version()
    terminal = mt5.terminal_info()
    account = mt5.account_info()

    if version is None or terminal is None or account is None:
        raise RuntimeError(f"session inspection failed: {mt5.last_error()}")

    print("version:", version)
    print("connected:", terminal.connected)
    print("server:", account.server)
    print("login:", account.login)
    print("trade_allowed:", account.trade_allowed)
finally:
    mt5.shutdown()
```

Notes:

- Prefer explicit terminal paths in multi-terminal setups
- Fail fast on `None` and read `last_error()` immediately

---

## Recipe: Fetch Candles Into A DataFrame

Use UTC timestamps whenever you call time-bounded rate functions.

```python
from datetime import datetime, timezone

import MetaTrader5 as mt5
import pandas as pd

if not mt5.initialize():
    raise RuntimeError(f"initialize failed: {mt5.last_error()}")

try:
    date_from = datetime(2026, 1, 1, tzinfo=timezone.utc)
    date_to = datetime(2026, 1, 31, 23, 59, tzinfo=timezone.utc)

    rates = mt5.copy_rates_range("EURUSD", mt5.TIMEFRAME_H1, date_from, date_to)
    if rates is None:
        raise RuntimeError(f"copy_rates_range failed: {mt5.last_error()}")

    candles = pd.DataFrame(rates)
    candles["time"] = pd.to_datetime(candles["time"], unit="s", utc=True)

    print(candles[["time", "open", "high", "low", "close"]].tail())
finally:
    mt5.shutdown()
```

Notes:

- Returned timestamps are UTC
- Convert to local time only for display, not for analytics inputs

---

## Recipe: Ensure Symbol Visibility And Read Tick Data

This is the minimal safe pattern before using a symbol for trading logic.

```python
import MetaTrader5 as mt5

symbol = "XAUUSD"

if not mt5.initialize():
    raise RuntimeError(f"initialize failed: {mt5.last_error()}")

try:
    info = mt5.symbol_info(symbol)
    if info is None:
        raise RuntimeError(f"symbol_info failed: {mt5.last_error()}")

    if not info.visible and not mt5.symbol_select(symbol, True):
        raise RuntimeError(f"symbol_select failed: {mt5.last_error()}")

    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        raise RuntimeError(f"symbol_info_tick failed: {mt5.last_error()}")

    print({
        "bid": tick.bid,
        "ask": tick.ask,
        "spread_points": info.spread,
        "volume_min": info.volume_min,
        "volume_step": info.volume_step,
    })
finally:
    mt5.shutdown()
```

---

## Recipe: Safe Market Order Flow

This example keeps the validation sequence explicit: account, symbol, check, send.

```python
import MetaTrader5 as mt5

symbol = "EURUSD"
volume = 0.10
deviation = 20
magic = 26032026

if not mt5.initialize():
    raise RuntimeError(f"initialize failed: {mt5.last_error()}")

try:
    account = mt5.account_info()
    symbol_info = mt5.symbol_info(symbol)
    tick = mt5.symbol_info_tick(symbol)

    if account is None or symbol_info is None or tick is None:
        raise RuntimeError(f"pre-trade inspection failed: {mt5.last_error()}")

    if not account.trade_allowed:
        raise RuntimeError("account trading is disabled")

    if volume < symbol_info.volume_min or volume > symbol_info.volume_max:
        raise RuntimeError("requested volume is outside broker limits")

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": mt5.ORDER_TYPE_BUY,
        "price": tick.ask,
        "deviation": deviation,
        "magic": magic,
        "comment": "python-bridge market buy",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    check = mt5.order_check(request)
    if check is None:
        raise RuntimeError(f"order_check failed: {mt5.last_error()}")

    result = mt5.order_send(request)
    if result is None:
        raise RuntimeError(f"order_send failed: {mt5.last_error()}")

    print({
        "retcode": result.retcode,
        "order": result.order,
        "deal": result.deal,
        "price": result.price,
        "comment": result.comment,
    })
finally:
    mt5.shutdown()
```

Notes:

- A non-`None` result is not enough; inspect `retcode`
- Validate stops, margin, and symbol trade rules before adding `sl` and `tp`

---

## Recipe: Estimate Margin And Profit

Use these calculations before deciding whether a proposed trade belongs in the next step.

```python
import MetaTrader5 as mt5

symbol = "GBPUSD"
volume = 0.20

if not mt5.initialize():
    raise RuntimeError(f"initialize failed: {mt5.last_error()}")

try:
    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        raise RuntimeError(f"symbol_info_tick failed: {mt5.last_error()}")

    margin = mt5.order_calc_margin(mt5.ORDER_TYPE_BUY, symbol, volume, tick.ask)
    profit = mt5.order_calc_profit(mt5.ORDER_TYPE_BUY, symbol, volume, tick.ask, tick.ask + 0.0020)

    if margin is None or profit is None:
        raise RuntimeError(f"calculation failed: {mt5.last_error()}")

    print({"margin": margin, "projected_profit": profit})
finally:
    mt5.shutdown()
```

---

## Recipe: Query Open Positions Into pandas

```python
import MetaTrader5 as mt5
import pandas as pd

if not mt5.initialize():
    raise RuntimeError(f"initialize failed: {mt5.last_error()}")

try:
    positions = mt5.positions_get(group="*USD*")
    if positions is None:
        raise RuntimeError(f"positions_get failed: {mt5.last_error()}")

    frame = pd.DataFrame(list(positions), columns=positions[0]._asdict().keys()) if positions else pd.DataFrame()
    if not frame.empty:
        frame["time"] = pd.to_datetime(frame["time"], unit="s", utc=True)
    print(frame)
finally:
    mt5.shutdown()
```

Notes:

- `positions_get()` returning an empty collection is different from returning `None`
- Group filters support include and exclude patterns

---

## Recipe: Pull Deal History For One Position

Use position-linked deal history when you want execution audit data rather than only current exposure.

```python
from datetime import datetime, timedelta, timezone

import MetaTrader5 as mt5
import pandas as pd

position_id = 100000001

if not mt5.initialize():
    raise RuntimeError(f"initialize failed: {mt5.last_error()}")

try:
    date_to = datetime.now(timezone.utc)
    date_from = date_to - timedelta(days=30)

    deals = mt5.history_deals_get(date_from, date_to, position=position_id)
    if deals is None:
        raise RuntimeError(f"history_deals_get failed: {mt5.last_error()}")

    history = pd.DataFrame(list(deals), columns=deals[0]._asdict().keys()) if deals else pd.DataFrame()
    if not history.empty:
        history["time"] = pd.to_datetime(history["time"], unit="s", utc=True)

    print(history[["ticket", "order", "position_id", "symbol", "volume", "price", "profit", "time"]])
finally:
    mt5.shutdown()
```

Practical rule:

- Use order history for order lifecycle analysis
- Use deal history for actual fills and realized P&L