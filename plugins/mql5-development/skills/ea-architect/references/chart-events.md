# Chart Events — OnChartEvent Reference

## OnChartEvent Signature

```mql5
void OnChartEvent(const int id,
                  const long   &lparam,
                  const double &dparam,
                  const string &sparam)
{
   switch(id)
   {
      case CHARTEVENT_CLICK:
         // lparam = bar index, dparam = price at click
         break;
      case CHARTEVENT_OBJECT_CLICK:
         // sparam = clicked object name
         break;
      case CHARTEVENT_KEYDOWN:
         // lparam = key code (e.g. VK_SPACE = 32)
         break;
      default:
         if(id >= CHARTEVENT_CUSTOM && id <= CHARTEVENT_CUSTOM_LAST)
         {
            // Custom event: id - CHARTEVENT_CUSTOM = event number
         }
         break;
   }
}
```

---

## Custom Events

```mql5
EventChartCustom(targetChartId, (ushort)N, lparam, dparam, sparam);
// Receiver sees id = CHARTEVENT_CUSTOM + N
```

- Up to 65535 custom event IDs (0–65534 offset from `CHARTEVENT_CUSTOM`)
- Enable `CHART_EVENT_MOUSE_MOVE` / `CHART_EVENT_OBJECT_CREATE` / `CHART_EVENT_OBJECT_DELETE` via `ChartSetInteger` to receive those events

---

## When to Use

- Adding clickable chart buttons that trigger EA actions
- Detecting keyboard input for manual intervention or dashboard control
- Communicating between multiple EAs on different charts via custom events

---

## References

- `docs/mql5_com_-_docs/event_handlers-onchartevent.md`
- `docs/mql5_com_-_docs/constants-chartconstants-enum_chartevents.md`
