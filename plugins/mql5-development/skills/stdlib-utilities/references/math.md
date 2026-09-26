# Math Functions — Trig, Exponential, Rounding, Classification, Randomness

## Trigonometric, Exponential, and Logarithmic Functions

| Function group | What it covers | Usage note |
|----------------|----------------|------------|
| `MathSin`, `MathCos`, `MathTan`, `MathArcsin`, `MathArccos`, `MathArctan`, `MathArctan2` | Trigonometric functions | Inputs and outputs use radians |
| `MathSinh`, `MathCosh`, `MathTanh` | Hyperbolic functions | These are specialised and should usually sit behind a named helper with domain context |
| `MathExp`, `MathLog`, `MathLog10`, `MathLog1p`, `MathPow`, `MathSqrt` | Exponential and logarithmic operations | Check numeric validity when domain assumptions can fail |

## Rounding, Classification, Randomness, and Utility Math

| Function group | What it covers | Usage note |
|----------------|----------------|------------|
| `MathAbs`, `MathMin`, `MathMax` | Bounds and distance helpers | Common in stop-distance, drawdown, and range calculations |
| `MathFloor`, `MathCeil`, `MathRound` | Rounding control | Be explicit about whether you need truncation, ceiling, or bank-style rounding behaviour |
| `MathClassify`, `MathIsValidNumber` | Floating-point safety checks | Use before comparing or storing values that may become `NaN` or infinity |
| `MathRand`, `MathSrand`, `MathSwap` | Randomness and utility operations | Seed once deliberately; repeated reseeding destroys randomness quality |
