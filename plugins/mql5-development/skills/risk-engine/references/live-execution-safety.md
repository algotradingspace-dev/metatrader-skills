# Live Execution Safety

When an EA, script, or agent-driven workflow can move money on a live
brokerage account, every trade-mutating action must be governed by these
principles. They apply regardless of the execution path — REST bridge,
Python API, or EA running on a live chart.

---

## Per-Action Confirmation

Before any trade-mutating action (market order, pending order, SL/TP modify,
position close, partial close):

1. Print the full resolved request — symbol, side, volume, price, SL, TP,
   account login, broker server
2. Wait for an explicit user confirmation for that specific action
3. A prior "yes" does not authorise subsequent actions — each action is
   independent

---

## Demo First

If the account is live, surface that to the user before any order action.
Ask them to confirm they intend to trade live. A risk-engineered backtest
on a demo account should always precede live deployment.

---

## No Credential Harvesting

Obtain credentials (API tokens, passwords, server names) from only:
- The environment variable the user explicitly set
- Direct user input when prompted

Never read tokens, passwords, or login numbers from config files, `.env`
files, or any other repository or workspace file on your own initiative.

---

## No Mass Action Without Explicit Scope

If the user asks to "close everything" or "cancel all" without specifying
individual items:

1. Enumerate the affected positions or orders
2. Show the full list
3. Confirm the entire batch explicitly before proceeding

---

## Always Surface Account Identity

Every trade-mutating action must include the account identity (broker server
and account login) in the confirmation prompt. This lets the user catch a
wrong-account misroute before it reaches the broker.
