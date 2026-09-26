# Named Constants — Pointer Types, Uninit Reasons, Data Types, Math, Compile Macros

## ENUM_POINTER_TYPE — `CheckPointer(ptr)`

| Value | Description |
|-------|-------------|
| `POINTER_INVALID` | Incorrect pointer — stop, do not use |
| `POINTER_DYNAMIC` | Created by `new()` — call `delete()` when done |
| `POINTER_AUTOMATIC` | Auto-managed by MQL5 — do NOT call `delete()` |

## REASON_* Uninit Codes — `UninitializeReason()` in `OnDeinit`

> Canonical MQL5 reference: [REASON_PROGRAM](https://www.mql5.com/en/docs/constants/namedconstants/uninit) · [ExpertRemove](https://www.mql5.com/en/docs/common/expertremove) · [REASON_INITFAILED](https://www.mql5.com/en/docs/constants/namedconstants/uninit#reason_initfailed) · [OnInit](https://www.mql5.com/en/docs/event_handlers/oninit)

| Code | Constant | Description |
|------|----------|-------------|
| 0 | `REASON_PROGRAM` | EA called `ExpertRemove()` |
| 1 | `REASON_REMOVE` | Program deleted from chart |
| 2 | `REASON_RECOMPILE` | Program recompiled |
| 3 | `REASON_CHARTCHANGE` | Symbol or TF changed |
| 4 | `REASON_CHARTCLOSE` | Chart closed |
| 5 | `REASON_PARAMETERS` | Input parameters changed |
| 6 | `REASON_ACCOUNT` | Account changed / reconnect |
| 7 | `REASON_TEMPLATE` | New template applied |
| 8 | `REASON_INITFAILED` | `OnInit()` returned non-zero |
| 9 | `REASON_CLOSE` | Terminal closed |

> Pattern: `if(reason == REASON_CHARTCHANGE) SaveState(); else CleanUp();`

## ENUM_DATATYPE — Data Types for `MqlParam.type`

| Value | MQL5 type | Value | MQL5 type |
|-------|-----------|-------|-----------|
| `TYPE_BOOL` | bool | `TYPE_UINT` | uint |
| `TYPE_CHAR` | char | `TYPE_LONG` | long |
| `TYPE_UCHAR` | uchar | `TYPE_ULONG` | ulong |
| `TYPE_SHORT` | short | `TYPE_FLOAT` | float |
| `TYPE_USHORT` | ushort | `TYPE_DOUBLE` | double |
| `TYPE_INT` | int | `TYPE_STRING` | string |
| `TYPE_COLOR` | color | `TYPE_DATETIME` | datetime |

## Mathematical Constants

| Constant | Value | Constant | Value |
|----------|-------|----------|-------|
| `M_PI` | 3.14159265358979 | `M_E` | 2.71828182845905 |
| `M_PI_2` | p/2 | `M_LN2` | ln(2) = 0.693147 |
| `M_SQRT2` | v2 = 1.41421 | `M_LOG10E` | log10(e) = 0.43429 |

## Other Useful Constants

> Canonical MQL5 reference: [EMPTY_VALUE](https://www.mql5.com/en/docs/constants/namedconstants/otherconstants) · [DBL_MAX](https://www.mql5.com/en/docs/constants/namedconstants/typeconstants)

| Constant | Value | Description |
|----------|-------|-------------|
| `NULL` | 0 | Zero for any type |
| `EMPTY_VALUE` | `DBL_MAX` | Empty indicator buffer value |
| `INVALID_HANDLE` | -1 | Invalid file/indicator handle |
| `WHOLE_ARRAY` | -1 | Process entire array |
| `WRONG_VALUE` | -1 | Casts to any enum type |
| `clrNONE` | -1 | No color (hide object/plot) |
| `CHARTS_MAX` | 100 | Max simultaneous open charts |

## Compile-Time Macros

| Macro | Description |
|-------|-------------|
| `__FILE__` | Source file name |
| `__LINE__` | Current line number |
| `__FUNCTION__` | Current function name |
| `__FUNCSIG__` | Full function signature |
| `__DATE__` | Compilation date |
| `__DATETIME__` | Compilation date + time |
| `__MQLBUILD__` | Build number |
