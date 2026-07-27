# OpenClaw Live Trading Workflows

Guidance for using MetaTrader-related skills inside OpenClaw when a task
involves live account execution rather than only MQL source code or
platform setup.

---

## When This Reference Applies

Use this reference when the task is any of the following:

- Route a trading action to a specific MT5 account
- Ask OpenClaw to place, modify, or close trades via an external MT5 execution layer
- Combine strategy logic with live execution safeguards
- Structure prompts or tasks so account identity is never ambiguous

If the task is mainly about the REST bridge itself, use the dedicated
`httpapi` skill. If the task is mainly about MQL code, use the relevant
MQL5 development skill. If the task is about platform setup or file
structure, use the platform setup reference.

---

## Recommended Separation of Concerns

Keep these concerns distinct:

- `platform` skill: platform behaviour, file structure, account management, deployment paths
- `python` skill: MetaTrader5 Python module, pandas workflows, session lifecycle
- `httpapi` skill: infrastructure, ports, REST requests, live account state, execution mechanics
- MQL5 development skills: strategy logic, EA architecture, signal generation, risk management
- Python strategy or automation code: signal generation, analytics, orchestration, portfolio logic

This separation prevents one skill file from becoming a mixed reference
for infrastructure, MQL, Python, and live risk handling.

---

## Prompt Pattern

When OpenClaw is asked to trade live, the prompt should include:

1. Account target
2. Symbol
3. Action
4. Risk or sizing rule
5. Whether this is simulation, paper, or live

Good prompt shape:

```text
Use the prop firm challenge account. Check account and symbol state for
XAUUSD, then place a live buy order only if trading is enabled and the
position size for 0.5% risk is valid.
```

Bad prompt shape:

```text
Buy gold now.
```

The system needs explicit routing and risk constraints before it should
touch a live execution surface.

---

## Task Structure

For live execution tasks, prefer a fixed sequence:

1. Resolve account endpoint
2. Check terminal connectivity
3. Check account trading permissions
4. Fetch symbol constraints and current price
5. Compute or validate volume
6. Submit order or modification request
7. Record the result with account identity and ticket data

Do not compress those into a single opaque step when task tracking matters.

---

## Account Routing Rules

Every task should carry explicit account identity. Use at least one of:

- Broker name (generic reference, e.g. "challenge broker", "main broker")
- Account label such as `main`, `demo`, `challenge`
- API port
- Strategy-owned account alias used consistently across prompts and docs

If the prompt omits account routing, the agent should treat that as
incomplete live-trading context rather than guessing.

---

## Metadata Conventions

For OpenClaw tasks or logs, capture:

- `executionMode`: `live`, `paper`, or `simulation`
- `broker`
- `account`
- `port`
- `symbol`
- `action`
- `riskModel`
- `requestedBy` or upstream workflow source

This makes later auditing and replay possible, especially when multiple
MT5 terminals exist on one host.

---

## Safety Defaults

When the prompt does not specify otherwise, live workflows should assume:

- Identity checks before action
- Symbol constraint checks before sizing
- No order placement if trading permissions are off
- No implicit account selection
- No assumption that one broker's settings match another broker's settings

These defaults belong in orchestration logic even if the strategy logic
lives elsewhere.

---

## Python Integration Boundary

If you later add Python-focused developer docs, keep them on the client
side of the boundary:

- Build signals, analytics, and risk calculations in Python
- Use the execution skill to translate validated intent into MT5 REST calls
- Avoid mixing transport details into strategy notebooks or research notes
  unless the task is specifically integration work

This keeps strategy development portable even if the execution layer changes.

---

## Practical Rule

The moment a task can affect a live account, prefer explicit routing,
explicit validation, and explicit logging over convenience. MetaTrader
execution should be treated as an infrastructure boundary, not as an
implied side effect of a trading idea.
