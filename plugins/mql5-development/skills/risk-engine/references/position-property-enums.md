# Position Property Enums

## ENUM_POSITION_PROPERTY_INTEGER — `PositionGetInteger()`

| Identifier | Description | Type |
|------------|-------------|------|
| `POSITION_TICKET` | Unique position ticket | long |
| `POSITION_TIME` | Open time | datetime |
| `POSITION_TIME_MSC` | Open time in ms since 1970 | long |
| `POSITION_TIME_UPDATE` | Last modification time | datetime |
| `POSITION_TIME_UPDATE_MSC` | Last modification time in ms | long |
| `POSITION_TYPE` | Buy or Sell | `ENUM_POSITION_TYPE` |
| `POSITION_MAGIC` | EA magic number | long |
| `POSITION_IDENTIFIER` | Stable lifetime ID (unchanged on netting reversal) | long |
| `POSITION_REASON` | Origin of position open | `ENUM_POSITION_REASON` |

## ENUM_POSITION_PROPERTY_DOUBLE — `PositionGetDouble()`

| Identifier | Description |
|------------|-------------|
| `POSITION_VOLUME` | Lot size |
| `POSITION_PRICE_OPEN` | Open price |
| `POSITION_SL` | Stop Loss |
| `POSITION_TP` | Take Profit |
| `POSITION_PRICE_CURRENT` | Current symbol price |
| `POSITION_SWAP` | Cumulative swap |
| `POSITION_PROFIT` | Current floating P&L |

`ENUM_POSITION_PROPERTY_STRING`: `POSITION_SYMBOL` · `POSITION_COMMENT` · `POSITION_EXTERNAL_ID`

---

## ENUM_POSITION_TYPE

| Value | Description |
|-------|-------------|
| `POSITION_TYPE_BUY` | Long position |
| `POSITION_TYPE_SELL` | Short position |

## ENUM_POSITION_REASON

`POSITION_REASON_CLIENT` · `POSITION_REASON_MOBILE` · `POSITION_REASON_WEB` · `POSITION_REASON_EXPERT`

> Netting note: `POSITION_IDENTIFIER` never changes across reversals;
> `POSITION_TICKET` may change.
> Filter deal history: `HistoryDealGetInteger(ticket, DEAL_POSITION_ID) == POSITION_IDENTIFIER`.
