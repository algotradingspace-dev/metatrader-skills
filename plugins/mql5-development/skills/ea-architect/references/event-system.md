# Event System — Timer and Custom Chart Events

## Timer Functions

> Canonical MQL5 reference: [EventSetTimer](https://www.mql5.com/en/docs/eventfunctions/eventsettimer) · [OnInit](https://www.mql5.com/en/docs/event_handlers/oninit) · [EventSetMillisecondTimer](https://www.mql5.com/en/docs/eventfunctions/eventsetmillisecondtimer) · [EventKillTimer](https://www.mql5.com/en/docs/eventfunctions/eventkilltimer)

| Function | Return | Description |
|----------|--------|-------------|
| `EventSetTimer(int seconds)` | `bool` | Registers a periodic timer; call in `OnInit()` |
| `EventSetMillisecondTimer(int ms)` | `bool` | High-resolution timer (period < 1 s); call in `OnInit()` |
| `EventKillTimer()` | `void` | Stops the timer; call in `OnDeinit()` |
| `EventChartCustom(chart_id, event_id, lparam, dparam, sparam)` | `bool` | Posts a custom event to target chart's queue |

---

## Timer Lifecycle — Standard Pattern

```mql5
int OnInit() {
   EventSetTimer(5);           // fire OnTimer every 5 seconds
   return INIT_SUCCEEDED;
}

void OnTimer() {
   // periodic work: heartbeat, external data check, dashboard update
}

void OnDeinit(const int reason) {
   EventKillTimer();           // always kill
}
```

---

## Timer Rules

- **One timer per program** — calling `EventSetTimer` twice replaces the first timer
- **Auto-destroyed** if the program stops without an explicit `EventKillTimer` call
- **Queue dedup** — if a Timer event is already queued or being processed, the new event is dropped (no accumulation)
- **Millisecond timer**: hardware floor is ~10–16 ms regardless of argument; higher frequency increases CPU load and test run time proportionally

**`EventSetMillisecondTimer` vs `EventSetTimer`:**
```
Use EventSetMillisecondTimer when:  event rate > 1 Hz (DOM refresh, tick dashboard)
Use EventSetTimer when:             event rate <= 1 Hz (position monitor, periodic writes)
Caution:                            faster timer -> more CPU; tester run time scales proportionally
```

---

## EventChartCustom — Cross-Chart and Cross-Program Events

```mql5
// Sender dispatches a custom event to another chart:
long targetChart = ChartFirst();
EventChartCustom(targetChart, 1, lparam, dparam, sparam);
// Actual CHARTEVENT id received by target = CHARTEVENT_CUSTOM + 1 (i.e., 1001)

// Receiver must have OnChartEvent:
void OnChartEvent(const int id, const long& lparam,
                  const double& dparam, const string& sparam) {
   if(id == CHARTEVENT_CUSTOM + 1) {
      // handle event
   }
}
```

- `sparam` is **truncated to 63 characters** — use for short labels or identifiers only
- Returns `false` if target chart's event queue is full — caller must decide whether to retry
- If target chart has no `OnChartEvent` handler, the event is silently discarded

---

## References

- `docs/mql5_com_-_docs/eventfunctions.md`
- `docs/mql5_com_-_docs/eventfunctions-eventsettimer.md`
- `docs/mql5_com_-_docs/eventfunctions-eventkilltimer.md`
- `docs/mql5_com_-_docs/eventfunctions-eventsetmillisecondtimer.md`
- `docs/mql5_com_-_docs/eventfunctions-eventchartcustom.md`
