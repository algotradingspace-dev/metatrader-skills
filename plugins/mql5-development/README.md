# mql5-development

Agent skills for building MQL5 Expert Advisors. Covers the full development
lifecycle from architecture wiring to trade management.

## Included skills

- **EA Architecture** — 5-layer module wiring, OnTick/OnDeinit, IsNewBar gating
- **Risk Engine** — position sizing, drawdown guards, prop firm compliance
- **Signal Engine** — SMC/ICT, indicators, multi-timeframe confluence
- **Market Regime** — trend/range, volatility, session/news filters
- **Trade Manager** — trailing SL, breakeven, partial close, pyramiding

## Usage

```bash
claude plugin marketplace add algotradingspace-dev/metatrader-skills   # once
claude plugin install mql5-development@metatrader-skills
```

Then reference skills by name in your prompts (e.g. "use mql5-risk-engine").
