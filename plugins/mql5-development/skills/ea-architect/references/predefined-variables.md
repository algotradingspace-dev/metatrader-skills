# Predefined Variables

All predefined variables are **read-only constants** set before the program
starts. The one exception: `_LastError` can be reset via `ResetLastError()`.

---

## Reference Table

| Variable | Type | Equivalent function | Notes |
|----------|------|-------------------|-------|
| `_Symbol` | `string` | `Symbol()` | Current chart symbol name |
| `_Period` | `ENUM_TIMEFRAMES` | `Period()` | Current chart timeframe |
| `_Digits` | `int` | `Digits()` | Decimal places for current symbol |
| `_Point` | `double` | `Point()` | Point size in quote currency |
| `_LastError` | `int` | `GetLastError()` | Last error code; reset with `ResetLastError()` |
| `_StopFlag` | `int` | `IsStopped()` | Non-zero when terminal requests program stop |
| `_UninitReason` | `int` | `UninitializeReason()` | Deinit reason (same codes as `OnDeinit` reason param) |
| `_RandomSeed` | `int` | — | Current PRNG state; updated by `MathRand()`; seed with `MathSrand()` |
| `_IsX64` | `int` | `TerminalInfoInteger(TERMINAL_X64)` | 0 = 32-bit terminal, non-zero = 64-bit |
| `_AppliedTo` | `int` | — | Indicator only: data source type |

---

## Key Usage Patterns

```mql5
// Prefer _Symbol over hardcoded name — makes EA chart-portable
double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);

// Use _StopFlag in long loops (scripts/services)
for(int i = 0; i < total && !_StopFlag; i++) { }

// _UninitReason inside OnDeinit — same as reason param but accessible anywhere
void OnDeinit(const int reason) {
   if(_UninitReason == REASON_CHARTCHANGE) ReinitOnNewChart();
}

// _Point is per-symbol; never use hardcoded 0.0001 or 0.00001
double sl = ask - 50 * _Point;
```

---

## `_AppliedTo` Values (Indicator Only)

| Value | Meaning |
|-------|---------|
| 0 | Second `OnCalculate` form (OHLCV arrays) |
| 1–7 | Close, Open, High, Low, Median (HL/2), Typical (HLC/3), Weighted (HLCC/4) |
| 8 | Previous indicator's data |
| 9 | First indicator's data |
| 10+ | Indicator handle (passed via `iCustom`) |

---

## References

- `docs/mql5_com_-_docs/predefined.md`
- `docs/mql5_com_-_docs/predefined-_symbol.md`
- `docs/mql5_com_-_docs/predefined-_period.md`
- `docs/mql5_com_-_docs/predefined-_digits.md`
- `docs/mql5_com_-_docs/predefined-_point.md`
- `docs/mql5_com_-_docs/predefined-_lasterror.md`
- `docs/mql5_com_-_docs/predefined-_stopflag.md`
- `docs/mql5_com_-_docs/predefined-_uninitreason.md`
- `docs/mql5_com_-_docs/predefined-_randomseed.md`
- `docs/mql5_com_-_docs/predefined-_isx64.md`
- `docs/mql5_com_-_docs/predefined-_appliedto.md`
