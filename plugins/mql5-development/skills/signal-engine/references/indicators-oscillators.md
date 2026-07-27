# Oscillator and Momentum Indicator Handles

All follow the same handle pattern. The main implementation decision is
whether you need a single oscillator line or multiple synchronised buffers
for crossovers.

| Indicator | Signature skeleton | Buffers | Implementation note |
|-----------|-------------------|---------|---------------------|
| `iRSI` | `iRSI(symbol, period, ma_period, applied_price)` | `0` | Basic one-buffer momentum/mean-reversion read |
| `iCCI` | `iCCI(symbol, period, ma_period, applied_price)` | `0` | One buffer |
| `iMomentum` | `iMomentum(symbol, period, mom_period, applied_price)` | `0` | One buffer |
| `iWPR` | `iWPR(symbol, period, calc_period)` | `0` | One buffer |
| `iDeMarker` | `iDeMarker(symbol, period, ma_period)` | `0` | One buffer |
| `iTriX` | `iTriX(symbol, period, ma_period, applied_price)` | `0` | One buffer |
| `iBullsPower` | `iBullsPower(symbol, period, ma_period)` | `0` | One buffer |
| `iBearsPower` | `iBearsPower(symbol, period, ma_period)` | `0` | One buffer |
| `iMACD` | `iMACD(symbol, period, fast_ema_period, slow_ema_period, signal_period, applied_price)` | `0=MAIN_LINE`, `1=SIGNAL_LINE` | Copy both buffers before testing line cross or histogram slope |
| `iStochastic` | `iStochastic(symbol, period, Kperiod, Dperiod, slowing, ma_method, price_field)` | `0=MAIN_LINE`, `1=SIGNAL_LINE` | Use `MAIN_LINE` / `SIGNAL_LINE` constants for readability |
| `iRVI` | `iRVI(symbol, period, ma_period)` | `0=MAIN_LINE`, `1=SIGNAL_LINE` | Same two-line read pattern as Stochastic/MACD |
| `iOsMA` | `iOsMA(symbol, period, fast_ema_period, slow_ema_period, signal_period, applied_price)` | `0` | One-buffer derivative of MACD |

## Two-Line Crossover Pattern

```mql5
double main_line[];
double signal_line[];
ArraySetAsSeries(main_line, true);
ArraySetAsSeries(signal_line, true);

if(CopyBuffer(handle, MAIN_LINE, 0, 3, main_line) <= 0) return false;
if(CopyBuffer(handle, SIGNAL_LINE, 0, 3, signal_line) <= 0) return false;

bool bullish_cross = (main_line[2] <= signal_line[2] && main_line[1] > signal_line[1]);
```

## Terminal-Help Interpretation Notes

- Oscillator-family terminal-help pages are about chart reading: divergences,
  overbought/oversold zones, failure swings, and pattern visibility
- `RSI`, `WPR`, `CCI`, `DeMarker`, `MFI`: treat threshold bands as context,
  not unconditional triggers. Pair with regime, structure, or divergence
  confirmation
- `MACD`, `OsMA`, `RVI`, `Stochastic`: use the second line for crossovers but
  pay attention to slope and location, not just the raw cross
- `Bulls Power`, `Bears Power`, `Force Index`, `Chaikin`, `Momentum`, `TriX`:
  best as confirmation layers added on top of price-structure entries

## Family Gotchas

- Copy at least 3 elements if you want to detect a fresh crossover without
  confusing the current bar and last closed bar
- `start_pos=0` is still the current bar even for oscillators in a separate
  window; use `[1]` for stable closed-bar signals
- If `CopyBuffer()` fails on one line of a multi-buffer indicator, treat the
  whole indicator read as invalid for that pass
