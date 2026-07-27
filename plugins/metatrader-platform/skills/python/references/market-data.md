# Market Data

Self-written reference for reading symbols, ticks, bars, and depth-of-market data through the `MetaTrader5` Python module.

---

## Symbol Discovery

Core functions:

- `symbols_total()`
- `symbols_get()`
- `symbol_info()`
- `symbol_select()`
- `symbol_info_tick()`

Use `symbols_get()` when you need filtered discovery. The group filter supports wildcard-style matching and sequential exclusions.

Useful patterns:

- Include all USD symbols: `group="*USD*"`
- Include everything, then exclude EUR symbols: `group="*, !EUR"`

Before relying on a symbol for trading or market data, confirm:

- it exists
- it is selected or visible when required
- its contract and volume constraints are sensible for the intended workflow

`symbol_select()` is especially important in automation when a symbol is not already visible in Market Watch.

---

## Tick And Bar Retrieval

Bar functions:

- `copy_rates_from()`
- `copy_rates_from_pos()`
- `copy_rates_range()`

Tick functions:

- `copy_ticks_from()`
- `copy_ticks_range()`

Selection guidance:

- Use `copy_rates_from()` when anchoring from a specific start time and count
- Use `copy_rates_from_pos()` when you want bars by relative index from the current bar
- Use `copy_rates_range()` when the job is naturally bounded by a time window
- Use `copy_ticks_from()` for forward retrieval from a start point
- Use `copy_ticks_range()` for an explicit historical interval

---

## UTC Rule

MT5 stores bar and tick times in UTC. Python datetime objects should therefore be created in UTC for all time-bounded calls.

Practical rule:

- Build request timestamps in UTC
- Treat returned epoch-based times as UTC
- Convert to local time only at the presentation layer

If this rule is ignored, backfills and research jobs will silently shift the requested interval.

---

## pandas Conversion Pattern

Most data-returning MT5 calls map cleanly into a DataFrame.

Standard pattern:

```python
import pandas as pd

rates = mt5.copy_rates_range(symbol, timeframe, date_from, date_to)
if rates is None:
    raise RuntimeError(f"copy_rates_range failed: {mt5.last_error()}")

df = pd.DataFrame(rates)
df["time"] = pd.to_datetime(df["time"], unit="s", utc=True)
```

For tick data, also preserve `time_msc` when event ordering matters.

---

## Market Depth

Depth-of-market functions:

- `market_book_add()`
- `market_book_get()`
- `market_book_release()`

Workflow:

1. Subscribe with `market_book_add(symbol)`
2. Poll current book snapshots with `market_book_get(symbol)`
3. Release the subscription with `market_book_release(symbol)`

This is useful for order book inspection, but it should be treated as a live terminal feature, not a historical market-depth archive.

---

## Practical Data Checks

Before turning retrieved data into strategy inputs, validate:

- non-empty response
- expected symbol
- expected timeframe
- monotonic timestamps
- no unintended timezone conversion
- plausible spread and volume fields for the broker

The MT5 module is close to the terminal, which is useful, but it means data quality assumptions should be checked in your own code.

---

## CHUNK PY-3 — Function Signatures: Market Data

```python
# Symbol discovery
mt5.symbols_total()                            # → int (all symbols including hidden)
mt5.symbols_get()                              # → tuple of SymbolInfo
mt5.symbols_get(group="*USD*")                 # → filtered by group mask
mt5.symbol_info(symbol)                        # → SymbolInfo named tuple or None
mt5.symbol_info_tick(symbol)                   # → Tick named tuple or None
mt5.symbol_select(symbol, enable=True)         # → bool; adds/removes from MarketWatch

# Bars
mt5.copy_rates_from(symbol, timeframe, date_from, count)
mt5.copy_rates_from_pos(symbol, timeframe, start_pos, count)
mt5.copy_rates_range(symbol, timeframe, date_from, date_to)
# All return numpy array of (time, open, high, low, close, tick_volume, spread, real_volume)
# or None on failure

# Ticks
mt5.copy_ticks_from(symbol, date_from, count, flags)
mt5.copy_ticks_range(symbol, date_from, date_to, flags)
# Return numpy array of (time, bid, ask, last, volume, time_msc, flags, volume_real)

# Market depth
mt5.market_book_add(symbol)      # Subscribe to DOM updates → bool
mt5.market_book_get(symbol)      # Get snapshot → tuple of BookInfo dicts; must subscribe first
mt5.market_book_release(symbol)  # Unsubscribe → bool
```

