# Time and Date — Clock Sources, Offsets, and Struct Conversion

Time handling in MQL5 matters because not all clocks mean the same thing:
local OS time, GMT, trade-server time, and tick-refreshed current time can
differ materially in live systems.

## Current Time Sources

> Canonical MQL5 reference: [TimeCurrent](https://www.mql5.com/en/docs/dateandtime/timecurrent) · [TimeTradeServer](https://www.mql5.com/en/docs/dateandtime/timetradeserver) · [TimeLocal](https://www.mql5.com/en/docs/dateandtime/timelocal) · [TimeGMT](https://www.mql5.com/en/docs/dateandtime/timegmt)

| Function group | What it covers | Usage note |
|----------------|----------------|------------|
| `TimeCurrent`, `TimeTradeServer`, `TimeLocal`, `TimeGMT` | Current clock sources | Use trade-server time for broker-aligned scheduling and local time only for workstation-level diagnostics |
| `TimeGMTOffset`, `TimeDaylightSavings` | Offset and DST context | These are environment aids, not a replacement for broker-session logic |
| `TimeToStruct`, `StructToTime` | `datetime` and `MqlDateTime` conversion | Use these when you need explicit calendar fields instead of raw timestamps |
| `Day`, `DayOfWeek`, `DayOfYear`, `Hour`, `Minute`, `Month`, `Seconds`, `TimeDayOfWeek`, `TimeDayOfYear`, `TimeHour`, `TimeMinute`, `TimeMonth`, `TimeSeconds`, `TimeYear`, `Year` | Calendar-field extraction helpers | Prefer them for lightweight field reads when you do not need a full struct |

## Time Gotchas

- `TimeCurrent()` is broker/event-driven rather than a continuously advancing
  local wall clock
- Session logic should name which clock it relies on, because mixing local and
  server time is a common production bug
