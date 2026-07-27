---
name: python
description: >
  MetaTrader 5 Python package (MetaTrader5 module) integration. Use for:
  connecting Python code to a local MT5 terminal; initialising and shutting down
  sessions; reading account, terminal, symbol, tick, rate, order, position, and
  deal data; calculating margin or profit; validating and sending trade requests;
  building pandas-based MT5 data workflows; converting MT5 responses into
  DataFrame-friendly structures. Trigger: "MetaTrader5", "MT5 Python",
  "python mt5", "initialize MT5", "mt5 login", "mt5 order_send",
  "mt5 copy_rates", "mt5 account info", "pandas mt5", "mt5 symbol select".
---

# MetaTrader Python

Guidance for integrating Python code with a locally installed MetaTrader 5
terminal through the official `MetaTrader5` module.

---

## Purpose

Catalogs the `MetaTrader5` Python module API: session lifecycle, market data
access (ticks, rates, symbols), trade request construction and validation,
order/position/deal history retrieval, and pandas integration patterns.

---

## When to Use

- Connect Python code directly to a local MT5 terminal
- Initialise and shut down MT5 sessions from scripts or services
- Read account, terminal, symbol, tick, candle, order, position, and deal data
- Estimate margin or profit before trading
- Validate and send trade requests with the native Python bridge
- Convert MT5 responses into pandas-friendly structures

**Do NOT use** for:
- REST access through mt5-httpapi -> use `httpapi`
- MQL source code or EA coding -> use `ea-architect` or `stdlib-utilities`
- Platform setup, security, or account management -> use `platform`
- Performance analytics and scorecards -> use `analytics`

---

## Working Model

This module talks to a locally available MT5 terminal process through
MetaQuotes' native bridge. Treat it as a terminal-bound API:

- One Python process can attach to one terminal context at a time
- Terminal state matters for every call
- Symbol visibility, login state, and terminal connection affect data and
  trading behaviour
- Time-sensitive data should be handled in UTC

---

## References

| File | Contents | Read when |
|------|----------|-----------|
| `references/connection-and-session.md` | `initialize()`, `login()`, `shutdown()`, `version()`, `last_error()`, account/terminal inspection, session lifecycle | Setting up a session; troubleshooting connection errors |
| `references/market-data.md` | Symbol discovery/selection, tick/bar/DOM access, UTC handling, pandas conversion | Reading prices, rates, or symbol metadata |
| `references/trading-and-history.md` | `order_calc_margin()`, `order_calc_profit()`, `order_check()`, `order_send()`, orders/positions/history | Sending trades; retrieving order/position/deal history |
| `references/code-recipes.md` | Minimal connection scripts, candle-to-pandas, market-order flow, position/deal lookup | Copy-paste starting points for common tasks |
| `references/helper-patterns.md` | Session wrappers, request builders, DataFrame normalisation, separation of concerns | Building reusable Python modules around MT5 |
