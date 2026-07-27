# Volume and Money-Flow Indicator Handles

| Indicator | Signature skeleton | Buffers | Implementation note |
|-----------|-------------------|---------|---------------------|
| `iAD` | `iAD(symbol, period, applied_volume)` | `0` | Accumulation/Distribution line |
| `iMFI` | `iMFI(symbol, period, ma_period, applied_volume)` | `0` | Money Flow Index with explicit volume type |
| `iOBV` | `iOBV(symbol, period, applied_volume)` | `0` | On Balance Volume |
| `iChaikin` | `iChaikin(symbol, period, fast_ma_period, slow_ma_period, ma_method, applied_volume)` | `0` | One-buffer volume-flow oscillator |
| `iForce` | `iForce(symbol, period, ma_period, ma_method, applied_volume)` | `0` | One-buffer force index |
| `iVolumes` | `iVolumes(symbol, period, applied_volume)` | `0=data`, `1=color index` | For signal logic you usually only need buffer `0`; buffer `1` mirrors histogram colour state |

## Terminal-Help Interpretation Notes

- Volume-family terminal-help pages explain the market-reading intent:
  accumulation vs distribution, confirmation of price expansion, and divergence
  between volume flow and price
- `MFI` is explicitly described as RSI plus volume. In practice, treat its
  `80/20` zones and divergence patterns as confirmation inputs rather than
  standalone reversal orders
- `AD` and `OBV` are accumulation-flow tools. They are most useful when they
  confirm or reject a breakout already seen in price structure
- `Volumes` is more about participation and session quality than directional
  alpha. For EAs, it usually becomes a liquidity filter for breakout or
  momentum setups

## Volume-Family Notes

- Volume-based indicators depend on `ENUM_APPLIED_VOLUME`, so choose tick
  volume vs real volume deliberately
- `iVolumes` exposes a colour-index buffer because the built-in plot is a
  colour histogram; EAs usually ignore that buffer unless they want
  display-state parity
- The handle / `CopyBuffer()` / `IndicatorRelease()` workflow is identical to
  price-based indicators
