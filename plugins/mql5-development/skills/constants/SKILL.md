---
name: constants
description: >
  Canonical reference skill for MQL5 ENUM_* values, flag combinations, and
  property identifiers. Use for: looking up any ENUM_* name or property
  identifier; valid values for AccountInfo*, TerminalInfo*, Chart*, Object*,
  File* calls; combining bitmask flags (file modes, visibility, fill policy);
  trade return codes, runtime error codes, symbol property enums, Web colors,
  Wingdings codes, MessageBox constants. Trigger: "what does ENUM_ mean",
  "MQL5 error code", "property identifier", "valid values", "ENUM_SYMBOL_",
  "ENUM_ACCOUNT_", "ENUM_OBJECT_", "file flags", "Wingdings", "trade return
  code", "chart property", "OBJPROP_", "OrderGetInteger", "PositionGetDouble".
---

# Constants

Canonical reference for MQL5 constant enums, bit flags, and property
identifiers.

This is a Reference skill: the body is a routing table into `references/`.
Read the relevant reference file for the enum family you need.

---

## Purpose

Catalogs every MQL5 enum family, property identifier, and bitmask flag used
in the MQL5 API — account info, terminal info, chart events and properties,
file I/O flags, object types and properties, symbol info, runtime error codes,
trade return codes, and account access patterns.

---

## When to Use

- Looking up any `ENUM_*` name or property identifier used by the MQL5 API
- Asking for valid values for `AccountInfo*`, `TerminalInfo*`, `Chart*`,
  `Object*`, `File*`, or similar calls
- Determining what constant to pass to an object, chart, file, or MessageBox API
- Combining flag masks such as file-open modes or object visibility periods
- Resolving color constants, Wingdings codes, and object/chart property lookups

**Do NOT use** for:
- Function signatures for indicator or trade APIs → use the relevant skill
  (`signal-engine`, `trade-manager`, `stdlib-utilities`)
- Indicator handle lifecycle → use `signal-engine` references
- EA architecture or module wiring → use `ea-architect`

---

## References

| File | Contents | Read when |
|------|----------|-----------|
| `references/account-terminal-enums.md` | `ENUM_ACCOUNT_INFO_INTEGER/DOUBLE/STRING`, `ENUM_ACCOUNT_TRADE_MODE/STOPOUT_MODE/MARGIN_MODE`, `ENUM_TERMINAL_INFO_INTEGER/STRING` | AccountInfoInteger, AccountInfoDouble, TerminalInfoInteger calls |
| `references/chart-enums.md` | `ENUM_CHART_EVENT`, `ENUM_CHART_MODE`, `ENUM_CHART_POSITION`, key `ENUM_CHART_PROPERTY_INTEGER` identifiers | OnChartEvent handling; ChartSetInteger/GetInteger property IDs |
| `references/file-io-constants.md` | File opening flags (bitmask), `ENUM_FILE_POSITION`, `ENUM_FILE_PROPERTY_INTEGER`, codepage constants, `MessageBox` return codes and type flags | FileOpen/FileGetInteger calls; MessageBox configuration |
| `references/object-type-enums.md` | `ENUM_OBJECT` (44 types), `ENUM_BASE_CORNER`, `ENUM_ANCHOR_POINT`, `ENUM_ARROW_ANCHOR`, `ENUM_ELLIOT_WAVE_DEGREE`, `ENUM_GANN_DIRECTION`, object visibility flags `OBJ_PERIOD_*` | ObjectCreate type selection; corner/anchor/visibility configuration |
| `references/object-property-enums.md` | `ENUM_OBJECT_PROPERTY_INTEGER` (47 identifiers), `ENUM_OBJECT_PROPERTY_DOUBLE` (5), `ENUM_OBJECT_PROPERTY_STRING` (7) | ObjectSetInteger/GetInteger, ObjectSetDouble, ObjectSetString calls |
| `references/web-colors-wingdings.md` | 140+ named `clrXxx` color constants, Wingdings character codes (250+ codes for `OBJ_ARROW`) | Setting OBJPROP_COLOR; OBJ_ARROW arrow code selection |
| `references/symbol-info-enums.md` | `ENUM_SYMBOL_INFO_INTEGER/DOUBLE/STRING`, `ENUM_SYMBOL_TRADE_MODE`, `SYMBOL_EXPIRATION_MODE/FILLING_MODE/ORDER_MODE` flags | SymbolInfoInteger/Double/String property lookups |
| `references/error-codes.md` | Runtime error code ranges (key examples), `TRADE_RETCODE_*` table | Mapping GetLastError() values; interpreting MqlTradeResult.retcode |
| `references/account-info-api.md` | `AccountInfoInteger/Double/String` signatures, type expectations, casting patterns, usage notes | Writing account info access code; correct accessor/property pairing |
