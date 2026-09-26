# Custom Indicator Architecture — Buffers, Plot Properties, and Draw Types

**Source family:** `customind*.md`

Custom indicators have a strict initialisation contract: declare chart/window
mode, buffer count, and plot count up front; bind buffers with
`SetIndexBuffer()`; then configure indicator-level and plot-level properties
through `IndicatorSet*()` and `PlotIndexSet*()`.

---

## Core Property and Binding Functions

> Canonical MQL5 reference: [SetIndexBuffer](https://www.mql5.com/en/docs/customind/setindexbuffer) · [ArraySetAsSeries](https://www.mql5.com/en/docs/array/arraysetasseries) · [IndicatorSetDouble](https://www.mql5.com/en/docs/customind/indicatorsetdouble) · [IndicatorSetInteger](https://www.mql5.com/en/docs/customind/indicatorsetinteger)

| Function | Purpose | Usage note |
|----------|---------|------------|
| `SetIndexBuffer(index, buffer, data_type)` | Binds a dynamic `double` array to an indicator buffer slot | Binding resets array indexing to common-array mode, so call `ArraySetAsSeries()` again afterward if you need timeseries access |
| `IndicatorSetDouble()` | Sets indicator-window doubles such as min/max and level values | Level modifiers are zero-based in code even though `#property indicator_levelN` is one-based |
| `IndicatorSetInteger()` | Sets integer-valued indicator properties such as level count, digits, or level styling | Use for subwindow height, level count, level colour/style/width, and display precision |
| `IndicatorSetString()` | Sets indicator text properties such as short name and level labels | `INDICATOR_SHORTNAME` controls the name shown in `Ctrl+I` and the Data Window |
| `PlotIndexSetDouble()` | Sets plot-level double properties where needed | Use when the plot itself, not the whole indicator window, owns the property |
| `PlotIndexSetInteger()` | Sets plot draw type, line colour, style, width, and related integer properties | Plot numbering is zero-based even when `#property indicator_typeN` syntax is one-based |
| `PlotIndexSetString()` | Sets plot label strings | Labels feed the Data Window and tooltip text for each plot |
| `PlotIndexGetInteger()` | Reads current plot property values | Useful when a derived indicator must inspect an already configured plot |

---

## Non-Negotiable Setup Rules

- `#property indicator_chart_window` or `#property indicator_separate_window`
  decides where the indicator is drawn; there is no runtime function to
  switch that layout mode later
- `#property indicator_buffers` and `#property indicator_plots` must be
  declared before runtime property setters can work correctly
- `SetIndexBuffer()` accepts `INDICATOR_DATA`, `INDICATOR_COLOR_INDEX`, and
  `INDICATOR_CALCULATIONS`; use colour-index buffers for coloured draw styles
  and calculations buffers for internal working arrays
- Once a dynamic array is bound as an indicator buffer, terminal code owns
  its size management; do not try to `ArrayResize()` it manually

---

## Draw-Type Families

> Canonical MQL5 reference: [DRAW_NONE](https://www.mql5.com/en/docs/customind/indicators_examples/draw_none) · [DRAW_LINE](https://www.mql5.com/en/docs/customind/indicators_examples/draw_line) · [DRAW_SECTION](https://www.mql5.com/en/docs/customind/indicators_examples/draw_section) · [DRAW_ARROW](https://www.mql5.com/en/docs/customind/indicators_examples/draw_arrow)

| Family | Draw types | Architectural meaning |
|--------|-----------|----------------------|
| Hidden / single-line | `DRAW_NONE`, `DRAW_LINE`, `DRAW_SECTION`, `DRAW_ARROW` | Best for simple overlays, signal markers, or hidden calculation outputs |
| Histogram / range | `DRAW_HISTOGRAM`, `DRAW_HISTOGRAM2`, `DRAW_ZIGZAG`, `DRAW_FILLING` | Use when the indicator expresses spread, channel width, or paired boundaries |
| Bar / candle | `DRAW_BARS`, `DRAW_CANDLES` | Use only when the indicator must render OHLC-style structures |
| Coloured variants | `DRAW_COLOR_LINE`, `DRAW_COLOR_SECTION`, `DRAW_COLOR_HISTOGRAM`, `DRAW_COLOR_HISTOGRAM2`, `DRAW_COLOR_ARROW`, `DRAW_COLOR_ZIGZAG`, `DRAW_COLOR_BARS`, `DRAW_COLOR_CANDLES` | These require an extra colour-index buffer and are the main reason buffer/plot planning must happen before `OnCalculate()` logic |

---

## High-Value Gotchas

- Preprocessor numbering is one-based, runtime modifiers are zero-based.
  This mismatch is the easiest way to mislabel a level or configure the wrong plot
- The `indicator_applied_price` property has no runtime setter; it must be
  declared in preprocessor directives or supplied through the indicator UI
  when supported
- If a buffer should behave like a series after binding, reapply
  `ArraySetAsSeries()` after `SetIndexBuffer()` because binding normalises
  it to standard indexing
- Coloured draw types are never single-buffer indicators in practice; plan
  value and colour buffers together before you finalise `indicator_buffers`

---

## References

- `docs/mql5_com_-_docs/customind.md`
- `docs/mql5_com_-_docs/customind-indicators_examples.md`
- `docs/mql5_com_-_docs/customind-indicators_examples-draw_arrow.md`
- `docs/mql5_com_-_docs/customind-indicators_examples-draw_bars.md`
- `docs/mql5_com_-_docs/customind-indicators_examples-draw_candles.md`
- `docs/mql5_com_-_docs/customind-indicators_examples-draw_color_arrow.md`
- `docs/mql5_com_-_docs/customind-indicators_examples-draw_color_bars.md`
- `docs/mql5_com_-_docs/customind-indicators_examples-draw_color_candles.md`
- `docs/mql5_com_-_docs/customind-indicators_examples-draw_color_histogram.md`
- `docs/mql5_com_-_docs/customind-indicators_examples-draw_color_histogram2.md`
- `docs/mql5_com_-_docs/customind-indicators_examples-draw_color_line.md`
- `docs/mql5_com_-_docs/customind-indicators_examples-draw_color_section.md`
- `docs/mql5_com_-_docs/customind-indicators_examples-draw_color_zigzag.md`
- `docs/mql5_com_-_docs/customind-indicators_examples-draw_filling.md`
- `docs/mql5_com_-_docs/customind-indicators_examples-draw_histogram.md`
- `docs/mql5_com_-_docs/customind-indicators_examples-draw_histogram2.md`
- `docs/mql5_com_-_docs/customind-indicators_examples-draw_line.md`
- `docs/mql5_com_-_docs/customind-indicators_examples-draw_none.md`
- `docs/mql5_com_-_docs/customind-indicators_examples-draw_section.md`
- `docs/mql5_com_-_docs/customind-indicators_examples-draw_zigzag.md`
- `docs/mql5_com_-_docs/customind-indicatorsetdouble.md`
- `docs/mql5_com_-_docs/customind-indicatorsetinteger.md`
- `docs/mql5_com_-_docs/customind-indicatorsetstring.md`
- `docs/mql5_com_-_docs/customind-plotindexgetinteger.md`
- `docs/mql5_com_-_docs/customind-plotindexsetdouble.md`
- `docs/mql5_com_-_docs/customind-plotindexsetinteger.md`
- `docs/mql5_com_-_docs/customind-plotindexsetstring.md`
- `docs/mql5_com_-_docs/customind-propertiesandfunctions.md`
- `docs/mql5_com_-_docs/customind-setindexbuffer.md`
