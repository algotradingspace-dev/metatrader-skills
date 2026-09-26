# metatrader-platform

Agent skills for MetaTrader 4/5 platform operations, Python API integration,
and journal monitoring.

## Included skills

- **Platform** — terminal setup, SSL, 2FA, multi-account mgmt, runtime ops
- **Python** — MetaTrader5 package, pandas workflows, trade execution
- **Journal Monitor** — broker execution quality, connection drops, fills

## Usage

```bash
claude plugin marketplace add algotradingspace-dev/metatrader-skills   # once
claude plugin install metatrader-platform@metatrader-skills
```

Then reference skills by name in your prompts (e.g. "use metatrader-python").
