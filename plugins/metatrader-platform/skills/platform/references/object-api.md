# Object API — MQL5 Programmatic Drawing Object Manipulation

MQL5 functions for creating, configuring, and destroying graphical objects
on charts. Distinct from the `constants` skill which holds
`ENUM_OBJECT_PROPERTY_*` constant tables.

---

## Object Lifecycle

| Function | Signature | Returns | Purpose |
|----------|-----------|---------|---------|
| `ObjectCreate` | `ObjectCreate(long chart_id, string name, ENUM_OBJECT type, int nwin, datetime time1, double price1, ...)` | `bool` | Creates a named graphical object. Up to 30 anchor time/price pairs. |
| `ObjectDelete` | `ObjectDelete(long chart_id, string name)` | `bool` | Deletes object by exact name. |
| `ObjectDeleteAll` | `ObjectDeleteAll(long chart_id, string prefix, int window=-1, int type=-1)` | `int` | Deletes all objects whose names start with `prefix`; optional window and type filter. Returns count deleted. |

---

## Object Property Get/Set

> Canonical MQL5 reference: [ObjectGetInteger](https://www.mql5.com/en/docs/objects/objectgetinteger) · [ObjectGetDouble](https://www.mql5.com/en/docs/objects/objectgetdouble) · [ObjectGetString](https://www.mql5.com/en/docs/objects/objectgetstring) · [ObjectSetInteger](https://www.mql5.com/en/docs/objects/objectsetinteger)

| Function | Signature | Purpose |
|----------|-----------|---------|
| `ObjectGetInteger` | `ObjectGetInteger(long chart_id, string name, ENUM_OBJECT_PROPERTY_INTEGER prop_id, int modifier=0)` | Read integer/bool/color/datetime property |
| `ObjectGetDouble` | `ObjectGetDouble(long chart_id, string name, ENUM_OBJECT_PROPERTY_DOUBLE prop_id, int modifier=0)` | Read double property |
| `ObjectGetString` | `ObjectGetString(long chart_id, string name, ENUM_OBJECT_PROPERTY_STRING prop_id, int modifier=0)` | Read string property (e.g. text, tooltip) |
| `ObjectSetInteger` | `ObjectSetInteger(long chart_id, string name, ENUM_OBJECT_PROPERTY_INTEGER prop_id, long value)` | Write integer property |
| `ObjectSetDouble` | `ObjectSetDouble(long chart_id, string name, ENUM_OBJECT_PROPERTY_DOUBLE prop_id, double value)` | Write double property |
| `ObjectSetString` | `ObjectSetString(long chart_id, string name, ENUM_OBJECT_PROPERTY_STRING prop_id, string value)` | Write string property |

All two-variant functions (return value directly, or return bool + write to
reference parameter) follow the same pattern as `ChartGetInteger`.

---

## Object Discovery and Positioning

> Canonical MQL5 reference: [ObjectFind](https://www.mql5.com/en/docs/objects/objectfind) · [ObjectName](https://www.mql5.com/en/docs/objects/objectname) · [ObjectsTotal](https://www.mql5.com/en/docs/objects/objectstotal) · [ObjectMove](https://www.mql5.com/en/docs/objects/objectmove)

| Function | Signature | Returns | Purpose |
|----------|-----------|---------|---------|
| `ObjectFind` | `ObjectFind(long chart_id, string name)` | `int` | Returns subwindow index of the named object, or -1 if not found |
| `ObjectName` | `ObjectName(long chart_id, int pos, int window=-1, int type=-1)` | `string` | Returns the name of the object at position `pos`; optional window and type filter |
| `ObjectsTotal` | `ObjectsTotal(long chart_id, int window=-1, int type=-1)` | `int` | Returns count of objects; optional filter by subwindow and type |
| `ObjectMove` | `ObjectMove(long chart_id, string name, int point_index, datetime time, double price)` | `bool` | Moves the anchor point at `point_index` to new time/price |
| `ObjectGetValueByTime` | `ObjectGetValueByTime(long chart_id, string name, datetime time, int line_id)` | `double` | Returns the price value of a line object at a given time |
| `ObjectGetTimeByValue` | `ObjectGetTimeByValue(long chart_id, string name, double value, int line_id)` | `datetime` | Returns the time at which a line object crosses a given price |

---

## Text Rendering to Chart Pixel Context

> Canonical MQL5 reference: [TextSetFont](https://www.mql5.com/en/docs/objects/textsetfont) · [TextOut](https://www.mql5.com/en/docs/objects/textout) · [TextGetSize](https://www.mql5.com/en/docs/objects/textgetsize)

| Function | Signature | Purpose |
|----------|-----------|---------|
| `TextSetFont` | `TextSetFont(string name, int size, uint flags=0, int angle=0)` | Sets font for subsequent `TextOut` calls |
| `TextOut` | `TextOut(string text, int x, int y, uint anchor, color clr, uchar opacity)` | Writes text to a resource bitmap at pixel coordinates |
| `TextGetSize` | `TextGetSize(const string text, uint &width, uint &height)` | Returns pixel dimensions of text in current font |

---

## References

- `docs/mql5_com_-_docs/objects.md`
- `docs/mql5_com_-_docs/objects-objectcreate.md`
- `docs/mql5_com_-_docs/objects-objectdelete.md`
- `docs/mql5_com_-_docs/objects-objectdeleteall.md`
- `docs/mql5_com_-_docs/objects-objectfind.md`
- `docs/mql5_com_-_docs/objects-objectgetdouble.md`
- `docs/mql5_com_-_docs/objects-objectgetinteger.md`
- `docs/mql5_com_-_docs/objects-objectgetstring.md`
- `docs/mql5_com_-_docs/objects-objectgettimebyvalue.md`
- `docs/mql5_com_-_docs/objects-objectgetvaluebytime.md`
- `docs/mql5_com_-_docs/objects-objectmove.md`
- `docs/mql5_com_-_docs/objects-objectname.md`
- `docs/mql5_com_-_docs/objects-objectsetdouble.md`
- `docs/mql5_com_-_docs/objects-objectsetinteger.md`
- `docs/mql5_com_-_docs/objects-objectsetstring.md`
- `docs/mql5_com_-_docs/objects-objectstotal.md`
- `docs/mql5_com_-_docs/objects-textgetsize.md`
- `docs/mql5_com_-_docs/objects-textout.md`
- `docs/mql5_com_-_docs/objects-textsetfont.md`
