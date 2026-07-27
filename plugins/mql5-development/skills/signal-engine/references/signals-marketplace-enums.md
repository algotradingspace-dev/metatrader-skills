# MQL5 Signals Marketplace — Subscription Property Enums

**Note:** These enums describe the MQL5.com Signals marketplace subscription
API — not algorithmic signal generation. Use `SignalBaseGetDouble/Integer/String()`
and `SignalInfoGetDouble/Integer/String()` to read these properties.

## ENUM_SIGNAL_BASE_DOUBLE — Signal Performance Stats

| Identifier | Description |
|------------|-------------|
| `SIGNAL_BASE_BALANCE` | Account balance |
| `SIGNAL_BASE_EQUITY` | Account equity |
| `SIGNAL_BASE_GAIN` | Gain % since monitoring start |
| `SIGNAL_BASE_MAX_DRAWDOWN` | Maximum drawdown % |
| `SIGNAL_BASE_PRICE` | Subscription price (USD) |
| `SIGNAL_BASE_ROI` | Return on Investment % |

## ENUM_SIGNAL_BASE_INTEGER — Signal Metadata

| Identifier | Description |
|------------|-------------|
| `SIGNAL_BASE_DATE_PUBLISHED` | Publication date |
| `SIGNAL_BASE_DATE_STARTED` | Monitoring start date |
| `SIGNAL_BASE_DATE_UPDATED` | Last stats update date |
| `SIGNAL_BASE_ID` | Signal ID |
| `SIGNAL_BASE_LEVERAGE` | Account leverage |
| `SIGNAL_BASE_PIPS` | Total profit in pips |
| `SIGNAL_BASE_RATING` | Position in leaderboard |
| `SIGNAL_BASE_SUBSCRIBERS` | Subscriber count |
| `SIGNAL_BASE_TRADES` | Number of trades |
| `SIGNAL_BASE_TRADE_MODE` | Account type (0=real, 1=demo, 2=contest) |

## ENUM_SIGNAL_BASE_STRING — Signal Identification

`SIGNAL_BASE_AUTHOR_LOGIN` · `SIGNAL_BASE_BROKER` · `SIGNAL_BASE_BROKER_SERVER` · `SIGNAL_BASE_NAME` · `SIGNAL_BASE_CURRENCY`

## ENUM_SIGNAL_INFO_\* — Subscription Copy Settings

| Identifier | Type | Description |
|------------|------|-------------|
| `SIGNAL_INFO_VOLUME_PERCENT` | double | Max deposit % to use for copied trades |
| `SIGNAL_INFO_EQUITY_LIMIT` | double | Minimum equity to allow copying |
| `SIGNAL_INFO_SLIPPAGE` | double | Max allowed slippage |
| `SIGNAL_INFO_CONFIRMATIONS_DISABLED` | int | Skip confirmation dialogs |
| `SIGNAL_INFO_COPY_SLTP` | int | Copy SL/TP from signal |
| `SIGNAL_INFO_DEPOSIT_PERCENT` | int | Deposit percent to use |
| `SIGNAL_INFO_ID` | int | Signal ID (read-only) |
| `SIGNAL_INFO_SUBSCRIPTION_ENABLED` | int | Subscription active flag |
| `SIGNAL_INFO_NAME` | string | Signal name (read-only) |
