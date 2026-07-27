# Trade Signals Subscription API

Use these functions to enumerate signals available in the terminal, read
signal metadata, configure copy settings, and manage subscriptions
programmatically from an EA or script.

## Signal Base — Enumeration and Property Read

| Function | Signature | Returns | Purpose |
|----------|-----------|---------|---------|
| `SignalBaseTotal` | `SignalBaseTotal()` | `int` | Total signals available in terminal |
| `SignalBaseSelect` | `SignalBaseSelect(int index)` | `bool` | Selects a signal by index for subsequent `SignalBaseGet*` calls |
| `SignalBaseGetDouble` | `SignalBaseGetDouble(ENUM_SIGNAL_BASE_DOUBLE)` | `double` | Reads a double property of the selected signal |
| `SignalBaseGetInteger` | `SignalBaseGetInteger(ENUM_SIGNAL_BASE_INTEGER)` | `long` | Reads an integer property |
| `SignalBaseGetString` | `SignalBaseGetString(ENUM_SIGNAL_BASE_STRING)` | `string` | Reads a string property |

`SignalBaseSelect` must be called before any `SignalBaseGet*` call; it sets
the implicit selection context.

## Signal Info — Copy Settings Read/Write

| Function | Signature | Returns | Purpose |
|----------|-----------|---------|---------|
| `SignalInfoGetDouble` | `SignalInfoGetDouble(ENUM_SIGNAL_INFO_DOUBLE)` | `double` | Reads a double copy-setting |
| `SignalInfoGetInteger` | `SignalInfoGetInteger(ENUM_SIGNAL_INFO_INTEGER)` | `long` | Reads an integer copy-setting |
| `SignalInfoGetString` | `SignalInfoGetString(ENUM_SIGNAL_INFO_STRING)` | `string` | Reads a string copy-setting |
| `SignalInfoSetDouble` | `SignalInfoSetDouble(ENUM_SIGNAL_INFO_DOUBLE, double)` | `bool` | Writes a double copy-setting |
| `SignalInfoSetInteger` | `SignalInfoSetInteger(ENUM_SIGNAL_INFO_INTEGER, long)` | `bool` | Writes an integer copy-setting |

## Subscription Management

| Function | Signature | Returns | Purpose |
|----------|-----------|---------|---------|
| `SignalSubscribe` | `SignalSubscribe(long signal_id)` | `bool` | Subscribes to the signal with the given ID |
| `SignalUnsubscribe` | `SignalUnsubscribe()` | `bool` | Cancels the current signal subscription |

## Enumerate-and-Filter Pattern

```mql5
int total = SignalBaseTotal();
for(int i = 0; i < total; i++) {
    if(!SignalBaseSelect(i)) continue;
    long   id        = SignalBaseGetInteger(SIGNAL_BASE_ID);
    string name      = SignalBaseGetString(SIGNAL_BASE_NAME);
    double price     = SignalBaseGetDouble(SIGNAL_BASE_PRICE);
    long   pips      = SignalBaseGetInteger(SIGNAL_BASE_PIPS);
    long   subs      = SignalBaseGetInteger(SIGNAL_BASE_SUBSCRIBERS);
    if(price == 0.0 && pips > 0 && subs > 0)
        PrintFormat("id=%d name=%s pips=%d subscribers=%d", id, name, pips, subs);
}
```