**BookInfo dict fields:** `type` (1=bid, 2=ask), `price`, `volume`, `volume_dbl`

---

## CHUNK PY-4 — Enumerations: Timeframes, Ticks

**TIMEFRAME enumeration (use `mt5.TIMEFRAME_*`):**

| Constant | Value |
|----------|-------|
| TIMEFRAME_M1 | 1 min |
| TIMEFRAME_M2 | 2 min |
| TIMEFRAME_M3 | 3 min |
| TIMEFRAME_M4 | 4 min |
| TIMEFRAME_M5 | 5 min |
| TIMEFRAME_M6 | 6 min |
| TIMEFRAME_M10 | 10 min |
| TIMEFRAME_M12 | 12 min |
| TIMEFRAME_M15 | 15 min |
| TIMEFRAME_M20 | 20 min |
| TIMEFRAME_M30 | 30 min |
| TIMEFRAME_H1 | 1 hour |
| TIMEFRAME_H2 | 2 hours |
| TIMEFRAME_H3 | 3 hours |
| TIMEFRAME_H4 | 4 hours |
| TIMEFRAME_H6 | 6 hours |
| TIMEFRAME_H8 | 8 hours |
| TIMEFRAME_H12 | 12 hours |
| TIMEFRAME_D1 | 1 day |
| TIMEFRAME_W1 | 1 week |
| TIMEFRAME_MN1 | 1 month |

**COPY_TICKS enumeration (flags param for `copy_ticks_*`):**

| Constant | Description |
|----------|-------------|
| `mt5.COPY_TICKS_ALL` | All ticks |
| `mt5.COPY_TICKS_INFO` | Ticks with Bid and/or Ask changes |
| `mt5.COPY_TICKS_TRADE` | Ticks with Last and/or Volume changes |

**TICK_FLAG bit values (in returned tick `flags` field):**

| Constant | Meaning |
|----------|---------|
| `mt5.TICK_FLAG_BID` | Bid price changed |
| `mt5.TICK_FLAG_ASK` | Ask price changed |
| `mt5.TICK_FLAG_LAST` | Last price changed |
| `mt5.TICK_FLAG_VOLUME` | Volume changed |
| `mt5.TICK_FLAG_BUY` | Last Buy price changed |
| `mt5.TICK_FLAG_SELL` | Last Sell price changed |

**`symbols_get()` group filter syntax:**
- `group="*USD*"` — all symbols with USD in name
- `group="*, !EUR"` — all symbols except those containing EUR
- Multiple comma-separated conditions applied sequentially; prefix `!` for exclusion

**References:**
- `docs/mql5_com_-_docs_python_metatrader5/08_mt5symbolstotal_py.md`
- `docs/mql5_com_-_docs_python_metatrader5/09_mt5symbolsget_py.md`
- `docs/mql5_com_-_docs_python_metatrader5/10_mt5symbolinfo_py.md`
- `docs/mql5_com_-_docs_python_metatrader5/11_mt5symbolinfotick_py.md`
- `docs/mql5_com_-_docs_python_metatrader5/12_mt5symbolselect_py.md`
- `docs/mql5_com_-_docs_python_metatrader5/13_mt5marketbookadd_py.md`
- `docs/mql5_com_-_docs_python_metatrader5/14_mt5marketbookget_py.md`
- `docs/mql5_com_-_docs_python_metatrader5/15_mt5marketbookrelease_py.md`
- `docs/mql5_com_-_docs_python_metatrader5/16_mt5copyratesfrom_py.md`
- `docs/mql5_com_-_docs_python_metatrader5/17_mt5copyratesfrompos_py.md`
- `docs/mql5_com_-_docs_python_metatrader5/18_mt5copyratesrange_py.md`
- `docs/mql5_com_-_docs_python_metatrader5/19_mt5copyticksfrom_py.md`
- `docs/mql5_com_-_docs_python_metatrader5/20_mt5copyticksrange_py.md`