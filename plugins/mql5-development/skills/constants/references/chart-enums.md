# Chart API Enums

## ENUM_CHART_EVENT — `OnChartEvent(id, lparam, dparam, sparam)`

| Value | Description |
|-------|-------------|
| `CHARTEVENT_KEYDOWN` | Key pressed |
| `CHARTEVENT_KEYUP` | Key released |
| `CHARTEVENT_MOUSE_MOVE` | Mouse move / click (requires `CHART_EVENT_MOUSE_MOVE=true`) |
| `CHARTEVENT_MOUSE_WHEEL` | Mouse wheel (requires `CHART_EVENT_MOUSE_WHEEL=true`) |
| `CHARTEVENT_OBJECT_CREATE` | Object created (requires `CHART_EVENT_OBJECT_CREATE=true`) |
| `CHARTEVENT_OBJECT_CHANGE` | Object properties changed via dialog |
| `CHARTEVENT_OBJECT_DELETE` | Object deleted (requires `CHART_EVENT_OBJECT_DELETE=true`) |
| `CHARTEVENT_CLICK` | Chart clicked |
| `CHARTEVENT_OBJECT_CLICK` | Graphical object clicked |
| `CHARTEVENT_OBJECT_DRAG` | Object drag-and-drop |
| `CHARTEVENT_OBJECT_ENDEDIT` | Edit object text editing ended |
| `CHARTEVENT_CHART_CHANGE` | Chart resized or properties changed via dialog |
| `CHARTEVENT_CUSTOM` | First custom event ID (65536) |
| `CHARTEVENT_CUSTOM_LAST` | Last custom event ID (66535) |

> Custom events: use `EventChartCustom(chartId, CHARTEVENT_CUSTOM + N, l, d, s)`.
> `lparam`/`dparam`/`sparam` semantics differ per event type.

## ENUM_CHART_MODE — `ChartSetInteger(chart, CHART_MODE, mode)`

| Value | Description |
|-------|-------------|
| `CHART_BARS` | Bar chart |
| `CHART_CANDLES` | Japanese candlesticks |
| `CHART_LINE` | Line chart (Close prices) |

## ENUM_CHART_POSITION — `ChartNavigate(chart, pos, shift)`

| Value | Description |
|-------|-------------|
| `CHART_BEGIN` | Oldest prices (chart start) |
| `CHART_CURRENT_POS` | Current view position |
| `CHART_END` | Newest prices (chart end) |

## Key ENUM_CHART_PROPERTY_INTEGER Identifiers

| Identifier | Description |
|------------|-------------|
| `CHART_SHOW` | Enable/disable full chart rendering |
| `CHART_MODE` | Bar/candle/line (`ENUM_CHART_MODE`) |
| `CHART_SCALE` | Zoom level (0-5) |
| `CHART_AUTOSCROLL` | Auto-scroll to latest bar |
| `CHART_SHIFT` | Chart indent from right border |
| `CHART_VISIBLE_BARS` | Visible bar count (r/o) |
| `CHART_FIRST_VISIBLE_BAR` | Oldest visible bar index (r/o) |
| `CHART_WIDTH_IN_BARS` | Chart width in bars (r/o) |
| `CHART_WIDTH_IN_PIXELS` | Chart width in pixels (r/o) |
| `CHART_HEIGHT_IN_PIXELS` | Chart height in pixels |
| `CHART_WINDOWS_TOTAL` | Total windows incl. subwindows (r/o) |
| `CHART_EVENT_MOUSE_MOVE` | Fire `CHARTEVENT_MOUSE_MOVE` |
| `CHART_EVENT_MOUSE_WHEEL` | Fire `CHARTEVENT_MOUSE_WHEEL` |
| `CHART_EVENT_OBJECT_CREATE` | Fire `CHARTEVENT_OBJECT_CREATE` |
| `CHART_EVENT_OBJECT_DELETE` | Fire `CHARTEVENT_OBJECT_DELETE` |
| `CHART_SHOW_GRID` | Show price grid |
| `CHART_SHOW_VOLUMES` | Volume display mode (`ENUM_CHART_VOLUME_MODE`) |
| `CHART_SHOW_TRADE_LEVELS` | Show SL/TP/pending order levels |
| `CHART_IS_MAXIMIZED` | Maximized flag (r/o) |
| `CHART_IS_DOCKED` | Docked flag |
