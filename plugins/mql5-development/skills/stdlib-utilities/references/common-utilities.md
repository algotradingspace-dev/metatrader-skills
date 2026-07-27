# Common Utilities — Journal Output, Alerts, Execution Control, Tester, Pointers

## Journal Output, Alerts, and Execution Control

| Function group | What it covers | Usage note |
|----------------|----------------|------------|
| `Print`, `PrintFormat`, `Comment` | Journal and chart-surface output | Use `PrintFormat` for structured logs and `Comment` only for transient chart overlays |
| `Alert`, `MessageBox`, `PlaySound` | Interactive notifications | Avoid blocking or intrusive calls in latency-sensitive event paths |
| `Sleep`, `ExpertRemove`, `TerminalClose`, `DebugBreak` | Execution control | These change or pause program state and should be rare in production event handlers |
| `ResetLastError`, `SetUserError` | Error-state management | Use to bracket risky calls or report user-domain failures consistently |

## Tester, Resources, Pointers, and Miscellaneous Runtime Utilities

| Function group | What it covers | Usage note |
|----------------|----------------|------------|
| `TesterDeposit`, `TesterWithdrawal`, `TesterHideIndicators`, `TesterStatistics`, `TesterStop`, `TesterKeyDown` | Tester-only utilities | Guard them so live runs do not assume tester context |
| `ResourceCreate`, `ResourceFree`, `ResourceReadImage`, `ResourceSave` | Embedded resource management | Use when an EA or indicator needs packaged images or generated assets |
| `CheckPointer`, `GetPointer`, `ZeroMemory` | Memory and pointer helpers | Treat raw pointer work as defensive-code territory, not normal business logic |
| `GetMicrosecondCount`, `GetTickCount64`, `PeriodSeconds`, `TranslateKey`, `CryptEncode`, `CryptDecode` | Timers, key translation, and lightweight crypto | Helpful for profiling, keyboard mapping, time scaling, and simple transport encoding |
