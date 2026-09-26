# CExpertSignal — Voting, Filters, Thresholds, and Order Parameters

**Source family:** `standardlibrary-expertclasses-expertbaseclasses-cexpertsignal*.md`

`CExpertSignal` is the standard-library voting and parameterisation surface
for entry, exit, reverse, and pending-order logic. Derived signal classes
override its checks, vote-strength methods, and order-parameter hooks while
the owning `CExpert` handles execution.

> Canonical MQL5 reference: [InitIndicators](https://www.mql5.com/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpert/cexpertinitindicators) · [ValidationSettings](https://www.mql5.com/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpert/cexpertvalidationsettings) · [AddFilter](https://www.mql5.com/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpertsignal/cexpertsignaladdfilter) · [BasePrice](https://www.mql5.com/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpertsignal/cexpertsignalbaseprice)

| Method | Return type | Purpose | Usage note |
|--------|------------|---------|------------|
| `InitIndicators` | `bool` | Initialises all necessary indicators and timeseries | Create signal handles here after the base series contract is ready |
| `ValidationSettings` | `bool` | Checks the object settings | Reject inconsistent thresholds, filters, or pattern masks before live use |
| `AddFilter` | `bool` | Adds a filter to the composite signal | Use to build multi-filter voting trees under one signal object |
| `BasePrice` | `void` | Sets base price level | Set this before price-level, stop, or take calculations depend on it |
| `UsedSeries` | `int` | Gets the flags of the timeseries used | Expose required history so the owning expert preloads only necessary series |
| `Weight` | `void` | Sets new value of "Weight" parameter | Tune how strongly this signal contributes inside a composite model |
| `PatternsUsage` | `void` | Sets new value of "PatternsUsage" parameter | Configure which pattern groups are active before evaluation starts |
| `General` | `void` | Sets new value of "General" parameter | Use as a broad signal-tuning knob before testing or live runs |
| `Ignore` | `void` | Sets new value of "Ignore" parameter | Silence this signal when the parent composite should bypass it |
| `Invert` | `void` | Sets new value of "Invert" parameter | Flip directionality when the same logic is used contrarian-style |
| `ThresholdOpen` | `void` | Sets new value of "ThresholdOpen" parameter | Set the vote strength required to open a trade |
| `ThresholdClose` | `void` | Sets new value of "ThresholdClose" parameter | Set the vote strength required to close a trade |
| `PriceLevel` | `void` | Sets new value of "PriceLevel" parameter | Configure price offsets used in entry parameter calculation |
| `StopLevel` | `void` | Sets new value of "StopLevel" parameter | Set stop-distance policy before signal-generated orders are built |
| `TakeLevel` | `void` | Sets new value of "TakeLevel" parameter | Set take-profit policy before signal-generated orders are built |
| `Expiration` | `void` | Sets the value of "Expiration" parameter | Configure pending-order lifetime before returning order params |
| `Magic` | `void` | Sets the value of "Magic" parameter | Keep the signal aligned with the owning expert's trade ownership id |
| `CheckOpenLong` | `bool` | Checks conditions to open a long position | Override with the long-entry gate for the derived signal |
| `CheckCloseLong` | `bool` | Checks conditions to close a long position | Override with long-exit logic tied to this signal |
| `CheckOpenShort` | `bool` | Checks conditions to open a short position | Override with the short-entry gate for the derived signal |
| `CheckCloseShort` | `bool` | Checks conditions to close a short position | Override with short-exit logic tied to this signal |
| `CheckReverseLong` | `bool` | Checks conditions of a long position reversal | Override when a long should flip directly into a short |
| `CheckReverseShort` | `bool` | Checks conditions of a short position reversal | Override when a short should flip directly into a long |
| `OpenLongParams` | `bool` | Sets parameters to open a long position | Fill price, SL, TP, and expiration outputs before order submission |
| `OpenShortParams` | `bool` | Sets parameters to open a short position | Fill price, SL, TP, and expiration outputs for short entries |
| `CloseLongParams` | `bool` | Sets parameters to close a long position | Customise close-side parameters before the expert sends the request |
| `CloseShortParams` | `bool` | Sets parameters to close a short position | Customise close-side parameters for short exits |
| `CheckTrailingOrderLong` | `bool` | Checks conditions to modify parameters of Buy Pending order | Use when the signal also owns pending-order repricing rules |
| `CheckTrailingOrderShort` | `bool` | Checks conditions to modify parameters of Sell Pending order | Use when the signal also owns short pending-order repricing rules |
| `LongCondition` | `int` | Checks conditions to open a long position | Return vote strength rather than a final trade decision |
| `ShortCondition` | `int` | Checks conditions to open a short position | Return vote strength rather than a final trade decision |
| `Direction` | `double` | Returns the value of "weighted" price direction | Call after refresh to get the final weighted directional bias |

---

## References

- `docs/mql5_com_-_docs/standardlibrary-expertclasses-expertbaseclasses-cexpertsignal*.md`
