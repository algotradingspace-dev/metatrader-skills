# Chart Operations API — MQL5 Programmatic Chart Control

MQL5 functions for opening, configuring, and reading chart data. Distinct
from chart constants (see the `constants` skill).

---

## Chart Lifecycle and Navigation

| Function | Signature | Returns | Purpose |
|----------|-----------|---------|---------|
| `ChartOpen` | `ChartOpen(string symbol, ENUM_TIMEFRAMES period)` | `long` | Opens a new chart; returns chart ID or 0 on failure. Max open charts = `CHARTS_MAX` (100). |
| `ChartClose` | `ChartClose(long chart_id)` | `bool` | Closes the chart by ID. |
| `ChartFirst` | `ChartFirst()` | `long` | Returns the ID of the first chart in the terminal. |
| `ChartNext` | `ChartNext(long chart_id)` | `long` | Returns the ID of the next chart after `chart_id`; 0 if none. |
| `ChartID` | `ChartID()` | `long` | Returns the ID of the chart the program is attached to. |
| `ChartSymbol` | `ChartSymbol(long chart_id)` | `string` | Returns the symbol of the given chart. |
| `ChartPeriod` | `ChartPeriod(long chart_id)` | `ENUM_TIMEFRAMES` | Returns the timeframe of the given chart. |
| `ChartSetSymbolPeriod` | `ChartSetSymbolPeriod(long chart_id, string symbol, ENUM_TIMEFRAMES period)` | `bool` | Changes symbol and/or timeframe of an open chart. |
| `ChartNavigate` | `ChartNavigate(long chart_id, ENUM_CHART_POSITION position, int shift)` | `bool` | Scrolls the chart; `CHART_BEGIN`, `CHART_END`, `CHART_CURRENT_POS`. |
| `ChartRedraw` | `ChartRedraw(long chart_id)` | `void` | Forces immediate chart redraw. |

---

## Property Getters and Setters

| Function | Purpose |
|----------|---------|
| `ChartGetInteger(chart_id, ENUM_CHART_PROPERTY_INTEGER, sub_window)` | Read integer/bool/datetime property |
| `ChartGetDouble(chart_id, ENUM_CHART_PROPERTY_DOUBLE, sub_window)` | Read double property |
| `ChartGetString(chart_id, ENUM_CHART_PROPERTY_STRING)` | Read string property (e.g. comment, symbol) |
| `ChartSetInteger(chart_id, ENUM_CHART_PROPERTY_INTEGER, value)` | Write integer property |
| `ChartSetDouble(chart_id, ENUM_CHART_PROPERTY_DOUBLE, value)` | Write double property |
| `ChartSetString(chart_id, ENUM_CHART_PROPERTY_STRING, value)` | Write string property |

All getters are synchronous — they wait for any pending chart-queue commands
before reading.

---

## Template and Screenshot

| Function | Signature | Purpose |
|----------|-----------|---------|
| `ChartApplyTemplate` | `ChartApplyTemplate(long chart_id, string filename)` | Apply a `.tpl` template file to chart |
| `ChartSaveTemplate` | `ChartSaveTemplate(long chart_id, string filename)` | Save current chart state as `.tpl` |
| `ChartScreenShot` | `ChartScreenShot(long chart_id, string filename, int width, int height, ENUM_ALIGN_MODE align)` | Saves a PNG screenshot to the terminal Files folder |

---

## Indicator Attachment

| Function | Signature | Purpose |
|----------|-----------|---------|
| `ChartIndicatorAdd` | `ChartIndicatorAdd(long chart_id, int sub_window, int indicator_handle)` | Attaches an indicator handle to a chart subwindow |
| `ChartIndicatorDelete` | `ChartIndicatorDelete(long chart_id, int sub_window, string indicator_shortname)` | Removes indicator by short name from subwindow |
| `ChartIndicatorGet` | `ChartIndicatorGet(long chart_id, int sub_window, string indicator_shortname)` | Returns handle of attached indicator |
| `ChartIndicatorName` | `ChartIndicatorName(long chart_id, int sub_window, int index)` | Returns short name of the indicator at index in subwindow |
| `ChartIndicatorsTotal` | `ChartIndicatorsTotal(long chart_id, int sub_window)` | Returns count of indicators in subwindow |

---

## Coordinate Conversion and Drop Positions

| Function | Purpose |
|----------|---------|
| `ChartTimePriceToXY` | Convert chart time+price to pixel x/y |
| `ChartXYToTimePrice` | Convert pixel x/y to chart time+price |
| `ChartXOnDropped` / `ChartYOnDropped` | Pixel coordinates where an object was dropped |
| `ChartTimeOnDropped` / `ChartPriceOnDropped` | Time/price where an object was dropped |
| `ChartWindowOnDropped` | Subwindow index where an object was dropped |
| `ChartWindowFind` | Returns subwindow index that displays a given indicator |

---

## References

- `docs/mql5_com_-_docs/chart_operations.md`
- `docs/mql5_com_-_docs/chart_operations-chartopen.md`
- `docs/mql5_com_-_docs/chart_operations-chartclose.md`
- `docs/mql5_com_-_docs/chart_operations-chartfirst.md`
- `docs/mql5_com_-_docs/chart_operations-chartnext.md`
- `docs/mql5_com_-_docs/chart_operations-chartid.md`
- `docs/mql5_com_-_docs/chart_operations-chartsymbol.md`
- `docs/mql5_com_-_docs/chart_operations-chartperiod.md`
- `docs/mql5_com_-_docs/chart_operations-chartsetsymbolperiod.md`
- `docs/mql5_com_-_docs/chart_operations-chartnavigate.md`
- `docs/mql5_com_-_docs/chart_operations-chartredraw.md`
- `docs/mql5_com_-_docs/chart_operations-chartgetinteger.md`
- `docs/mql5_com_-_docs/chart_operations-chartgetdouble.md`
- `docs/mql5_com_-_docs/chart_operations-chartgetstring.md`
- `docs/mql5_com_-_docs/chart_operations-chartsetinteger.md`
- `docs/mql5_com_-_docs/chart_operations-chartsetdouble.md`
- `docs/mql5_com_-_docs/chart_operations-chartsetstring.md`
- `docs/mql5_com_-_docs/chart_operations-chartapplytemplate.md`
- `docs/mql5_com_-_docs/chart_operations-chartsavetemplate.md`
- `docs/mql5_com_-_docs/chart_operations-chartscreenshot.md`
- `docs/mql5_com_-_docs/chart_operations-chartindicatoradd.md`
- `docs/mql5_com_-_docs/chart_operations-chartindicatordelete.md`
- `docs/mql5_com_-_docs/chart_operations-chartindicatorget.md`
- `docs/mql5_com_-_docs/chart_operations-chartindicatorname.md`
- `docs/mql5_com_-_docs/chart_operations-chartindicatorstotal.md`
- `docs/mql5_com_-_docs/chart_operations-charttimepricetoxy.md`
- `docs/mql5_com_-_docs/chart_operations-chartxytotimeprice.md`
- `docs/mql5_com_-_docs/chart_operations-chartxondropped.md`
- `docs/mql5_com_-_docs/chart_operations-chartyondropped.md`
- `docs/mql5_com_-_docs/chart_operations-charttimeondropped.md`
- `docs/mql5_com_-_docs/chart_operations-chartpriceondropped.md`
- `docs/mql5_com_-_docs/chart_operations-chartwindowondropped.md`
- `docs/mql5_com_-_docs/chart_operations-chartwindowfind.md`
