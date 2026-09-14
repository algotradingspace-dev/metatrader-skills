# Position and Pending Order Access API

## Position Selection Patterns

```mql5
// By symbol (netting: single position; hedging: lowest ticket)
if(PositionSelect(_Symbol)) { ... }

// By ticket (hedging — iterate all positions)
if(PositionSelectByTicket(ticket)) { ... }

// Iterate all positions
int total = PositionsTotal();
for(int i = total - 1; i >= 0; i--) {
   ulong ticket = PositionGetTicket(i);
   string sym   = PositionGetSymbol(i);
   if(PositionGetInteger(POSITION_MAGIC) != magic) continue;
}
```
> **Warning:** Iterate backwards (`total-1` to `0`) — closing a position removes it from the list and shifts indices.

## ENUM_POSITION_PROPERTY_DOUBLE

| Constant | Meaning |
|----------|---------|
| `POSITION_VOLUME` | current lot size |
| `POSITION_PRICE_OPEN` | entry price |
| `POSITION_PRICE_CURRENT` | current market price |
| `POSITION_SL` | stop loss |
| `POSITION_TP` | take profit |
| `POSITION_SWAP` | accumulated swap |
| `POSITION_PROFIT` | floating P&L in account currency |
| `POSITION_COMMISSION` | commission |

## ENUM_POSITION_PROPERTY_INTEGER

| Constant | Meaning |
|----------|---------|
| `POSITION_TICKET` | unique ticket |
| `POSITION_TIME` | open time (datetime) |
| `POSITION_TIME_UPDATE` | last modification time |
| `POSITION_TYPE` | POSITION_TYPE_BUY / POSITION_TYPE_SELL |
| `POSITION_MAGIC` | EA magic number |
| `POSITION_IDENTIFIER` | unique ID linking to deals |
| `POSITION_REASON` | CLIENT / MOBILE / WEB / EXPERT |

## ENUM_POSITION_PROPERTY_STRING

| Constant | Meaning |
|----------|---------|
| `POSITION_SYMBOL` | symbol name |
| `POSITION_COMMENT` | comment |
| `POSITION_EXTERNAL_ID` | broker-side ID |

---

## Pending Order Iteration

```mql5
int total = OrdersTotal();
for(int i = total - 1; i >= 0; i--) {
   ulong ticket = OrderGetTicket(i);
   if(OrderGetInteger(ORDER_MAGIC) != magic) continue;
   ENUM_ORDER_TYPE type = (ENUM_ORDER_TYPE)OrderGetInteger(ORDER_TYPE);
   double openPrice     = OrderGetDouble(ORDER_PRICE_OPEN);
   string symbol        = OrderGetString(ORDER_SYMBOL);
}

// Select by ticket directly
if(OrderSelect(ticket)) { ... }
```

## ENUM_ORDER_PROPERTY_DOUBLE

| Constant | Meaning |
|----------|---------|
| `ORDER_VOLUME_INITIAL` | original volume |
| `ORDER_VOLUME_CURRENT` | remaining volume |
| `ORDER_PRICE_OPEN` | trigger price |
| `ORDER_SL` | stop loss |
| `ORDER_TP` | take profit |
| `ORDER_PRICE_CURRENT` | current price |
| `ORDER_PRICE_STOPLIMIT` | stop-limit trigger price |

## ENUM_ORDER_PROPERTY_INTEGER

> Canonical MQL5 reference: [ORDER_TICKET](https://www.mql5.com/en/docs/constants/tradingconstants/orderproperties#enum_order_property_integer) · [ORDER_MAGIC](https://www.mql5.com/en/docs/constants/tradingconstants/orderproperties)

| Constant | Meaning |
|----------|---------|
| `ORDER_TICKET` | order ticket |
| `ORDER_TIME_SETUP` | creation time |
| `ORDER_TIME_EXPIRATION` | expiry (0 = GTC) |
| `ORDER_TYPE` | BUY/SELL/BUY_LIMIT/SELL_LIMIT/BUY_STOP/SELL_STOP/BUY_STOP_LIMIT/SELL_STOP_LIMIT |
| `ORDER_STATE` | STARTED/PLACED/PARTIAL/FILLED/CANCELED/EXPIRED/REJECTED |
| `ORDER_MAGIC` | EA magic number |
| `ORDER_REASON` | CLIENT/MOBILE/WEB/EXPERT/SL/TP/SO |
| `ORDER_TYPE_FILLING` | FOK/IOC/RETURN |
| `ORDER_TYPE_TIME` | GTC/DAY/SPECIFIED/SPECIFIED_DAY |
