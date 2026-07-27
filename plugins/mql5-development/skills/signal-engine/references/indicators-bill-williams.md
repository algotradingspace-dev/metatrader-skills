# Bill Williams and Custom Indicator Handles

| Indicator | Signature skeleton | Buffers | Implementation note |
|-----------|-------------------|---------|---------------------|
| `iAC` | `iAC(symbol, period)` | `0` | Accelerator Oscillator |
| `iAO` | `iAO(symbol, period)` | `0` | Awesome Oscillator |
| `iBWMFI` | `iBWMFI(symbol, period, applied_volume)` | `0` | Market Facilitation Index |
| `iAlligator` | `iAlligator(symbol, period, jaw_period, jaw_shift, teeth_period, teeth_shift, lips_period, lips_shift, ma_method, applied_price)` | `0=JAW`, `1=TEETH`, `2=LIPS` | Docs copy each line with its own negative shift |
| `iFractals` | `iFractals(symbol, period)` | `0=UPPER_LINE`, `1=LOWER_LINE` | Two sparse arrow buffers; read both for reversal context |
| `iGator` | `iGator(symbol, period, jaw_period, jaw_shift, teeth_period, teeth_shift, lips_period, lips_shift, ma_method, applied_price)` | `0=UPPER_HISTOGRAM`, `1=upper color`, `2=LOWER_HISTOGRAM`, `3=lower color` | Use minimum Alligator shift to align both histograms |
| `iCustom` | `iCustom(symbol, period, name, ...)` | custom | Custom indicator EX5 must exist; parameter order and types must match exactly |

## `iCustom()` Rules That Matter in Production

- If the indicator name starts with `\`, lookup is relative to the MQL5 root
- Otherwise, MetaTrader first searches relative to the caller EX5 folder, then
  under `MQL5\Indicators`
- Missing EX5 files return `INVALID_HANDLE` with error `4802`
  (`ERR_INDICATOR_CANNOT_CREATE`)
- If the indicator name is not a compile-time constant string, or if you use
  `IndicatorCreate()` instead, add `#property tester_indicator "indicator_name.ex5"`
  for tester runs
- When chaining indicators, pass the upstream handle or `Applied_Price` argument
  last, after the custom indicator inputs

## Terminal-Help Interpretation Notes

- Bill Williams terminal-help pages are mostly system-logic explanations:
  sleeping vs hunting Alligator states, fractal breakout context, oscillator
  phase shifts, and the role of market facilitation
- `Alligator` and `Gator` are not just multi-line indicators. Their shifted
  lines describe market state transitions; EA rules should name those states
  explicitly instead of treating the buffers as generic moving averages
- `Fractals` in the UI docs are breakout anchors, not trend filters. In code,
  they pair naturally with pending-entry or stop-placement logic
- `AO`, `AC`, and `BWMFI` are best used as momentum confirmation after a
  structural setup appears, not as isolated triggers

## Shift-Sensitive Bill Williams Note

- `iAlligator` and `iGator` have parameter shifts that affect how the lines
  are copied and displayed; do not assume `CopyBuffer(handle, line, 0, ...)`
  is aligned with the visual plot unless you replicate the docs' shift handling
- `iFractals` returns two separate buffers, so a bullish or bearish fractal
  scan should always inspect the correct line instead of scanning a merged
  series
