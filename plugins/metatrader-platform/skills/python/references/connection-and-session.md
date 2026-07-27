# Connection And Session

Self-written reference for the official `MetaTrader5` Python module session lifecycle.

---

## Core Session Calls

The session flow is built around five functions:

- `initialize()`
- `login()`
- `shutdown()`
- `version()`
- `last_error()`

Typical lifecycle:

1. Start or attach to a terminal with `initialize()`
2. Optionally switch accounts with `login()`
3. Inspect terminal and account state
4. Perform data or trading work
5. Close the bridge with `shutdown()`

---

## `initialize()`

Use `initialize()` to connect Python to MT5. Supported patterns include:

- No arguments: auto-discover a terminal
- Executable path: attach to a specific installation
- Path plus account parameters: launch or attach with explicit login context

Important parameters:

- terminal executable path
- account number
- password
- server name
- timeout in milliseconds
- `portable=True` when working against portable terminal layouts

Operational guidance:

- Prefer explicit terminal paths in multi-terminal environments
- Use explicit timeouts for services rather than relying on defaults
- In automation, treat `False` from `initialize()` as a hard failure and inspect `last_error()` immediately

---

## `login()`

Use `login()` after initialization when you need to switch to a specific account in an already running terminal.

Good use cases:

- Shared development workstation with remembered terminal credentials
- Scripts that attach to a terminal first, then select an account deliberately
- Explicit account switching during controlled automation

Do not assume `login()` alone is a full substitute for terminal selection. The terminal process still has to be reachable first.

---

## `shutdown()`

Always call `shutdown()` when the script is finished with MT5. This matters for:

- Long-running worker hygiene
- Avoiding stale IPC state between test runs
- Predictable reconnection behavior in local tooling

In short scripts, wrap the session in `try/finally` so shutdown still happens on failure.

---

## `version()` And `last_error()`

Use `version()` to confirm the connected terminal build and release metadata.

Use `last_error()` immediately after any failed module call. It is the primary diagnostic hook for the Python bridge.

Minimal rule:

- Never ignore a `None` or `False` return without recording `last_error()` nearby

---

## Account And Terminal Inspection

Two functions should be treated as standard post-connect checks:

- `account_info()`
- `terminal_info()`

Use `account_info()` to confirm:

- login
- server
- balance, equity, margin, margin free
- leverage
- `trade_allowed`
- `trade_expert`

Use `terminal_info()` to confirm:

- `connected`
- `trade_allowed`
- build
- terminal path and data path
- `tradeapi_disabled`

These checks should happen before live trading or large data jobs.

---

## Safe Session Pattern

```python
import MetaTrader5 as mt5

if not mt5.initialize(path=terminal_path, login=login, password=password, server=server):
    raise RuntimeError(f"MT5 initialize failed: {mt5.last_error()}")

try:
    account = mt5.account_info()
    terminal = mt5.terminal_info()
    if account is None or terminal is None:
        raise RuntimeError(f"MT5 session inspection failed: {mt5.last_error()}")
finally:
    mt5.shutdown()
```

Keep the pattern boring and explicit. The bridge is stateful enough that clever abstractions tend to hide the real failure point.

---

## CHUNK PY-1 — Function Signatures: Session Calls

```python
# Establish connection to a terminal
mt5.initialize()                                  # auto-discover terminal
mt5.initialize(path)                              # attach by exe path
mt5.initialize(path, login=N, password="...",     # full explicit login
               server="...", timeout=60000,
               portable=False)

# Switch trading account on an already-running terminal
mt5.login(account, password="...", server="...", timeout=60000)
# Returns True on success

# Inspect what is connected
mt5.version()           # → tuple (build_int, build_int, "DD Mon YYYY")
mt5.account_info()      # → AccountInfo named tuple (or None)
mt5.terminal_info()     # → TerminalInfo named tuple (or None)
mt5.last_error()        # → tuple (error_code, description)

# Disconnect
mt5.shutdown()
```

**Key `account_info()` fields:** login, server, currency, balance, equity, margin, margin_free, margin_level, leverage, trade_allowed, trade_expert, fifo_close

**Key `terminal_info()` fields:** connected, trade_allowed, tradeapi_disabled, build, path, data_path, community_account, community_connection

---

## CHUNK PY-2 — `last_error()` Error Codes

| Code | Constant | Description |
|------|----------|-------------|
| 0 | RES_S_OK | Success |
| -2 | RES_E_NO_MEMORY | No memory condition |
| -10000 | RES_E_GENERAL_FAIL | Internal IPC general error |
| -10001 | RES_E_INTERNAL_FAIL | Internal IPC send failed |
| -10002 | RES_E_INTERNAL_FAIL_SEND | Internal IPC send failed |
| -10003 | RES_E_INTERNAL_FAIL_RECV | Internal IPC recv failed |
| -10004 | RES_E_INTERNAL_FAIL_INIT | Internal IPC initialization fail |
| -10005 | RES_E_INTERNAL_FAIL_CONNECT | Internal IPC no ipc |
| -10006 | RES_E_INTERNAL_FAIL_TIMEOUT | IPC timeout |

Always call `last_error()` immediately after a failed call. Error context is cleared by subsequent calls.

**References:**
- `docs/mql5_com_-_docs_python_metatrader5/01_mt5initialize_py.md`
- `docs/mql5_com_-_docs_python_metatrader5/02_mt5login_py.md`
- `docs/mql5_com_-_docs_python_metatrader5/03_mt5shutdown_py.md`
- `docs/mql5_com_-_docs_python_metatrader5/04_mt5version_py.md`
- `docs/mql5_com_-_docs_python_metatrader5/05_mt5lasterror_py.md`
- `docs/mql5_com_-_docs_python_metatrader5/06_mt5accountinfo_py.md`
- `docs/mql5_com_-_docs_python_metatrader5/07_mt5terminalinfo_py.md`