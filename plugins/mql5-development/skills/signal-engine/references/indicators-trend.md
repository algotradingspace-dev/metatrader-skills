# Trend-Following and Volatility Indicator Handles

Use the generic lifecycle: create handle, guard `INVALID_HANDLE`, wait for
`BarsCalculated(handle) > 0`, `CopyBuffer()` the needed lines, then
`IndicatorRelease(handle)` when done.

## Core Trend/Volatility Signatures and Buffer Maps

| Indicator | Signature skeleton | Buffers | Implementation note |
|-----------|-------------------|---------|---------------------|
| `iMA` | `iMA(symbol, period, ma_period, ma_shift, ma_method, applied_price)` | `0` | `applied_price` can be a price enum or another indicator handle |
| `iAMA` | `iAMA(symbol, period, ama_period, fast_ma_period, slow_ma_period, ama_shift, applied_price)` | `0` | Adaptive MA; same one-buffer read pattern as `iMA` |
| `iDEMA` | `iDEMA(symbol, period, ma_period, ma_shift, applied_price)` | `0` | Overlay MA variant |
| `iFrAMA` | `iFrAMA(symbol, period, ma_period, ma_shift, applied_price)` | `0` | Fractal adaptive overlay |
| `iTEMA` | `iTEMA(symbol, period, ma_period, ma_shift, applied_price)` | `0` | Triple EMA overlay |
| `iVIDyA` | `iVIDyA(symbol, period, cmo_period, ema_period, ma_shift, applied_price)` | `0` | Variable dynamic average |
| `iATR` | `iATR(symbol, period, ma_period)` | `0` | Volatility series; common for SL and position sizing |
| `iADX` | `iADX(symbol, period, adx_period)` | `0=MAIN_LINE`, `1=PLUSDI_LINE`, `2=MINUSDI_LINE` | Copy all 3 if your entry uses DI alignment, not just ADX strength |
| `iADXWilder` | `iADXWilder(symbol, period, adx_period)` | `0=MAIN_LINE`, `1=PLUSDI_LINE`, `2=MINUSDI_LINE` | Same buffer contract as `iADX` |
| `iBands` | `iBands(symbol, period, bands_period, bands_shift, deviation, applied_price)` | `0=BASE_LINE`, `1=UPPER_BAND`, `2=LOWER_BAND` | Shifted bands usually need negative shift handling in CopyBuffer |
| `iEnvelopes` | `iEnvelopes(symbol, period, ma_period, ma_shift, ma_method, applied_price, deviation)` | `0=UPPER_LINE`, `1=LOWER_LINE` | `ma_shift` is part of both plotting and copy alignment |
| `iIchimoku` | `iIchimoku(symbol, period, tenkan_sen, kijun_sen, senkou_span_b)` | `0=TENKAN`, `1=KIJUN`, `2=SENKOU_A`, `3=SENKOU_B`, `4=CHIKOU` | Copy Senkou spans with negative shift; Chikou is stored shifted |
| `iSAR` | `iSAR(symbol, period, step, maximum)` | `0` | One-buffer stop-and-reverse line |
| `iStdDev` | `iStdDev(symbol, period, ma_period, ma_shift, ma_method, applied_price)` | `0` | Volatility overlay, single-buffer |

## Minimal Closed-Bar Pattern

```mql5
int handle = iMA(_Symbol, PERIOD_H1, 50, 0, MODE_EMA, PRICE_CLOSE);
if(handle == INVALID_HANDLE) return false;

double ma_values[];
ArraySetAsSeries(ma_values, true);
if(CopyBuffer(handle, 0, 0, 3, ma_values) <= 0) return false;

double current_bar = ma_values[0];
double last_closed = ma_values[1];
```

## Terminal-Help Interpretation Notes

- Trend-family terminal-help pages are complementary to the API docs: they
  explain when the indicator is structurally useful, not how to allocate or
  copy the handle
- `ADX` / `ADX Wilder`: treat `MAIN_LINE` as trend-strength context and `+DI`
  vs `-DI` as direction; Wilder's "point of extremum" rule is a practical
  confirmation filter after a DI crossover
- `MA`, `AMA`, `DEMA`, `FrAMA`, `TEMA`, `VIDyA`: all are moving-average
  overlays, but with different responsiveness tradeoffs
- `Bands`, `Envelopes`, `StdDev`, `ATR`: better as filters and stop/target
  scalers than as standalone entry triggers
- `Ichimoku`: use the cloud for regime gating while reading Tenkan/Kijun
  crossovers from synchronised closed bars
- `SAR`: safer as an exit-management or stop-update tool than as a primary
  entry signal

## Family Gotchas

- If the indicator exposes shifted lines (`iBands`, `iEnvelopes`, `iIchimoku`),
  the docs' examples use negative offsets in `CopyBuffer()` to keep plotted
  and copied values aligned
- If reading a crossover on a multi-line indicator, copy every required line
  in the same pass and compare matching closed-bar indexes
- For signal logic, prefer closed-bar reads (`[1]`) unless you explicitly want
  intrabar repainting behaviour
