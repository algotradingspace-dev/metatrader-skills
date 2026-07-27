# Order Property Enums

## ENUM_ORDER_PROPERTY_INTEGER — `OrderGetInteger()` / `HistoryOrderGetInteger()`

| Identifier | Description | Type |
|------------|-------------|------|
| `ORDER_TICKET` | Unique order ticket | long |
| `ORDER_TIME_SETUP` | Order setup time | datetime |
| `ORDER_TYPE` | Order type | `ENUM_ORDER_TYPE` |
| `ORDER_STATE` | Order state | `ENUM_ORDER_STATE` |
| `ORDER_TIME_EXPIRATION` | Expiration time | datetime |
| `ORDER_TIME_DONE` | Execution or cancellation time | datetime |
| `ORDER_TIME_SETUP_MSC` | Setup time in ms since 1970 | long |
| `ORDER_TIME_DONE_MSC` | Done time in ms since 1970 | long |
| `ORDER_TYPE_FILLING` | Volume filling type | `ENUM_ORDER_TYPE_FILLING` |
| `ORDER_TYPE_TIME` | Order lifetime | `ENUM_ORDER_TYPE_TIME` |
| `ORDER_MAGIC` | EA magic number | long |
| `ORDER_REASON` | Reason for placing | `ENUM_ORDER_REASON` |
| `ORDER_POSITION_ID` | Related position ticket | long |
| `ORDER_POSITION_BY_ID` | Opposite position ticket (CLOSE_BY) | long |

## ENUM_ORDER_PROPERTY_DOUBLE — `OrderGetDouble()` / `HistoryOrderGetDouble()`

| Identifier | Description |
|------------|-------------|
| `ORDER_VOLUME_INITIAL` | Initial volume |
| `ORDER_VOLUME_CURRENT` | Current (remaining) volume |
| `ORDER_PRICE_OPEN` | Order price |
| `ORDER_SL` | Stop Loss |
| `ORDER_TP` | Take Profit |
| `ORDER_PRICE_CURRENT` | Current symbol price |
| `ORDER_PRICE_STOPLIMIT` | StopLimit level |

`ENUM_ORDER_PROPERTY_STRING`: `ORDER_SYMBOL` · `ORDER_COMMENT` · `ORDER_EXTERNAL_ID`

---

## ENUM_ORDER_TYPE

| Value | Description |
|-------|-------------|
| `ORDER_TYPE_BUY` | Market Buy |
| `ORDER_TYPE_SELL` | Market Sell |
| `ORDER_TYPE_BUY_LIMIT` | Buy Limit pending |
| `ORDER_TYPE_SELL_LIMIT` | Sell Limit pending |
| `ORDER_TYPE_BUY_STOP` | Buy Stop pending |
| `ORDER_TYPE_SELL_STOP` | Sell Stop pending |
| `ORDER_TYPE_BUY_STOP_LIMIT` | Buy StopLimit pending |
| `ORDER_TYPE_SELL_STOP_LIMIT` | Sell StopLimit pending |
| `ORDER_TYPE_CLOSE_BY` | Close by opposite position |

## ENUM_ORDER_STATE

| Value | Description |
|-------|-------------|
| `ORDER_STATE_STARTED` | Checked, not yet accepted |
| `ORDER_STATE_PLACED` | Accepted by broker |
| `ORDER_STATE_CANCELED` | Canceled by client |
| `ORDER_STATE_PARTIAL` | Partially executed |
| `ORDER_STATE_FILLED` | Fully executed |
| `ORDER_STATE_REJECTED` | Rejected by broker |
| `ORDER_STATE_EXPIRED` | Expired |
| `ORDER_STATE_REQUEST_ADD` | Being placed |
| `ORDER_STATE_REQUEST_MODIFY` | Being modified |
| `ORDER_STATE_REQUEST_CANCEL` | Being deleted |

## ENUM_ORDER_TYPE_FILLING

| Value | Description | Notes |
|-------|-------------|-------|
| `ORDER_FILLING_FOK` | Fill or Kill | Full volume or cancel |
| `ORDER_FILLING_IOC` | Immediate or Cancel | Partial fill allowed, remainder canceled |
| `ORDER_FILLING_BOC` | Book or Cancel (passive) | Must rest in book; limit/stop-limit only |
| `ORDER_FILLING_RETURN` | Return partial | Default for pending orders; disabled in Market Execution |

**Filling compatibility matrix:**

| Execution Mode | FOK | IOC | RETURN |
|---------------|-----|-----|--------|
| Instant / Request | (always) | (always) |  |
| Market Execution | per symbol | per symbol | ✗ |
| Exchange Execution | per symbol | per symbol |  |

> Check `SymbolInfoInteger(sym, SYMBOL_FILLING_MODE)` before sending.
> Always use `ORDER_FILLING_RETURN` for pending orders regardless of execution mode.

## ENUM_ORDER_TYPE_TIME

| Value | Description |
|-------|-------------|
| `ORDER_TIME_GTC` | Good till canceled |
| `ORDER_TIME_DAY` | Good till end of trading day |
| `ORDER_TIME_SPECIFIED` | Good till explicit `expiration` datetime |
| `ORDER_TIME_SPECIFIED_DAY` | Good till 23:59:59 of specified day |

## ENUM_ORDER_REASON

`ORDER_REASON_CLIENT` · `ORDER_REASON_MOBILE` · `ORDER_REASON_WEB` ·
`ORDER_REASON_EXPERT` (EA/script) · `ORDER_REASON_SL` · `ORDER_REASON_TP` ·
`ORDER_REASON_SO` (Stop Out)
