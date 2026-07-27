# Symbol Info Properties and Flag Combinations

## Key ENUM_SYMBOL_INFO_INTEGER Properties

| Identifier | Description | Type |
|------------|-------------|------|
| `SYMBOL_SELECT` | Symbol selected in Market Watch | bool |
| `SYMBOL_VISIBLE` | Symbol visible in Market Watch | bool |
| `SYMBOL_EXIST` | Symbol exists in terminal database | bool |
| `SYMBOL_DIGITS` | Decimal digits | int |
| `SYMBOL_SPREAD` | Current spread in points | int |
| `SYMBOL_SPREAD_FLOAT` | Floating spread flag | bool |
| `SYMBOL_TICKS_BOOKDEPTH` | Depth of Market levels available | int |
| `SYMBOL_TRADE_CALC_MODE` | Contract price calculation mode | `ENUM_SYMBOL_CALC_MODE` |
| `SYMBOL_TRADE_MODE` | Allowed trading mode | `ENUM_SYMBOL_TRADE_MODE` |
| `SYMBOL_TRADE_EXEMODE` | Execution mode | `ENUM_SYMBOL_TRADE_EXECUTION` |
| `SYMBOL_FILLING_MODE` | Allowed fill policies (bitmask) | int |
| `SYMBOL_EXPIRATION_MODE` | Allowed pending-order expirations (bitmask) | int |
| `SYMBOL_ORDER_MODE` | Allowed order types (bitmask) | int |
| `SYMBOL_ORDER_GTC_MODE` | SL/TP lifetime mode for GTC symbols | `ENUM_SYMBOL_ORDER_GTC_MODE` |
| `SYMBOL_SWAP_MODE` | Swap calculation model | `ENUM_SYMBOL_SWAP_MODE` |
| `SYMBOL_SWAP_ROLLOVER3DAYS` | Triple-swap weekday | `ENUM_DAY_OF_WEEK` |
| `SYMBOL_TRADE_STOPS_LEVEL` | Min points from close for Stop orders | int |
| `SYMBOL_TRADE_FREEZE_LEVEL` | Freeze distance for trade operations | int |
| `SYMBOL_CUSTOM` | Synthetic custom symbol flag | bool |
| `SYMBOL_SECTOR` | Economic sector | `ENUM_SYMBOL_SECTOR` |
| `SYMBOL_INDUSTRY` | Industry / branch | `ENUM_SYMBOL_INDUSTRY` |
| `SYMBOL_START_TIME` | Symbol trade start time | datetime |
| `SYMBOL_EXPIRATION_TIME` | Symbol trade end time | datetime |

## Key ENUM_SYMBOL_INFO_DOUBLE Properties

| Identifier | Description |
|------------|-------------|
| `SYMBOL_BID` / `SYMBOL_ASK` | Current Bid / Ask |
| `SYMBOL_LAST` | Last trade price |
| `SYMBOL_POINT` | Minimal price change (1 point) |
| `SYMBOL_TRADE_TICK_SIZE` | Minimal price change (1 tick) |
| `SYMBOL_TRADE_TICK_VALUE` | Tick value in deposit currency |
| `SYMBOL_TRADE_TICK_VALUE_PROFIT` | Tick value for profit calculation |
| `SYMBOL_TRADE_TICK_VALUE_LOSS` | Tick value for loss calculation |
| `SYMBOL_TRADE_CONTRACT_SIZE` | Contract size in base currency |
| `SYMBOL_VOLUME_MIN` | Minimum order volume |
| `SYMBOL_VOLUME_MAX` | Maximum order volume |
| `SYMBOL_VOLUME_STEP` | Volume increment step |
| `SYMBOL_VOLUME_LIMIT` | Max aggregate directional volume |
| `SYMBOL_MARGIN_INITIAL` | Initial margin per lot |
| `SYMBOL_MARGIN_MAINTENANCE` | Maintenance margin per lot |
| `SYMBOL_SWAP_LONG` / `SYMBOL_SWAP_SHORT` | Swap rates |

## Key ENUM_SYMBOL_INFO_STRING Properties

`SYMBOL_CURRENCY_BASE` · `SYMBOL_CURRENCY_PROFIT` · `SYMBOL_CURRENCY_MARGIN` · `SYMBOL_DESCRIPTION` · `SYMBOL_PATH`

## ENUM_SYMBOL_TRADE_MODE

| Value | Description |
|-------|-------------|
| `SYMBOL_TRADE_MODE_DISABLED` | Trade is disabled |
| `SYMBOL_TRADE_MODE_LONGONLY` | Only long positions allowed |
| `SYMBOL_TRADE_MODE_SHORTONLY` | Only short positions allowed |
| `SYMBOL_TRADE_MODE_CLOSEONLY` | Only closing operations allowed |
| `SYMBOL_TRADE_MODE_FULL` | No trade restrictions |

## `SYMBOL_EXPIRATION_MODE` Flags

Combine with `|`; test with `(flags & mode) == mode`.

| Flag | Value | Meaning |
|------|-------|---------|
| `SYMBOL_EXPIRATION_GTC` | 1 | Valid until explicitly canceled |
| `SYMBOL_EXPIRATION_DAY` | 2 | Valid until end of trading day |
| `SYMBOL_EXPIRATION_SPECIFIED` | 4 | Exact expiration time allowed |
| `SYMBOL_EXPIRATION_SPECIFIED_DAY` | 8 | Exact expiration date allowed |

## ENUM_SYMBOL_ORDER_GTC_MODE

| Value | Description |
|-------|-------------|
| `SYMBOL_ORDERS_GTC` | Pending orders and SL/TP remain until explicitly canceled |
| `SYMBOL_ORDERS_DAILY` | Pending orders and SL/TP deleted at end of day |
| `SYMBOL_ORDERS_DAILY_EXCLUDING_STOPS` | Pending orders deleted daily; SL/TP preserved |

## `SYMBOL_FILLING_MODE` Flags

Combine with `|`; test with `(flags & mode) == mode`.

| Flag | Value | Meaning |
|------|-------|---------|
| `SYMBOL_FILLING_FOK` | 1 | Fill or Kill |
| `SYMBOL_FILLING_IOC` | 2 | Immediate or Cancel |
| `SYMBOL_FILLING_BOC` | 4 | Book or Cancel; passive only |

`ORDER_FILLING_RETURN` has no `SYMBOL_FILLING_*` flag. It is available except under `SYMBOL_TRADE_EXECUTION_MARKET`.

## `SYMBOL_ORDER_MODE` Flags

Combine with `|`; test with `(flags & mode) == mode`.

| Flag | Value | Meaning |
|------|-------|---------|
| `SYMBOL_ORDER_MARKET` | 1 | Market orders allowed |
| `SYMBOL_ORDER_LIMIT` | 2 | Limit orders allowed |
| `SYMBOL_ORDER_STOP` | 4 | Stop orders allowed |
| `SYMBOL_ORDER_STOP_LIMIT` | 8 | Stop-limit orders allowed |
| `SYMBOL_ORDER_SL` | 16 | Stop Loss placement allowed |
| `SYMBOL_ORDER_TP` | 32 | Take Profit placement allowed |
| `SYMBOL_ORDER_CLOSEBY` | 64 | Close By allowed on hedging accounts |

> Lot-size normalisation: `MathRound(lots / step) * step` where `step = SymbolInfoDouble(sym, SYMBOL_VOLUME_STEP)`.
> Tick-value check: `SYMBOL_TRADE_TICK_VALUE` may vary by execution mode, so query it live before lot sizing.
