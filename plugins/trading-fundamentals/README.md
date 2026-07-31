# trading-fundamentals

Agent skill for interpreting forex macroeconomic fundamentals.

## Included skills

- **Forex Fundamentals Reference** — trading-oriented meaning for CPI, GDP,
  NFP, PMI, rate decisions, employment, trade balance, current account,
  housing, wages, and confidence/survey releases across USD, EUR, GBP, GER,
  JPY, CAD, AUD, NZD, CHF, and CNY, with high-value release ranking per
  currency.

## Usage

```bash
claude plugin install ./plugins/trading-fundamentals
```

Then reference the skill by name in your prompts (e.g. "use
forex-fundamentals-reference — what does this week's US CPI print mean for
USD?").
