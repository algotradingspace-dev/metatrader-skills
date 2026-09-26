# CExpertBase — Shared Context, Series Wiring, and Initialisation Phases

**Source family:** `standardlibrary-expertclasses-expertbaseclasses-cexpertbase*.md`

`CExpertBase` is the common substrate under `CExpert`, `CExpertSignal`,
`CExpertTrailing`, and `CExpertMoney`. It owns symbol/timeframe identity,
magic routing, series pointers, and the staged initialisation contract
that derived expert modules inherit.

> Canonical MQL5 reference: [ValidationSettings](https://www.mql5.com/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpert/cexpertvalidationsettings) · [OnInit](https://www.mql5.com/en/docs/event_handlers/oninit) · [SetPriceSeries](https://www.mql5.com/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpertbase/cexpertbasesetpriceseries) · [SetOtherSeries](https://www.mql5.com/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpertbase/cexpertbasesetotherseries)

| Method | Return type | Purpose | Usage note |
|--------|------------|---------|------------|
| `Init` | `bool` | Initialises the object | Call once from the owning expert before any derived module reads series data |
| `ValidationSettings` | `bool` | Checks the settings | Fail `OnInit()` early if shared symbol/period parameters are invalid |
| `Symbol` | `bool` | Sets the object symbol | Set before indicators or signals so every child module uses one instrument context |
| `Period` | `bool` | Sets the object timeframe | Set the working timeframe before any bar-indexed logic runs |
| `Magic` | `void` | Sets the Expert Advisor ID | Propagate ownership before managing positions or pending orders |
| `SetPriceSeries` | `bool` | Sets pointers to external price series | Use when a parent expert injects shared OHLC arrays instead of owning them here |
| `SetOtherSeries` | `bool` | Sets pointers to external non-price series | Use when time, spread, or volume arrays are shared from outside |
| `InitIndicators` | `bool` | Initialises all indicators and time series | Call after all required series pointers are known and stable |
| `InitPhase` | `ENUM_INIT_PHASE` | Gets the current phase of the object initialisation | Inspect during staged setup or when debugging partial initialisation failures |
| `TrendType` | `void` | Sets trend type | Set in derived classes when signal logic depends on trend-vs-oscillator semantics |
| `UsedSeries` | `int` | Gets the bitmask of timeseries used | Read this to preload only the history series a derived module actually needs |
| `EveryTick` | `void` | Sets the "Every tick" flag | Enable only when the derived strategy must run on every tick rather than on new bars |
| `Open` | `double` | Gets the element of the Open timeseries by index | Read cached series values by bar shift inside signal or trailing code |
| `High` | `double` | Gets the element of the High timeseries by index | Use for bar-range logic without re-copying history on each call |
| `Low` | `double` | Gets the element of the Low timeseries by index | Use for stop, pattern, and range calculations by shift index |
| `Close` | `double` | Gets the element of the Close timeseries by index | Use as the default bar-price accessor in derived expert modules |
| `Spread` | `double` | Gets the element of the Spread timeseries by index | Read cached spread values when filtering entries or adjusting stops |
| `Time` | `datetime` | Gets the element of the Time timeseries by index | Use for bar timestamps when aligning signals and history checkpoints |
| `TickVolume` | `long` | Gets the element of the TickVolume timeseries by index | Use when the module depends on activity-based filters from tick volume |
| `RealVolume` | `long` | Gets the element of the RealVolume timeseries by index | Use only on symbols/brokers that provide real volume |
| `InitOpen` | `bool` | Initialises the Open timeseries | Call from custom setup only if open-price history is required |
| `InitHigh` | `bool` | Initialises the High timeseries | Initialise explicitly when derived logic depends on highs |
| `InitLow` | `bool` | Initialises the Low timeseries | Initialise explicitly when derived logic depends on lows |
| `InitClose` | `bool` | Initialises the Close timeseries | Initialise explicitly when close-price history is required |
| `InitSpread` | `bool` | Initialises the Spread timeseries | Initialise only if spread-aware entry or execution logic is enabled |
| `InitTime` | `bool` | Initialises the Time timeseries | Initialise when time alignment or session gating needs cached bar times |
| `InitTickVolume` | `bool` | Initialises the TickVolume timeseries | Initialise only for volume-aware models to avoid unnecessary work |
| `InitRealVolume` | `bool` | Initialises the RealVolume timeseries | Guard with symbol capability checks before relying on it |
| `PriceLevelUnit` | `double` | Gets the price level unit | Use to convert abstract levels into symbol-scaled price offsets |
| `StartIndex` | `int` | Gets the index of starting bar to analyse | Respect this when scanning history so setup bars are skipped consistently |
| `CompareMagic` | `bool` | Compares the Expert Advisor ID (magic) with the specified value | Use in ownership checks before acting on positions or orders |

---

## References

- `docs/mql5_com_-_docs/standardlibrary-expertclasses-expertbaseclasses-cexpertbase*.md`
