# Terminal Global Variables — Cross-Session State

Terminal global variables are the lightweight persistence mechanism shared
across programs and restarts on the same terminal installation.

> Canonical MQL5 reference: [GlobalVariableSet](https://www.mql5.com/en/docs/globals/globalvariableset) · [GlobalVariableGet](https://www.mql5.com/en/docs/globals/globalvariableget) · [GlobalVariableCheck](https://www.mql5.com/en/docs/globals/globalvariablecheck) · [GlobalVariableDel](https://www.mql5.com/en/docs/globals/globalvariabledel)

| Function group | What it covers | Usage note |
|----------------|----------------|------------|
| `GlobalVariableSet`, `GlobalVariableGet`, `GlobalVariableCheck`, `GlobalVariableDel` | Basic CRUD | Use for small cross-session flags and counters, not large datasets |
| `GlobalVariableSetOnCondition` | Compare-and-set style update | This is the safest update path when multiple programs may contend for the same key |
| `GlobalVariableTemp`, `GlobalVariableTime` | Temporary vars and timestamp lookup | Helpful for expiring coordination flags or observing refresh age |
| `GlobalVariablesFlush`, `GlobalVariablesDeleteAll`, `GlobalVariableName`, `GlobalVariablesTotal` | Persistence and enumeration | Flush only when immediate disk durability matters |
