---
name: stdlib-utilities
description: >
  MQL4/MQL5 language and runtime utilities reference skill. Use for: magic
  number isolation; OrderSend retry logic; .set file parameter presets; MQL4
  vs MQL5 differences; file I/O and sandbox rules; string manipulation; array
  operations; date/time functions; terminal global variables; SQLite database
  access; runtime error codes; type conversion; matrix/vector stubs. Trigger:
  "magic number", "OrderSend retry", ".set file", "MQL4 vs MQL5", "file I/O",
  "string functions", "array functions", "date and time", "global variables",
  "database", "type conversion", "runtime error", "MqlDateTime",
  "terminal global".
---

# Standard Library Utilities

Language-level reference for MQL4/MQL5 standard library functions, runtime
utilities, and development conventions.

This is a Reference skill: the body is a routing table into `references/`.
Read the relevant reference file for the function family you need.

---

## Purpose

Catalogs the MQL5 standard library and runtime utility surface — everything
from string manipulation and file I/O to database access, math functions,
and terminal global variables. The initial "Development Standards" section
covers EA structure conventions, input parameter grouping, error handling
patterns, .set file presets, and MQL4 vs MQL5 differences.

---

## When to Use

- Looking up a specific function family: file I/O, strings, arrays, math,
  time, conversion, database, global vars
- Structuring EA input parameters and magic numbers
- Implementing OrderSend retry logic
- Creating .set file presets
- Understanding MQL4 vs MQL5 differences before porting code
- Checking runtime error code ranges or trade return codes

**Do NOT use** for:
- EA architecture / 5-layer module wiring → use `ea-architect`
- ENUM_* constant tables (chart, trade, object properties) → use `constants`
- Indicator buffer/plot setup → use `ea-architect` reference `custom-indicators.md`

---

## References

| File | Contents | Read when |
|------|----------|-----------|
| `references/dev-standards.md` | EA header template, input grouping, magic number rules, mandatory components, OrderSend retry, .set presets, MQL4 vs MQL5 | Starting a new EA; structuring inputs; setting up presets |
| `references/program-context.md` | `MQLInfoInteger`/`MQLInfoString`, `ENUM_PROGRAM_TYPE`, `MqlDateTime`, `TerminalInfo*`, program lifecycle, `IsStopped` | Checking tester/trade/dll permissions; resolving data paths; runtime identity |
| `references/error-codes.md` | Runtime error code ranges, `TRADE_RETCODE_*` return codes | Debugging OrderSend failures; mapping GetLastError() values |
| `references/named-constants.md` | `ENUM_POINTER_TYPE`, `REASON_*` uninit codes, `ENUM_DATATYPE`, math constants, compile macros, `EMPTY_VALUE`, `INVALID_HANDLE` | `CheckPointer()` usage; OnDeinit reason handling; data type lookup |
| `references/file-io.md` | File sandbox rules, `FileOpen` flags, text/binary read/write, `FileFindFirst`/`FileFindNext`/`FileFindClose`, `FileCopy`, `FolderCreate` | Reading/writing EA data files; file search; folder management |
| `references/time-date.md` | `TimeCurrent`, `TimeTradeServer`, `TimeLocal`, `TimeGMT`, `TimeToStruct`, `StructToTime`, calendar field helpers | Broker-aligned time handling; timestamp conversion |
| `references/strings.md` | `StringAdd`, `StringConcatenate`, `StringFind`, `StringReplace`, `StringSplit`, `StringTrimLeft`, `StringTrimRight`, `StringToLower` | Building or parsing strings; CSV tokenization; case normalization |
| `references/conversions.md` | `DoubleToString`, `StringToDouble`, `NormalizeDouble`, `StringFormat`, `ColorToString`, `TimeToString`, `StructToCharArray` | Formatting output; parsing input; color/time serialization |
| `references/arrays.md` | `ArrayResize`, `ArrayCopy`, `ArraySetAsSeries`, `ArraySort`, `ArrayBsearch`, `ArrayMaximum`, `ArrayInsert`, `ArrayToFP16` | Dynamic array management; search/sort; series orientation |
| `references/math.md` | `MathSin`/`Cos`/`Tan`, `MathExp`/`Log`/`Pow`, `MathFloor`/`Ceil`/`Round`, `MathRand`, `MathIsValidNumber` | Indicator math; risk calculations; floating-point safety |
| `references/common-utilities.md` | `Print`/`PrintFormat`, `Alert`, `Sleep`, `ExpertRemove`, `TesterStatistics`, `CheckPointer`, `GetMicrosecondCount`, `CryptEncode` | Logging; tester utilities; memory/pointer helpers; profiling |
| `references/global-variables.md` | `GlobalVariableSet`, `GlobalVariableGet`, `GlobalVariableSetOnCondition`, `GlobalVariableTemp` | Cross-session flags; inter-program coordination |
| `references/database.md` | `DatabaseOpen`, `DatabasePrepare`, `DatabaseBind`, `DatabaseRead`, `DatabaseExecute`, transactions, import/export | SQLite storage in MQL5; prepared statements; bulk writes |
| `references/matrix-stub.md` | `matrix<T>`/`vector<T>` function catalog — init, manipulations, products, statistics, transformations, ML | Matrix/vector numerical work; linear algebra in MQL5 |
