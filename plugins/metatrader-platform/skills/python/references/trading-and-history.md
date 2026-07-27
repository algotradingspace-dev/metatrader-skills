# Trading And History

Self-written reference for trading requests, margin and profit estimation, and history retrieval through the `MetaTrader5` Python module.

---

## Pre-Trade Estimation

Use these functions before sending a live request:

- `order_calc_margin()`
- `order_calc_profit()`
- `order_check()`

Use `order_calc_margin()` when you need to estimate capital usage for a proposed trade.

Use `order_calc_profit()` when you need a broker-aware profit estimate for a given open and close price.

Use `order_check()` when you have assembled a concrete trade request and want the terminal to validate it before execution.

These functions are complementary:

- margin estimate for capacity
- profit estimate for scenario analysis
- order check for request validity against current account and symbol rules

---

## Sending Orders

Live trading is performed through `order_send()` using a request dictionary that mirrors MT5 trade request fields.

Common request fields:

- `action`
- `symbol`
- `volume`
- `type`
- `price`
- `sl`
- `tp`
- `deviation`
- `magic`
- `comment`
- `type_filling`
- `type_time`
- `position`
- `order`

Minimum safe rule set:

1. Inspect `account_info()` and `symbol_info()` first
2. Build the request explicitly
3. Run `order_check()` for non-trivial requests
4. Call `order_send()`
5. Inspect the returned result object, not just whether a Python object was returned

`order_send()` can succeed as an API call while still reporting a business-level rejection in the result.

---

## Active Orders And Positions

Use these functions for current state:

- `orders_total()`
- `orders_get()`
- `positions_total()`
- `positions_get()`

Filtering patterns:

- by symbol
- by ticket
- by group mask with include and exclude expressions

Use `orders_get()` for pending orders and `positions_get()` for live exposure. Do not treat them as interchangeable.

---

## Historical Orders And Deals

History functions:

- `history_orders_total()`
- `history_orders_get()`
- `history_deals_total()`
- `history_deals_get()`

Typical retrieval styles:

- by time interval
- by order ticket
- by position ticket
- by symbol group filter

Use order history when you need lifecycle visibility on submitted orders. Use deal history when you need actual execution records and realized trading activity.

This distinction matters because one order can produce multiple deal records.

---

## Request And Result Hygiene

For safe automation:

- always log the request you intended to send
- log the result fields that determine success or failure
- record `last_error()` when a call returns `None` or another invalid object
- keep order, position, and deal identifiers together in downstream logs

For pandas-based analysis, convert returned named tuples or structured arrays into records intentionally rather than relying on ad hoc printing.

---

## Practical Workflow

For most live Python trading flows, the sequence should be:

1. `initialize()`
2. `account_info()` and `terminal_info()`
3. `symbol_info()` and `symbol_info_tick()`
4. `order_calc_margin()` or `order_calc_profit()` if needed
5. `order_check()`
6. `order_send()`
7. `positions_get()` or `orders_get()` to verify resulting state
8. `history_deals_get()` later for execution audit
9. `shutdown()`

Keep the workflow explicit. The MetaTrader Python module is powerful, but it gives you little protection from vague or under-validated trading code.

---

## CHUNK PY-5 — Function Signatures: Trading And History

```python
# Pre-trade estimation
mt5.order_calc_margin(action, symbol, volume, price)  # → float margin or None
mt5.order_calc_profit(action, symbol, volume, price_open, price_close)  # → float or None
mt5.order_check(request)   # → MqlTradeCheckResult named tuple or None

# Send order
mt5.order_send(request)    # → MqlTradeResult named tuple or None

# Active state
mt5.orders_total()                             # → int
mt5.orders_get()                               # → all pending orders
mt5.orders_get(symbol="EURUSD")                # → by symbol
mt5.orders_get(group="*GBP*")                  # → by group mask
mt5.orders_get(ticket=100000002)               # → by ticket

mt5.positions_total()                          # → int
mt5.positions_get()                            # → all open positions
mt5.positions_get(symbol="EURUSD")
mt5.positions_get(group="*USD*")
mt5.positions_get(ticket=100000003)

# History (date_from/date_to: datetime or epoch seconds)
mt5.history_orders_total(date_from, date_to)   # → int
mt5.history_orders_get(date_from, date_to)     # → by time interval
mt5.history_orders_get(date_from, date_to, group="*GBP*")
mt5.history_orders_get(ticket=100000001)       # → by order ticket
mt5.history_orders_get(position=100000001)     # → all orders for a position

mt5.history_deals_total(date_from, date_to)    # → int
mt5.history_deals_get(date_from, date_to)      # → by time interval
mt5.history_deals_get(date_from, date_to, group="*USD*")
mt5.history_deals_get(ticket=100000004)        # → by order ticket (DEAL_ORDER)
mt5.history_deals_get(position=100000001)      # → by position ticket (DEAL_POSITION_ID)
```

**Key result fields from `order_send()`:** `retcode`, `deal`, `order`, `volume`, `price`, `bid`, `ask`, `comment`, `request_id`, `retcode_external`

