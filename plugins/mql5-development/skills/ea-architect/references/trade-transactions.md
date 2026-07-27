# Trade Transaction Types — OnTradeTransaction Reference

## ENUM_TRADE_TRANSACTION_TYPE

| Value | Description |
|-------|-------------|
| `TRADE_TRANSACTION_ORDER_ADD` | New open order added |
| `TRADE_TRANSACTION_ORDER_UPDATE` | Open order changed (state transition, modification) |
| `TRADE_TRANSACTION_ORDER_DELETE` | Open order removed (filled or canceled) |
| `TRADE_TRANSACTION_DEAL_ADD` | New deal added to history |
| `TRADE_TRANSACTION_DEAL_UPDATE` | Historical deal changed (rare — exchange adjustment) |
| `TRADE_TRANSACTION_DEAL_DELETE` | Historical deal deleted (rare) |
| `TRADE_TRANSACTION_HISTORY_ADD` | Order moved to history (executed or canceled) |
| `TRADE_TRANSACTION_HISTORY_UPDATE` | Historical order changed |
| `TRADE_TRANSACTION_HISTORY_DELETE` | Historical order deleted |
| `TRADE_TRANSACTION_POSITION` | Position changed server-side (not by deal execution) |
| `TRADE_TRANSACTION_REQUEST` | Server processed trade request — analyse `request` + `result` params |

---

## MqlTradeTransaction Structure

```mql5
struct MqlTradeTransaction {
   ulong                         deal;            // Deal ticket (DEAL_ADD)
   ulong                         order;           // Order ticket
   string                        symbol;          // Symbol
   ENUM_TRADE_TRANSACTION_TYPE   type;            // Transaction type
   ENUM_ORDER_TYPE               order_type;      // Order type
   ENUM_ORDER_STATE              order_state;     // Order state
   ENUM_DEAL_TYPE                deal_type;       // Deal type
   ENUM_ORDER_TYPE_TIME          time_type;       // Order expiration type
   datetime                      time_expiration; // Expiration time
   double                        price;
   double                        price_trigger;   // StopLimit level
   double                        price_sl;
   double                        price_tp;
   double                        volume;
   ulong                         position;        // Position ticket
   ulong                         position_by;     // Opposite position (CLOSE_BY)
};
```

---

## OnTradeTransaction Pattern

```mql5
void OnTradeTransaction(const MqlTradeTransaction &trans,
                        const MqlTradeRequest &request,
                        const MqlTradeResult &result) {
   switch(trans.type) {
      case TRADE_TRANSACTION_DEAL_ADD:
         if(trans.deal_type == DEAL_TYPE_BUY || trans.deal_type == DEAL_TYPE_SELL)
            ProcessNewDeal(trans.deal, trans.symbol, trans.volume, trans.price);
         break;

      case TRADE_TRANSACTION_ORDER_DELETE:
         break;

      case TRADE_TRANSACTION_REQUEST:
         if(result.retcode != TRADE_RETCODE_DONE)
            LogTradeError(result.retcode, result.comment);
         break;
   }
}
```

> For `TRADE_TRANSACTION_REQUEST`, only `trans.type` is valid — analyse `request` and `result` for context.

## References

- `docs/mql5_com_-_docs/constants-tradingconstants-enum_trade_transaction_type.md`
- `docs/mql5_com_-_docs/constants-structures-mqltradetransaction.md`
