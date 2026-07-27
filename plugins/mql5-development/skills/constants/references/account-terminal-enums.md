# Account and Terminal Info Enums

## ENUM_ACCOUNT_INFO_INTEGER — `AccountInfoInteger(id)`

| Identifier | Description | Type |
|------------|-------------|------|
| `ACCOUNT_LOGIN` | Account number | long |
| `ACCOUNT_TRADE_MODE` | Account type | `ENUM_ACCOUNT_TRADE_MODE` |
| `ACCOUNT_LEVERAGE` | Leverage | long |
| `ACCOUNT_LIMIT_ORDERS` | Max pending orders allowed | int |
| `ACCOUNT_MARGIN_SO_MODE` | Margin call/stop-out measure | `ENUM_ACCOUNT_STOPOUT_MODE` |
| `ACCOUNT_TRADE_ALLOWED` | Trading allowed for account | bool |
| `ACCOUNT_TRADE_EXPERT` | Trading allowed for EA | bool |
| `ACCOUNT_MARGIN_MODE` | Margin calculation mode | `ENUM_ACCOUNT_MARGIN_MODE` |
| `ACCOUNT_CURRENCY_DIGITS` | Deposit currency decimal places | int |
| `ACCOUNT_FIFO_CLOSE` | Positions must close FIFO | bool |
| `ACCOUNT_HEDGE_ALLOWED` | Hedging allowed | bool |

## ENUM_ACCOUNT_INFO_DOUBLE — `AccountInfoDouble(id)`

| Identifier | Description |
|------------|-------------|
| `ACCOUNT_BALANCE` | Balance in deposit currency |
| `ACCOUNT_CREDIT` | Credit |
| `ACCOUNT_PROFIT` | Current floating profit |
| `ACCOUNT_EQUITY` | Equity |
| `ACCOUNT_MARGIN` | Margin used |
| `ACCOUNT_MARGIN_FREE` | Free margin |
| `ACCOUNT_MARGIN_LEVEL` | Margin level % |
| `ACCOUNT_MARGIN_SO_CALL` | Margin Call level (% or currency, see SO_MODE) |
| `ACCOUNT_MARGIN_SO_SO` | Stop Out level (% or currency) |
| `ACCOUNT_MARGIN_INITIAL` | Reserved for pending orders |
| `ACCOUNT_MARGIN_MAINTENANCE` | Minimum equity for open positions |
| `ACCOUNT_ASSETS` | Current assets |
| `ACCOUNT_LIABILITIES` | Current liabilities |
| `ACCOUNT_COMMISSION_BLOCKED` | Blocked commissions |

## ENUM_ACCOUNT_INFO_STRING — `AccountInfoString(id)`

`ACCOUNT_NAME` · `ACCOUNT_SERVER` · `ACCOUNT_CURRENCY` · `ACCOUNT_COMPANY`

---

## ENUM_ACCOUNT_TRADE_MODE

| Value | Description |
|-------|-------------|
| `ACCOUNT_TRADE_MODE_DEMO` | Demo account |
| `ACCOUNT_TRADE_MODE_CONTEST` | Contest account |
| `ACCOUNT_TRADE_MODE_REAL` | Real account |

## ENUM_ACCOUNT_STOPOUT_MODE

| Value | Description |
|-------|-------------|
| `ACCOUNT_STOPOUT_MODE_PERCENT` | Stop Out in percent |
| `ACCOUNT_STOPOUT_MODE_MONEY` | Stop Out in deposit currency |

## ENUM_ACCOUNT_MARGIN_MODE

| Value | Description |
|-------|-------------|
| `ACCOUNT_MARGIN_MODE_RETAIL_NETTING` | Netting (one position per symbol) |
| `ACCOUNT_MARGIN_MODE_EXCHANGE` | Exchange mode |
| `ACCOUNT_MARGIN_MODE_RETAIL_HEDGING` | Hedging (multiple positions per symbol) |

---

## ENUM_TERMINAL_INFO_INTEGER — Key Identifiers (via `TerminalInfoInteger(id)`)

| Identifier | Description |
|------------|-------------|
| `TERMINAL_BUILD` | Terminal build number |
| `TERMINAL_CONNECTED` | Connected to trade server |
| `TERMINAL_TRADE_ALLOWED` | Trading enabled in terminal |
| `TERMINAL_DLLS_ALLOWED` | DLL usage allowed |
| `TERMINAL_MAXBARS` | Max bars on chart |
| `TERMINAL_CPU_CORES` | CPU core count |
| `TERMINAL_MEMORY_PHYSICAL` | Physical memory (MB) |
| `TERMINAL_MEMORY_AVAILABLE` | Available process memory (MB) |
| `TERMINAL_PING_LAST` | Last ping to trade server (microseconds) |
| `TERMINAL_VPS` | Running on MetaTrader VPS |
| `TERMINAL_X64` | 64-bit terminal flag |
| `TERMINAL_COMMUNITY_ACCOUNT` | MQL5.community credentials present |
| `TERMINAL_COMMUNITY_CONNECTION` | Connected to MQL5.community |

## ENUM_TERMINAL_INFO_STRING — via `TerminalInfoString(id)`

`TERMINAL_LANGUAGE` · `TERMINAL_COMPANY` · `TERMINAL_NAME` · `TERMINAL_PATH` · `TERMINAL_DATA_PATH` · `TERMINAL_COMMONDATA_PATH`
