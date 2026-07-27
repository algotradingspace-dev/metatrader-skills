# History Access Patterns

> Required for performance analysis, duplicate-open prevention, and reporting.

## Select History Window

```mql5
// Full history since epoch
HistorySelect(0, TimeCurrent());

// Last N days (preferred — faster)
HistorySelect(TimeCurrent() - N * 86400, TimeCurrent());

// By position ticket (all deals for one position)
HistorySelectByPosition(positionID);
```

> **Critical:** `HistorySelect` resets the history list. Any call to `HistoryOrderSelect()` or `HistoryDealSelect()` also resets it. Re-call `HistorySelect` after those.

## Iterate Deals

```mql5
HistorySelect(from, to);
int total = HistoryDealsTotal();
for(int i = 0; i < total; i++) {
   ulong ticket = HistoryDealGetTicket(i);
   if(HistoryDealGetInteger(ticket, DEAL_MAGIC) != magic) continue;
   long   entry  = HistoryDealGetInteger(ticket, DEAL_ENTRY);
   double profit = HistoryDealGetDouble(ticket, DEAL_PROFIT);
   double volume = HistoryDealGetDouble(ticket, DEAL_VOLUME);
   string symbol = HistoryDealGetString(ticket, DEAL_SYMBOL);
}
```

## ENUM_DEAL_ENTRY Values

| Constant | Meaning |
|----------|---------|
| `DEAL_ENTRY_IN` | position opened |
| `DEAL_ENTRY_OUT` | position closed |
| `DEAL_ENTRY_INOUT` | reversal (netting) |
| `DEAL_ENTRY_OUT_BY` | close by counter-position |

## Key ENUM_DEAL_PROPERTY Constants

| Property | Type | Constant |
|----------|------|----------|
| Ticket | integer | `DEAL_TICKET` |
| Order ticket | integer | `DEAL_ORDER` |
| Time | integer | `DEAL_TIME` |
| Position ID | integer | `DEAL_POSITION_ID` |
| Type (buy/sell) | integer | `DEAL_TYPE` |
| Entry direction | integer | `DEAL_ENTRY` |
| Magic | integer | `DEAL_MAGIC` |
| Volume | double | `DEAL_VOLUME` |
| Price | double | `DEAL_PRICE` |
| Commission | double | `DEAL_COMMISSION` |
| Swap | double | `DEAL_SWAP` |
| Profit | double | `DEAL_PROFIT` |
| Symbol | string | `DEAL_SYMBOL` |
| Comment | string | `DEAL_COMMENT` |

## Iterate History Orders

```mql5
int total = HistoryOrdersTotal();
for(int i = 0; i < total; i++) {
   ulong ticket = HistoryOrderGetTicket(i);
   ENUM_ORDER_STATE state = (ENUM_ORDER_STATE)HistoryOrderGetInteger(ticket, ORDER_STATE);
}
```
