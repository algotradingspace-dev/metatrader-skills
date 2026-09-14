# Object Types and Positioning Enums

## ENUM_OBJECT — `ObjectCreate(chart, name, type, ...)`

44 graphical object types:

> Canonical MQL5 reference: [OBJ_VLINE](https://www.mql5.com/en/docs/constants/objectconstants/enum_object/obj_vline) · [OBJ_HLINE](https://www.mql5.com/en/docs/constants/objectconstants/enum_object/obj_hline) · [OBJ_TREND](https://www.mql5.com/en/docs/constants/objectconstants/enum_object/obj_trend) · [OBJ_TRENDBYANGLE](https://www.mql5.com/en/docs/constants/objectconstants/enum_object/obj_trendbyangle)

| ID | Description |
|----|-------------|
| `OBJ_VLINE` | Vertical Line |
| `OBJ_HLINE` | Horizontal Line |
| `OBJ_TREND` | Trend Line |
| `OBJ_TRENDBYANGLE` | Trend Line By Angle |
| `OBJ_CYCLES` | Cycle Lines |
| `OBJ_ARROWED_LINE` | Arrowed Line |
| `OBJ_CHANNEL` | Equidistant Channel |
| `OBJ_STDDEVCHANNEL` | Standard Deviation Channel |
| `OBJ_REGRESSION` | Linear Regression Channel |
| `OBJ_PITCHFORK` | Andrews' Pitchfork |
| `OBJ_GANNLINE` | Gann Line |
| `OBJ_GANNFAN` | Gann Fan |
| `OBJ_GANNGRID` | Gann Grid |
| `OBJ_FIBO` | Fibonacci Retracement |
| `OBJ_FIBOTIMES` | Fibonacci Time Zones |
| `OBJ_FIBOFAN` | Fibonacci Fan |
| `OBJ_FIBOARC` | Fibonacci Arcs |
| `OBJ_FIBOCHANNEL` | Fibonacci Channel |
| `OBJ_EXPANSION` | Fibonacci Expansion |
| `OBJ_ELLIOTWAVE5` | Elliott Motive Wave (5) |
| `OBJ_ELLIOTWAVE3` | Elliott Correction Wave (3) |
| `OBJ_RECTANGLE` | Rectangle |
| `OBJ_TRIANGLE` | Triangle |
| `OBJ_ELLIPSE` | Ellipse |
| `OBJ_ARROW_THUMB_UP` | Thumbs Up |
| `OBJ_ARROW_THUMB_DOWN` | Thumbs Down |
| `OBJ_ARROW_UP` | Arrow Up |
| `OBJ_ARROW_DOWN` | Arrow Down |
| `OBJ_ARROW_STOP` | Stop Sign |
| `OBJ_ARROW_CHECK` | Check Sign |
| `OBJ_ARROW_LEFT_PRICE` | Left Price Label |
| `OBJ_ARROW_RIGHT_PRICE` | Right Price Label |
| `OBJ_ARROW_BUY` | Buy Sign |
| `OBJ_ARROW_SELL` | Sell Sign |
| `OBJ_ARROW` | Arrow (custom Wingdings code) |
| `OBJ_TEXT` | Text (date/price anchor) |
| `OBJ_LABEL` | Label (pixel anchor, CORNER) |
| `OBJ_BUTTON` | Button |
| `OBJ_CHART` | Embedded Chart |
| `OBJ_BITMAP` | Bitmap (date/price anchor) |
| `OBJ_BITMAP_LABEL` | Bitmap Label (pixel anchor) |
| `OBJ_EDIT` | Editable text field |
| `OBJ_EVENT` | Economic calendar event marker |
| `OBJ_RECTANGLE_LABEL` | Rectangle Label (UI container) |

## ENUM_BASE_CORNER — `ObjectSetInteger(chart, name, OBJPROP_CORNER, ...)`

Used by `OBJ_LABEL`, `OBJ_BUTTON`, `OBJ_BITMAP_LABEL`, `OBJ_EDIT`, `OBJ_RECTANGLE_LABEL`:

| ID | Description |
|----|-------------|
| `CORNER_LEFT_UPPER` | Upper-left (default) |
| `CORNER_LEFT_LOWER` | Lower-left |
| `CORNER_RIGHT_LOWER` | Lower-right |
| `CORNER_RIGHT_UPPER` | Upper-right |

## ENUM_ANCHOR_POINT — `ObjectSetInteger(chart, name, OBJPROP_ANCHOR, ...)`

Used by `OBJ_TEXT`, `OBJ_LABEL`, `OBJ_BITMAP`, `OBJ_BITMAP_LABEL` (9 values):

| ID | Description |
|----|-------------|
| `ANCHOR_LEFT_UPPER` | Upper-left corner of object |
| `ANCHOR_LEFT` | Left center |
| `ANCHOR_LEFT_LOWER` | Lower-left corner |
| `ANCHOR_LOWER` | Bottom center |
| `ANCHOR_RIGHT_LOWER` | Lower-right corner |
| `ANCHOR_RIGHT` | Right center |
| `ANCHOR_RIGHT_UPPER` | Upper-right corner |
| `ANCHOR_UPPER` | Top center |
| `ANCHOR_CENTER` | Exact center |

> `OBJ_BUTTON`, `OBJ_RECTANGLE_LABEL`, `OBJ_EDIT`, `OBJ_CHART` have fixed `ANCHOR_LEFT_UPPER`.

## ENUM_ARROW_ANCHOR — `OBJPROP_ANCHOR` for `OBJ_ARROW` only

| ID | Description |
|----|-------------|
| `ANCHOR_TOP` | Anchor on top side |
| `ANCHOR_BOTTOM` | Anchor on bottom side |

## ENUM_ELLIOT_WAVE_DEGREE — `OBJPROP_DEGREE` on `OBJ_ELLIOTWAVE5`/`OBJ_ELLIOTWAVE3`

| ID | Description |
|----|-------------|
| `ELLIOTT_GRAND_SUPERCYCLE` | Grand Supercycle |
| `ELLIOTT_SUPERCYCLE` | Supercycle |
| `ELLIOTT_CYCLE` | Cycle |
| `ELLIOTT_PRIMARY` | Primary |
| `ELLIOTT_INTERMEDIATE` | Intermediate |
| `ELLIOTT_MINOR` | Minor |
| `ELLIOTT_MINUTE` | Minute |
| `ELLIOTT_MINUETTE` | Minuette |
| `ELLIOTT_SUBMINUETTE` | Subminuette |

## ENUM_GANN_DIRECTION — `OBJPROP_DIRECTION` on `OBJ_GANNFAN`/`OBJ_GANNGRID`

| ID | Description |
|----|-------------|
| `GANN_UP_TREND` | Uptrend direction |
| `GANN_DOWN_TREND` | Downtrend direction |

## Object Visibility Flags — `OBJPROP_TIMEFRAMES` (bitmask)

| ID | Value | Timeframe |
|----|-------|-----------|
| `OBJ_NO_PERIODS` | 0 | Not drawn anywhere |
| `OBJ_PERIOD_M1` | 0x00000001 | M1 |
| `OBJ_PERIOD_M2` | 0x00000002 | M2 |
| `OBJ_PERIOD_M3` | 0x00000004 | M3 |
| `OBJ_PERIOD_M4` | 0x00000008 | M4 |
| `OBJ_PERIOD_M5` | 0x00000010 | M5 |
| `OBJ_PERIOD_M6` | 0x00000020 | M6 |
| `OBJ_PERIOD_M10` | 0x00000040 | M10 |
| `OBJ_PERIOD_M12` | 0x00000080 | M12 |
| `OBJ_PERIOD_M15` | 0x00000100 | M15 |
| `OBJ_PERIOD_M20` | 0x00000200 | M20 |
| `OBJ_PERIOD_M30` | 0x00000400 | M30 |
| `OBJ_PERIOD_H1` | 0x00000800 | H1 |
| `OBJ_PERIOD_H2` | 0x00001000 | H2 |
| `OBJ_PERIOD_H3` | 0x00002000 | H3 |
| `OBJ_PERIOD_H4` | 0x00004000 | H4 |
| `OBJ_PERIOD_H6` | 0x00008000 | H6 |
| `OBJ_PERIOD_H8` | 0x00010000 | H8 |
| `OBJ_PERIOD_H12` | 0x00020000 | H12 |
| `OBJ_PERIOD_D1` | 0x00040000 | D1 |
| `OBJ_PERIOD_W1` | 0x00080000 | W1 |
| `OBJ_PERIOD_MN1` | 0x00100000 | MN1 |
| `OBJ_ALL_PERIODS` | 0x001FFFFF | All timeframes |