---

## CHUNK PY-6 — Enumerations: Trade Actions, Order Types, Filling, Time

**TRADE_REQUEST_ACTIONS:**

| Constant | Description |
|----------|-------------|
| `mt5.TRADE_ACTION_DEAL` | Market order (instant execution) |
| `mt5.TRADE_ACTION_PENDING` | Place pending order |
| `mt5.TRADE_ACTION_SLTP` | Modify SL/TP on open position |
| `mt5.TRADE_ACTION_MODIFY` | Modify pending order parameters |
| `mt5.TRADE_ACTION_REMOVE` | Remove pending order |
| `mt5.TRADE_ACTION_CLOSE_BY` | Close position by opposite position |

**ORDER_TYPE:**

| Constant | Description |
|----------|-------------|
| `mt5.ORDER_TYPE_BUY` | Market buy |
| `mt5.ORDER_TYPE_SELL` | Market sell |
| `mt5.ORDER_TYPE_BUY_LIMIT` | Buy Limit pending |
| `mt5.ORDER_TYPE_SELL_LIMIT` | Sell Limit pending |
| `mt5.ORDER_TYPE_BUY_STOP` | Buy Stop pending |
| `mt5.ORDER_TYPE_SELL_STOP` | Sell Stop pending |
| `mt5.ORDER_TYPE_BUY_STOP_LIMIT` | Buy Stop Limit (creates Buy Limit at stoplimit price when triggered) |
| `mt5.ORDER_TYPE_SELL_STOP_LIMIT` | Sell Stop Limit (creates Sell Limit at stoplimit price when triggered) |
| `mt5.ORDER_TYPE_CLOSE_BY` | Close by opposite position |

**ORDER_TYPE_FILLING:**

| Constant | Description |
|----------|-------------|
| `mt5.ORDER_FILLING_FOK` | Fill or Kill — full volume or cancel |
| `mt5.ORDER_FILLING_IOC` | Immediate or Cancel — fill available volume, cancel remainder |
| `mt5.ORDER_FILLING_RETURN` | Return remainder as new order; only for market/limit on Market or Exchange execution symbols |

**ORDER_TYPE_TIME:**

| Constant | Description |
|----------|-------------|
| `mt5.ORDER_TIME_GTC` | Good Till Cancelled |
| `mt5.ORDER_TIME_DAY` | Active only for current trading day |
| `mt5.ORDER_TIME_SPECIFIED` | Active until specified date |
| `mt5.ORDER_TIME_SPECIFIED_DAY` | Active until 23:59:59 of specified day |

---

## CHUNK PY-7 — `MqlTradeRequest` Field Reference

| Field | Description |
|-------|-------------|
| `action` | TRADE_REQUEST_ACTIONS value |
| `magic` | EA magic number for order identification |
| `order` | Order ticket (required when modifying pending orders) |
| `symbol` | Instrument name (not needed for modify/close) |
| `volume` | Requested volume in lots |
| `price` | Execution price (not needed for SYMBOL_TRADE_EXECUTION_MARKET + DEAL) |
| `stoplimit` | Limit price for Stop Limit orders (price where Limit is placed when triggered) |
| `sl` | Stop Loss price |
| `tp` | Take Profit price |
| `deviation` | Max price deviation in points |
| `type` | ORDER_TYPE value |
| `type_filling` | ORDER_TYPE_FILLING value |
| `type_time` | ORDER_TYPE_TIME value |
| `expiration` | Expiry for SPECIFIED/SPECIFIED_DAY time type |
| `comment` | Order comment (up to 31 chars effective) |
| `position` | Position ticket (for SLTP/CLOSE_BY — needed for unambiguous position identification) |
| `position_by` | Opposite position ticket (for CLOSE_BY only) |

**References:**
- `docs/mql5_com_-_docs_python_metatrader5/21_mt5orderstotal_py.md`
- `docs/mql5_com_-_docs_python_metatrader5/22_mt5ordersget_py.md`
- `docs/mql5_com_-_docs_python_metatrader5/23_mt5ordercalcmargin_py.md`
- `docs/mql5_com_-_docs_python_metatrader5/24_mt5ordercalcprofit_py.md`
- `docs/mql5_com_-_docs_python_metatrader5/25_mt5ordercheck_py.md`
- `docs/mql5_com_-_docs_python_metatrader5/26_mt5ordersend_py.md`
- `docs/mql5_com_-_docs_python_metatrader5/27_mt5positionstotal_py.md`
- `docs/mql5_com_-_docs_python_metatrader5/28_mt5positionsget_py.md`
- `docs/mql5_com_-_docs_python_metatrader5/29_mt5historyorderstotal_py.md`
- `docs/mql5_com_-_docs_python_metatrader5/30_mt5historyordersget_py.md`
- `docs/mql5_com_-_docs_python_metatrader5/31_mt5historydealstotal_py.md`
- `docs/mql5_com_-_docs_python_metatrader5/32_mt5historydealsget_py.md`