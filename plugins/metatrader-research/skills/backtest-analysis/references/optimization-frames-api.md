# Optimisation Frames API

Frames pass custom data from test **agents** to the optimisation **controller**
EA. Use when the `OnTester()` scalar return is not enough.

## Architecture

```
Agent EA (runs once per optimisation pass):
  OnTester()       -> FrameAdd(name, id, value, data[])   write frame(s)

Controller EA (runs in terminal, coordinates all passes):
  OnTesterPass()   -> FrameNext(pass, name, id, value, data[])  read new frames
  OnTesterDeinit() -> FrameFirst() + FrameNext() loop            catch stragglers

Frame storage: terminal_dir\MQL5\Files\Tester\<EA_name>.MQD
TesterPass event fires each time a frame arrives from any agent.
```

## Complete Function Reference

> Canonical MQL5 reference: [FrameAdd](https://www.mql5.com/en/docs/optimization_frames/frameadd) · [FrameFirst](https://www.mql5.com/en/docs/optimization_frames/framefirst) · [FrameFilter](https://www.mql5.com/en/docs/optimization_frames/framefilter) · [FrameNext](https://www.mql5.com/en/docs/optimization_frames/framenext)

| Function | Call context | Returns |
|----------|-------------|---------|
| `FrameAdd(name, id, value, data[])` | Agent — OnTester | `bool` |
| `FrameAdd(name, id, value, filename)` | Agent — OnTester | `bool` |
| `FrameFirst()` | Controller | `bool` — resets read pointer, clears filter |
| `FrameFilter(name, id)` | Controller | `bool` — set filter and reset pointer |
| `FrameNext(pass, name, id, value)` | Controller | `bool` — advance to next frame |
| `FrameNext(pass, name, id, value, data[])` | Controller | `bool` — advance + fill array |
| `FrameInputs(pass, params[], count)` | Controller | `bool` — get EA inputs for pass N |
| `ParameterGetRange(name, enable, value, start, step, stop)` | OnTesterInit/Pass/Deinit | `bool` |
| `ParameterSetRange(name, enable, value, start, step, stop)` | **OnTesterInit only** | `bool` |

## Typical Controller Pattern

```mql5
void OnTesterPass() {
   ulong pass; string name; long id; double value; double data[];
   while(FrameNext(pass, name, id, value, data))
      ProcessFrame(pass, name, id, value, data);
}

void OnTesterDeinit() {
   ulong pass; string name; long id; double value; double data[];
   FrameFirst();
   while(FrameNext(pass, name, id, value, data))
      ProcessFrame(pass, name, id, value, data);
}
```

## FrameFilter — Name/ID Combinations

```mql5
FrameFilter("equity_curve", ULONG_MAX);   // filter by name only
FrameFilter("",             42);           // filter by id only
FrameFilter("",             ULONG_MAX);    // equivalent to FrameFirst() — no filter
```

## ParameterSetRange — Override Optimisation Ranges

```mql5
void OnTesterInit() {
   ParameterSetRange("InpRiskPercent", true,  1.0, 0.5, 0.25, 3.0);
   ParameterSetRange("InpATRPeriod",   true,  14,  10,  1,    30);
   ParameterSetRange("InpMagicNumber", false, 10001, 0,  0,    0);
}
```

- Can only be called from `OnTesterInit()` — not from agents
- `sinput` variables can be included in optimisation via `ParameterSetRange`

## MQL5 Cloud Network Limits

```
Max RAM per agent:   4 GB
Max disk writes:     4 GB total across the pass
If exceeded:         agent fails silently — you are still billed for compute time

Guard pattern for file operations:
  bool do_files = !(MQLInfoInteger(MQL_OPTIMIZATION) || MQLInfoInteger(MQL_FORWARD));
  if(do_files) { handle = FileOpen(...); ... }
```
