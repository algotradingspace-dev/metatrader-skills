# Prop Firm Rule Presets

> **Last verified:** 2026-07-27
> **Verify before use:** Prop firm challenge rules change frequently.
> These values may be outdated. Always check the firm's current challenge
> terms before configuring an EA.

Configure `InpMaxDailyDD` and `InpMaxTotalDD` inputs to match your firm.
EA halts 1-2% before the hard limit using `halt_daily_buffer` /
`halt_total_buffer` in the `PropFirmRules` struct.

## Drawdown Limit Presets

| Firm | Daily Limit | Total Limit | EA Halts At |
|------|-------------|-------------|-------------|
| FTMO Standard | 5% | 10% | 4% daily / 8% total |
| MyFundedFX (MFF) | 4% | 8% | 3% daily / 6.5% total |
| E8 Funding | 4% | 8% | 3% daily / 7% total |
| The Funded Trader | 5% | 10% | 4% daily / 8% total |

## Additional Rules

Additional prop firm rules to implement in `IsTradeAllowed()`:
- Close all positions on Friday at 20:00 UTC if "no weekend hold" rule applies
- Skip trading during high-impact news if firm restricts news trading
- Enforce minimum trading days by tracking `distinctTradingDays`
