# Tester Journal Patterns and Agent Architecture

## Journal Message Patterns

| Journal Entry | Meaning / Action |
|---------------|------------------|
| `start time changed to YYYY.MM.DD to provide data at beginning` | Not an error — insufficient history, start shifted forward |
| `Tester stop out occurred on X% of testing interval` | EA hit stop-out, balance depleted |
| `array out of range in 'EA.mq5' (line, col)` | Critical bug — array index OOB, EA terminates |
| `zero divide in 'EA.mq5' (line, col)` | Critical bug — division by zero, EA terminates |
| `tester stopped because OnInit failed` | OnInit returned something other than INIT_SUCCEEDED |
| `tick volumes not matched for N minute bars` | Tick quality issue — minor, usually acceptable |
| `last prices absent for N minute bars, bid prices used` | Exchange instrument tested with missing Last prices |

## Testing Agent Architecture

```
Local agents:  #cores = #agents; created automatically; each is an isolated process
Remote agents: require MetaTester (metatester64.exe); 64-bit only; DLL calls prohibited
Cloud agents:  MQL5 Cloud Network; DLL + Print() logs not available
Agent cache:   remains active 5 min after test; compressed history reused across tests
Data exchange: MD5 hashes used — only changed parameter blocks retransmitted
```

## Agent Limitations on Remote/Cloud

- `Print()` output not logged
- Trade operation messages not logged
- DLL calls completely prohibited
- Results (profit, Sharpe, OnTester value) are returned to platform

## Global Variables During Testing

- Tester emulates platform global variables (`GlobalVariable*` functions)
- These are **separate** from the platform's real global variables
- Each testing agent has its own isolated copy

## TimeLocal/TimeTradeServer/TimeGMT During Tests

- All three return identical values (always equal to GMT)
- This is intentional for reproducibility
