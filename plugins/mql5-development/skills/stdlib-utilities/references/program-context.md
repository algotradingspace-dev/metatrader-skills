# Program Context — Runtime Identity, Terminal State, and Lifecycle

## ENUM_MQL_INFO_INTEGER — `MQLInfoInteger(id)`

| Identifier | Description | Type |
|------------|-------------|------|
| `MQL_HANDLES_USED` | Active object handle count | int |
| `MQL_MEMORY_LIMIT` | Max dynamic memory for program (MB) | int |
| `MQL_MEMORY_USED` | Memory currently used (MB) | int |
| `MQL_PROGRAM_TYPE` | Program type | `ENUM_PROGRAM_TYPE` |
| `MQL_DLLS_ALLOWED` | DLL usage permitted | bool |
| `MQL_TRADE_ALLOWED` | Trading permitted | bool |
| `MQL_SIGNALS_ALLOWED` | Signal modification permitted | bool |
| `MQL_DEBUG` | Running in debugger | bool |
| `MQL_PROFILER` | Running in code profiler | bool |
| `MQL_TESTER` | Running in Strategy Tester | bool |
| `MQL_FORWARD` | Running in forward test pass | bool |
| `MQL_OPTIMIZATION` | Running in optimization | bool |
| `MQL_VISUAL_MODE` | Running in visual test mode | bool |
| `MQL_FRAME_MODE` | Running in frame-gathering mode | bool |
| `MQL_LICENSE_TYPE` | License type of EX5 module | `ENUM_LICENSE_TYPE` |
| `MQL_STARTED_FROM_CONFIG` | Launched from terminal config startup | bool |

## ENUM_MQL_INFO_STRING — `MQLInfoString(id)`

`MQL_PROGRAM_NAME` · `MQL_PROGRAM_PATH`

## ENUM_PROGRAM_TYPE

| Value | Description |
|-------|-------------|
| `PROGRAM_EXPERT` | Expert Advisor |
| `PROGRAM_SCRIPT` | Script |
| `PROGRAM_INDICATOR` | Custom indicator |
| `PROGRAM_SERVICE` | Service |

## MqlDateTime Structure

```mql5
struct MqlDateTime {
   int year;       // Year
   int mon;        // Month  (1–12)
   int day;        // Day    (1–31)
   int hour;       // Hour   (0–23)
   int min;        // Minute (0–59)
   int sec;        // Second (0–59)
   int day_of_week;// 0=Sunday … 6=Saturday
   int day_of_year;// 0=Jan 1 … 364/365
};
```

> Populate via `TimeToStruct(TimeCurrent(), dt)`.
> Runtime detection pattern: `if(MQLInfoInteger(MQL_TESTER)) { /* tester-only init */ }`.
> `MQL_FRAME_MODE` is true during the optimization result collection phase (`OnTesterPass`).

## Runtime Context Checks

| Function group | What it covers | Usage note |
|----------------|----------------|------------|
| `MqlInfoInteger`, `MqlInfoString` | Program identity and execution-mode checks | Use to branch for tester, optimization, or visual-mode behaviour |
| `TerminalInfoInteger`, `TerminalInfoDouble`, `TerminalInfoString` | Terminal capability and path inspection | Resolve data paths, environment info, and terminal configuration facts here |
| `IsStopped`, `UninitializeReason`, `LastError` | Shutdown and last-error context | Query these before assuming long loops or delayed work can continue safely |
| `Symbol`, `Period`, `Digits`, `Point` | Chart-context and symbol-shape helpers | Prefer compiler constants like `_Point` when available, but these remain useful in generic helpers |

## Program Runtime Model

| Topic | Practical rule |
|-------|----------------|
| EA lifetime | One EA can be attached per chart and keeps running until removed, chart state changes force deinit, or terminal state stops it |
| Indicator lifetime | Indicators persist with the chart and can stack in unlimited count per chart |
| Script lifetime | Scripts are one-shot programs and do not survive terminal restart or chart-state changes |
| Service lifetime | Services are chartless background workers suited to auxiliary tasks such as continuously updating custom symbols |
| AutoTrading | EA execution is still gated by the terminal AutoTrading state |
