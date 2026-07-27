# Indicator Handle Lifecycle and the `prev_calculated` Delta-Copy

## Universal Handle Workflow

```mql5
int handle = iMA(_Symbol, PERIOD_H1, 20, 0, MODE_EMA, PRICE_CLOSE);
if(handle == INVALID_HANDLE) {
   PrintFormat("Failed to create handle, error %d", GetLastError());
   return INIT_FAILED;
}

int calculated = BarsCalculated(handle);
if(calculated <= 0) return 0;

double values[];
ArraySetAsSeries(values, true);
if(CopyBuffer(handle, 0, 0, 3, values) <= 0) return 0;

// On shutdown or when replacing the handle:
IndicatorRelease(handle);
handle = INVALID_HANDLE;
```

## Generic Creation and Reflection APIs

```mql5
int IndicatorCreate(string symbol, ENUM_TIMEFRAMES period, ENUM_INDICATOR indicator_type,
                    int parameters_cnt=0, const MqlParam& parameters_array[]=NULL);
int IndicatorParameters(int indicator_handle, ENUM_INDICATOR& indicator_type, MqlParam& parameters[]);
bool IndicatorRelease(int indicator_handle);
int BarsCalculated(int indicator_handle);
int CopyBuffer(int indicator_handle, int buffer_num, int start_pos, int count, double buffer[]);
```

- Use `IndicatorCreate()` when you need generic factory logic or to instantiate
  `IND_CUSTOM` / runtime-selected indicator types
- Use `IndicatorParameters()` when debugging or introspecting a handle you did
  not construct inline
- Always guard `INVALID_HANDLE` before any `CopyBuffer()` or `BarsCalculated()` call
- Release stale handles in `OnDeinit()` or before rebuilding them on
  symbol/timeframe/input changes

## `prev_calculated` Delta-Copy Pattern

This is where many EAs and custom indicators quietly go wrong. If you recopy
the entire buffer on every `OnCalculate()`, or if you forget the extra bar on
incremental updates, you get misaligned signals, redundant work, and false
crossover logic.

```mql5
int OnCalculate(const int rates_total,
                const int prev_calculated,
                const datetime &time[],
                const double &open[],
                const double &high[],
                const double &low[],
                const double &close[],
                const long &tick_volume[],
                const long &volume[],
                const int &spread[])
{
   int calculated = BarsCalculated(handle);
   if(calculated <= 0) return 0;
   int to_copy;
   if(prev_calculated <= 0 || prev_calculated > rates_total || calculated != bars_calculated)
      to_copy = MathMin(calculated, rates_total);
   else
      to_copy = (rates_total - prev_calculated) + 1;
   if(CopyBuffer(handle, 0, 0, to_copy, buffer) <= 0) return 0;
   bars_calculated = calculated;
   return rates_total;
}
```

Why the extra `+1` matters:
- The current bar can change between calls, so the newest already-known slot
  still needs refresh
- `prev_calculated == rates_total` does not mean bar `0` is stable
- If history changed or the handle recalculated a different bar count, fall
  back to a wider copy instead of assuming a clean one-bar increment

## CopyBuffer Usage Rules That Reduce Signal Bugs

- `buffer_num` must match the indicator line index: `0` for single-line,
  `0/1` for `iMACD`, `0/1/2` for `iBands` or `iADX` families
- `start_pos=0` means current bar value, not the last closed bar. For
  closed-bar logic, read index `1` after copying enough elements
- If `CopyBuffer()` returns `<= 0`, treat the data as not ready yet, not as
  a valid zero signal
- In custom indicators, compare `BarsCalculated(handle)` to `rates_total`
  before assuming the external indicator is ready
- If you only need closed bars in an EA, copy at least 2 values and reference
  `[1]` for the latest fully closed bar
