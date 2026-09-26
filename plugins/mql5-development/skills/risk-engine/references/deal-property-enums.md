# Deal Property Enums

## ENUM_DEAL_PROPERTY_INTEGER — `HistoryDealGetInteger()`

> Canonical MQL5 reference: [DEAL_ORDER](https://www.mql5.com/en/docs/constants/tradingconstants/dealproperties#enum_deal_property_integer) · [ENUM_DEAL_TYPE](https://www.mql5.com/en/docs/constants/tradingconstants/dealproperties#enum_deal_type) · [ENUM_DEAL_ENTRY](https://www.mql5.com/en/docs/constants/tradingconstants/dealproperties#enum_deal_entry) · [ENUM_DEAL_REASON](https://www.mql5.com/en/docs/constants/tradingconstants/dealproperties#enum_deal_reason)

| Identifier | Description | Type |
|------------|-------------|------|
| `DEAL_TICKET` | Unique deal ticket | long |
| `DEAL_ORDER` | Order ticket that triggered deal | long |
| `DEAL_TIME` | Deal execution time | datetime |
| `DEAL_TIME_MSC` | Deal time in ms since 1970 | long |
| `DEAL_TYPE` | Deal type | `ENUM_DEAL_TYPE` |
| `DEAL_ENTRY` | Entry/exit/reverse | `ENUM_DEAL_ENTRY` |
| `DEAL_MAGIC` | EA magic number | long |
| `DEAL_REASON` | Origin of deal execution | `ENUM_DEAL_REASON` |
| `DEAL_POSITION_ID` | Position lifetime identifier | long |

## ENUM_DEAL_PROPERTY_DOUBLE — `HistoryDealGetDouble()`

| Identifier | Description |
|------------|-------------|
| `DEAL_VOLUME` | Traded volume |
| `DEAL_PRICE` | Execution price |
| `DEAL_COMMISSION` | Commission |
| `DEAL_SWAP` | Swap on close |
| `DEAL_PROFIT` | Profit/loss |
| `DEAL_FEE` | Exchange fee (charged immediately) |
| `DEAL_SL` | Stop Loss at time of deal |
| `DEAL_TP` | Take Profit at time of deal |

`ENUM_DEAL_PROPERTY_STRING`: `DEAL_SYMBOL` · `DEAL_COMMENT` · `DEAL_EXTERNAL_ID`

---

## ENUM_DEAL_TYPE

| Value | Description |
|-------|-------------|
| `DEAL_TYPE_BUY` | Buy (market entry) |
| `DEAL_TYPE_SELL` | Sell (market entry) |
| `DEAL_TYPE_BALANCE` | Balance operation |
| `DEAL_TYPE_CREDIT` | Credit |
| `DEAL_TYPE_CHARGE` | Additional charge |
| `DEAL_TYPE_CORRECTION` | Correction |
| `DEAL_TYPE_BONUS` | Bonus |
| `DEAL_TYPE_COMMISSION` | Commission |
| `DEAL_TYPE_COMMISSION_DAILY` | Daily commission |
| `DEAL_TYPE_COMMISSION_MONTHLY` | Monthly commission |
| `DEAL_TYPE_COMMISSION_AGENT_DAILY` | Daily agent commission |
| `DEAL_TYPE_COMMISSION_AGENT_MONTHLY` | Monthly agent commission |
| `DEAL_TYPE_INTEREST` | Interest payment |
| `DEAL_TYPE_BUY_CANCELED` | Canceled buy (P&L zeroed, balance adjusted separately) |
| `DEAL_TYPE_SELL_CANCELED` | Canceled sell (P&L zeroed) |
| `DEAL_DIVIDEND` | Dividend |
| `DEAL_DIVIDEND_FRANKED` | Franked (non-taxable) dividend |
| `DEAL_TAX` | Tax charge |

> Filter P&L accounting: use `DEAL_TYPE_BUY` / `DEAL_TYPE_SELL` only. Balance,
> credit, and commission deals inflate `STAT_PROFIT` if not excluded.

## ENUM_DEAL_ENTRY

| Value | Description |
|-------|-------------|
| `DEAL_ENTRY_IN` | Opening / adding to position |
| `DEAL_ENTRY_OUT` | Closing / reducing position |
| `DEAL_ENTRY_INOUT` | Reversal |
| `DEAL_ENTRY_OUT_BY` | Close by opposite position |

## ENUM_DEAL_REASON

`DEAL_REASON_CLIENT` · `DEAL_REASON_MOBILE` · `DEAL_REASON_WEB` ·
`DEAL_REASON_EXPERT` · `DEAL_REASON_SL` · `DEAL_REASON_TP` ·
`DEAL_REASON_SO` · `DEAL_REASON_ROLLOVER` · `DEAL_REASON_VMARGIN` ·
`DEAL_REASON_SPLIT` · `DEAL_REASON_CORPORATE_ACTION`
