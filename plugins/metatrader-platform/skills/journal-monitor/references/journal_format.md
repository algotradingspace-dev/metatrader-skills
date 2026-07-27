# MT5 Journal Log Format Reference

## File encoding

MT5 writes journal logs as **UTF-16 LE with BOM** (`\xff\xfe` prefix). Some builds
write plain UTF-8. The parser auto-detects the BOM and falls back to UTF-8, then
Latin-1 on error.

## Filename convention

```
JournalLog-<account_id>-<YYYYMMDD>.log
```

Example: `JournalLog-ACCOUNT_ID-20260423.log`

The parser's `FILENAME_RE` requires this format; files not matching it are skipped
when processing directories.

## Line format

Tab-separated columns:

```
<code>\t<level>\t<HH:MM:SS.mmm>\t<source>\t<message>
```

- `code` — a short opaque identifier MT5 uses internally (e.g. `RO`, `LQ`, `JL`)
- `level` — `0` = info, `1` = warning, `2` = error
- `time` — time-of-day, millisecond precision. **The date comes from the filename.**
- `source` — `Trades`, `Network`, `Experts`, `Indicators`, `Terminal`, etc.
- `message` — free-form message, usually starts with `'<account>': <text>`

## Key message patterns (Trades)

### Pending order placement

```
'ACCOUNT_ID': buy stop 0.16 XAUUSD at 4772.25 sl: 4762.25 tp: 4782.25
'ACCOUNT_ID': accepted buy stop 0.16 XAUUSD at 4772.25 sl: 4762.25 tp: 4782.25
'ACCOUNT_ID': order #ORDER_ID buy stop 0.16 / 0.16 XAUUSD at 4772.25 done in 4.105 ms
```

Three log lines for one request: request -> accept -> done. The "done in X ms"
line is the one with the round-trip latency. Accepted timestamps are roughly
the broker ack time.

### Market order / deal (position open)

```
'ACCOUNT_ID': deal #DEAL_ID sell 0.16 XAUUSD at 4682.30 done (based on order #ORDER_ID)
```

A `deal` is the actual execution. For stop/limit orders triggered by market
movement, this appears without a preceding `market buy/sell` request — it's the
trigger firing.

### Position close

MT5 logs position closes as another `deal` in the opposite direction,
referencing a different order id. The same position has two deals that share
a position id (visible in the trade history report, not the journal).

To detect round trips purely from the journal, match deals on the same symbol
with equal volume and opposite sides, within a short time window. That's what
`fast_sl_seconds` does in the analyser.

### Modify (SL/TP change)

```
'ACCOUNT_ID': modify #ORDER_ID sell 0.16 XAUUSD sl: 4694.22, tp: 4674.22 -> sl: 4692.30, tp: 4672.30
'ACCOUNT_ID': accepted modify #ORDER_ID sell 0.16 XAUUSD sl: 4694.22, tp: 4674.22 -> sl: 4692.30, tp: 4672.30
'ACCOUNT_ID': modify #ORDER_ID sell 0.16 XAUUSD -> sl: 4692.30, tp: 4672.30 done in 8.279 ms
```

For trailing-stop EAs this is the hot path — every tick that moves the trail
generates one of these cycles. Slow modify latency is expensive here.

### Cancel

```
'ACCOUNT_ID': cancel order #ORDER_ID sell stop 0.16 XAUUSD at 4668.51 sl: 4678.51 tp: 4658.51
'ACCOUNT_ID': accepted cancel order #ORDER_ID sell stop 0.16 XAUUSD at 4668.51 sl: 4678.51 tp: 4658.51
'ACCOUNT_ID': cancel #ORDER_ID sell stop 0.16 XAUUSD at market done in 13.093 ms
```

### Failed / rejected

```
'ACCOUNT_ID': failed market buy 0.64 XAUUSD, close #TICKET_ID sell 0.64 XAUUSD 4682.84 [Modification failed due to order or position being close to market]
```

Common failure reasons:
- `Modification failed due to order or position being close to market` — SL/TP
  inside broker's minimum stop level (Stops Level)
- `requote` — broker wants a new price confirmation
- `off quotes` — no quotes for that symbol at that moment
- `not enough money` — margin insufficient
- `invalid stops` — SL/TP on the wrong side of market or violates stops level

## Key message patterns (Network)

### Connection drop

```
'ACCOUNT_ID': connection to <broker-server> lost
```

Always a Network source line. The server name follows "connection to".

### Reauthorization

```
'ACCOUNT_ID': authorized on <broker-server> through Access Server - NY1 (ping: 0.65 ms, build 5660)
'ACCOUNT_ID': previous successful authorization performed from CLIENT_IP_ADDRESS on 2026.04.23 11:30:26
'ACCOUNT_ID': terminal synchronized with <broker-company>: 0 positions, 0 orders, 3165 symbols, 0 spreads
'ACCOUNT_ID': trading has been enabled - hedging mode
```

Drop-reauth cycles take ~2 seconds on stable links but can stretch much longer
on flaky connections. The analyser counts reauths separately and groups drops
within 5 minutes into a single "cluster" for noise reduction.

### Network scanning

```
'ACCOUNT_ID': scanning network for access points
'ACCOUNT_ID': scanning network finished
```

Informational only — normal MT5 background behaviour, does not indicate a
problem.

## Important gotchas

1. **Dates come from filenames.** Journal lines only carry time-of-day. If a
   session crosses midnight, MT5 rotates into the next file. The parser uses
   the filename date strictly.

2. **MT5 points vs price units.** XAUUSD has 2 digits -> 1 point = 0.01 USD.
   A 10-USD SL distance = 1000 points. The analyser records price fields as
   raw floats from the journal; compute points by multiplying the diff by 100
   for 2-digit instruments, 10,000 for 4-digit FX, 100,000 for 5-digit FX.

3. **`done in X ms` is round-trip time**, not broker-side processing. It
   includes the EA -> terminal -> broker -> terminal round trip. Network latency
   to the broker is usually the dominant factor.

4. **Ping != fill latency.** The `(ping: 0.65 ms)` in authorisation messages
   is a control-channel ping; actual order round-trip times are much higher
   because they include broker-side matching.

5. **Sym-suffix conventions.** Many brokers append `p`, `.raw`, `.r`, or `.m`
   to symbol names to distinguish account types (premium/raw/micro). The
   parser treats these as separate symbols because they often have different
   spreads and sometimes different liquidity pools.
