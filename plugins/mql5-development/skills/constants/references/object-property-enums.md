# Object Properties (OBJPROP_*)

## ENUM_OBJECT_PROPERTY_INTEGER — `ObjectSetInteger()` / `ObjectGetInteger()`

> Canonical MQL5 reference: [OBJPROP_COLOR](https://www.mql5.com/en/docs/constants/objectconstants/enum_object_property#enum_object_property_integer) · [CHARTEVENT_CLICK](https://www.mql5.com/en/docs/constants/chartconstants/enum_chartevents) · [OBJPROP_CORNER](https://www.mql5.com/en/docs/constants/objectconstants/enum_object_property)

| Identifier | Type | Description |
|------------|------|-------------|
| `OBJPROP_COLOR` | color | Object color |
| `OBJPROP_STYLE` | ENUM_LINE_STYLE | Line style |
| `OBJPROP_WIDTH` | int | Line thickness |
| `OBJPROP_BACK` | bool | Draw in background |
| `OBJPROP_ZORDER` | long | Click event priority (`CHARTEVENT_CLICK`) |
| `OBJPROP_FILL` | bool | Fill with color (Rectangle/Triangle/Ellipse/Channels) |
| `OBJPROP_HIDDEN` | bool | Hide from Objects List (prevents accidental deletion) |
| `OBJPROP_SELECTED` | bool | Object selected state |
| `OBJPROP_READONLY` | bool | Editable text (OBJ_EDIT) |
| `OBJPROP_TYPE` | ENUM_OBJECT | Object type (r/o) |
| `OBJPROP_TIME` | datetime | Time coordinate (modifier = anchor index) |
| `OBJPROP_SELECTABLE` | bool | Selectable by mouse |
| `OBJPROP_CREATETIME` | datetime | Creation time (r/o) |
| `OBJPROP_LEVELS` | int | Number of Fibonacci/channel levels |
| `OBJPROP_LEVELCOLOR` | color | Level line color (modifier = level number) |
| `OBJPROP_LEVELSTYLE` | ENUM_LINE_STYLE | Level line style (modifier = level number) |
| `OBJPROP_LEVELWIDTH` | int | Level line thickness (modifier = level number) |
| `OBJPROP_ALIGN` | ENUM_ALIGN_MODE | Horizontal text alignment (OBJ_EDIT) |
| `OBJPROP_FONTSIZE` | int | Font size |
| `OBJPROP_RAY_LEFT` | bool | Ray extends left |
| `OBJPROP_RAY_RIGHT` | bool | Ray extends right |
| `OBJPROP_RAY` | bool | Vertical line through all subwindows |
| `OBJPROP_ELLIPSE` | bool | Show full ellipse for OBJ_FIBOARC |
| `OBJPROP_ARROWCODE` | uchar | Wingdings code for OBJ_ARROW |
| `OBJPROP_TIMEFRAMES` | flags | Visibility bitmask (OBJ_PERIOD_* flags) |
| `OBJPROP_ANCHOR` | enum | Anchor: ENUM_ARROW_ANCHOR (OBJ_ARROW) or ENUM_ANCHOR_POINT (others) |
| `OBJPROP_XDISTANCE` | int | X pixels from binding corner |
| `OBJPROP_YDISTANCE` | int | Y pixels from binding corner |
| `OBJPROP_DIRECTION` | ENUM_GANN_DIRECTION | Gann trend direction |
| `OBJPROP_DEGREE` | ENUM_ELLIOT_WAVE_DEGREE | Elliott wave labeling level |
| `OBJPROP_DRAWLINES` | bool | Show lines between Elliott wave tops |
| `OBJPROP_STATE` | bool | Button pressed/depressed |
| `OBJPROP_CHART_ID` | long | Embedded chart ID for OBJ_CHART (r/o) |
| `OBJPROP_XSIZE` | int | Width in pixels (OBJ_LABEL r/o, others r/w) |
| `OBJPROP_YSIZE` | int | Height in pixels |
| `OBJPROP_XOFFSET` | int | Bitmap visible area X offset |
| `OBJPROP_YOFFSET` | int | Bitmap visible area Y offset |
| `OBJPROP_PERIOD` | ENUM_TIMEFRAMES | Timeframe for OBJ_CHART |
| `OBJPROP_DATE_SCALE` | bool | Show date scale for OBJ_CHART |
| `OBJPROP_PRICE_SCALE` | bool | Show price scale for OBJ_CHART |
| `OBJPROP_CHART_SCALE` | int | Chart zoom 0-5 for OBJ_CHART |
| `OBJPROP_BGCOLOR` | color | Background color (OBJ_EDIT/OBJ_BUTTON/OBJ_RECTANGLE_LABEL) |
| `OBJPROP_CORNER` | ENUM_BASE_CORNER | Chart corner for pixel-anchored objects |
| `OBJPROP_BORDER_TYPE` | ENUM_BORDER_TYPE | Border type for OBJ_RECTANGLE_LABEL |
| `OBJPROP_BORDER_COLOR` | color | Border color for OBJ_EDIT/OBJ_BUTTON |

## ENUM_OBJECT_PROPERTY_DOUBLE — `ObjectSetDouble()` / `ObjectGetDouble()`

> Canonical MQL5 reference: [OBJPROP_SCALE](https://www.mql5.com/en/docs/constants/objectconstants/enum_object_property#enum_object_property_double) · [EMPTY_VALUE](https://www.mql5.com/en/docs/constants/namedconstants/otherconstants)

| Identifier | Description |
|------------|-------------|
| `OBJPROP_PRICE` | Price coordinate (modifier = anchor index) |
| `OBJPROP_LEVELVALUE` | Fibonacci/channel level value (modifier = level number) |
| `OBJPROP_SCALE` | Gann scale (Pips/Bar) or Fibonacci Arc scale |
| `OBJPROP_ANGLE` | Rotation angle counter-clockwise; `EMPTY_VALUE` if not set |
| `OBJPROP_DEVIATION` | Deviation for Standard Deviation Channel |

## ENUM_OBJECT_PROPERTY_STRING — `ObjectSetString()` / `ObjectGetString()`

> Canonical MQL5 reference: [OBJPROP_TEXT](https://www.mql5.com/en/docs/constants/objectconstants/enum_object_property#enum_object_property_double) · [OBJPROP_FONT](https://www.mql5.com/en/docs/constants/objectconstants/enum_object_property#enum_object_property_string) · [OBJPROP_BMPFILE](https://www.mql5.com/en/docs/constants/objectconstants/enum_object_property#enum_object_property_integer)

| Identifier | Description |
|------------|-------------|
| `OBJPROP_NAME` | Object name |
| `OBJPROP_TEXT` | Object description / displayed text |
| `OBJPROP_TOOLTIP` | Tooltip text (`"\n"` disables auto-tooltip) |
| `OBJPROP_LEVELTEXT` | Level description (modifier = level number) |
| `OBJPROP_FONT` | Font name |
| `OBJPROP_BMPFILE` | BMP filename for OBJ_BITMAP_LABEL (modifier: 0=ON, 1=OFF) |
| `OBJPROP_SYMBOL` | Symbol name for OBJ_CHART |
