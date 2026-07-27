# Timeseries Copy API — Indexing, Signatures, and Semantics

## Indexing Rules

- Timeseries are logically reversed: newest bar is index `0`, previous closed
  bar is index `1`
- Plain arrays are left-to-right by default. Call `ArraySetAsSeries(array, true)`
  explicitly when you want timeseries-style indexing
- `CopyRates`, `CopyOpen`, `CopyHigh`, `CopyLow`, `CopyClose`, `CopyTime`,
  `CopyTickVolume`, `CopyRealVolume`, `CopySpread`, and `CopyBuffer` all count
  `start_pos=0` from the current bar backward
- Copying ignores the recipient array's logical direction for physical layout:
  the oldest copied element is stored at the start of memory. `ArraySetAsSeries()`
  changes how you read the array, not how the bytes are copied
- Tick arrays are different: `CopyTicks*()` returns ticks oldest-to-newest,
  so tick index `0` is the oldest copied tick

## Core Copy Signatures

```mql5
int CopyRates(string symbol, ENUM_TIMEFRAMES timeframe, int start_pos, int count, MqlRates rates_array[]);
int CopyOpen(string symbol, ENUM_TIMEFRAMES timeframe, int start_pos, int count, double open_array[]);
int CopyHigh(string symbol, ENUM_TIMEFRAMES timeframe, int start_pos, int count, double high_array[]);
int CopyLow(string symbol, ENUM_TIMEFRAMES timeframe, int start_pos, int count, double low_array[]);
int CopyClose(string symbol, ENUM_TIMEFRAMES timeframe, int start_pos, int count, double close_array[]);
int CopyTime(string symbol, ENUM_TIMEFRAMES timeframe, int start_pos, int count, datetime time_array[]);
int CopyTickVolume(string symbol, ENUM_TIMEFRAMES timeframe, int start_pos, int count, long volume_array[]);
int CopyRealVolume(string symbol, ENUM_TIMEFRAMES timeframe, int start_pos, int count, long volume_array[]);
int CopySpread(string symbol, ENUM_TIMEFRAMES timeframe, int start_pos, int count, int spread_array[]);
int CopySeries(string symbol, ENUM_TIMEFRAMES timeframe, int start_pos, int count, ulong rates_mask, void& array1[], void& array2[] ...);
```

## Cheap Scalar Lookups

```mql5
int    iBars(const string symbol, ENUM_TIMEFRAMES timeframe);
int    iBarShift(const string symbol, ENUM_TIMEFRAMES timeframe, datetime time, bool exact=false);
double iOpen(const string symbol, ENUM_TIMEFRAMES timeframe, int shift);
double iHigh(const string symbol, ENUM_TIMEFRAMES timeframe, int shift);
double iLow(const string symbol, ENUM_TIMEFRAMES timeframe, int shift);
double iClose(const string symbol, ENUM_TIMEFRAMES timeframe, int shift);
int    iHighest(const string symbol, ENUM_TIMEFRAMES timeframe, ENUM_SERIESMODE type, int count=WHOLE_ARRAY, int start=0);
int    iLowest(const string symbol, ENUM_TIMEFRAMES timeframe, ENUM_SERIESMODE type, int count=WHOLE_ARRAY, int start=0);
```

## Array Sizing Rules

| Situation | Recommended target | Why |
|-----------|-------------------|-----|
| Unknown result size | Dynamic array | Docs recommend dynamic arrays so the terminal can resize to the returned count |
| Fixed known count | Static array | Avoids unnecessary reallocations |
| Copying into indicator buffer | Indicator buffer is fine | Partial copying is allowed for true indicator buffers |
| Partial copy into a non-indicator array | Intermediate array first | `CopyBuffer()` docs explicitly recommend staging, then element-wise placement |

## Tick-Copy Specifics

```mql5
int CopyTicks(string symbol, MqlTick& ticks_array[], uint flags=COPY_TICKS_ALL, ulong from=0, uint count=0);
int CopyTicksRange(const string symbol, MqlTick& ticks_array[], uint flags=COPY_TICKS_ALL, ulong from_msc=0, ulong to_msc=0);
```

- `COPY_TICKS_INFO` filters bid/ask changes
- `COPY_TICKS_TRADE` filters last/volume changes
- `COPY_TICKS_ALL` is the simplest default and returns full tick state with
  unchanged fields backfilled from the previous tick
- In indicators, `CopyTicks()` cannot block the shared symbol thread waiting
  for sync; return and retry on the next `OnCalculate()`
- In EAs and scripts, `CopyTicks()` can wait up to about 45 seconds for
  synchronisation and may still return partial results by timeout
- `CopyTicksRange()` on a static array can raise `ERR_HISTORY_SMALL_BUFFER (4407)`
  if the destination is too small

## History Availability Gotchas

- Data can exist in terminal storage but still be unavailable at the exact
  moment you ask for it because timeseries rebuilds and indicator recalculations
  are asynchronous
- If data are outside `TERMINAL_MAXBARS`, copy functions can return `-1`
- In indicators, do not spin in blocking loops waiting for same-symbol,
  same-period history; exit the event handler and retry on the next call
- Use `SeriesInfoInteger(symbol, period, SERIES_FIRSTDATE, ...)` when you need
  to reason about whether history is actually present
