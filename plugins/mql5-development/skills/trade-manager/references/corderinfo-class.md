# COrderInfo and CHistoryOrderInfo Class Reference

## COrderInfo — Active Pending Orders

`COrderInfo` is the read-only wrapper for active pending orders.

> Canonical MQL5 reference: [TimeSetup](https://www.mql5.com/en/docs/standardlibrary/tradeclasses/chistoryorderinfo/chistoryorderinfotimesetup) · [TimeSetupMsc](https://www.mql5.com/en/docs/standardlibrary/tradeclasses/chistoryorderinfo/chistoryorderinfotimesetupmsc) · [OrderType](https://www.mql5.com/en/docs/standardlibrary/tradeclasses/chistoryorderinfo/chistoryorderinfoordertype) · [ENUM_ORDER_TYPE](https://www.mql5.com/en/docs/constants/tradingconstants/orderproperties#enum_order_type)

| Method | Return Type | Brief purpose | One-line usage note |
|--------|------------|---------------|---------------------|
| `Ticket` | `ulong` | Get active order ticket | Select an order first, then read its ticket for downstream actions |
| `TimeSetup` | `datetime` | Get order placement time | Use for stale pending-order expiry logic |
| `TimeSetupMsc` | `ulong` | Get order placement time in milliseconds | Helpful when ordering multiple same-second placements |
| `OrderType` | `ENUM_ORDER_TYPE` | Get pending order type | Distinguish stop, limit, and stop-limit behaviours |
| `TypeDescription` | `string` | Get order type as text | Prefer in logs and UI strings |
| `State` | `ENUM_ORDER_STATE` | Get current order state | Read before assuming the order is still working |
| `StateDescription` | `string` | Get state as text | Use in diagnostics when pending orders disappear or freeze |
| `TimeExpiration` | `datetime` | Get expiration time | Validate time-based order policies against this field |
| `TimeDone` | `datetime` | Get execution or cancellation time | Useful in order lifecycle reporting |
| `TimeDoneMsc` | `ulong` | Get execution or cancellation time in milliseconds | Use for precise history stitching |
| `TypeFilling` | `ENUM_ORDER_TYPE_FILLING` | Get fill policy | Check this when broker behaviour differs by symbol |
| `TypeFillingDescription` | `string` | Get fill policy as text | Emit this in journals instead of raw enum names |
| `TypeTime` | `ENUM_ORDER_TYPE_TIME` | Get expiration mode | Important for GTC vs specified-time logic |
| `TypeTimeDescription` | `string` | Get expiration mode as text | Helps explain order lifetime behaviour |
| `Magic` | `long` | Get EA magic number | Filter orders before modifying or deleting them |
| `PositionId` | `long` | Get linked position id | Relevant when a pending order is tied to a position lifecycle |
| `VolumeInitial` | `double` | Get initial order volume | Use this for original intent, not remaining volume |
| `VolumeCurrent` | `double` | Get remaining unfilled volume | Important for partial-fill-aware logic |
| `PriceOpen` | `double` | Get order trigger price | Reconfirm this before repricing |
| `StopLoss` | `double` | Get linked stop loss | Preserve it during partial order edits |
| `TakeProfit` | `double` | Get linked take profit | Preserve it during partial order edits |
| `PriceCurrent` | `double` | Get current market price | Compare with trigger distance before modifying |
| `PriceStopLimit` | `double` | Get stop-limit secondary price | Only meaningful for stop-limit orders |
| `Symbol` | `string` | Get order symbol | Needed in multi-symbol pending-order books |
| `Comment` | `string` | Get order comment | Useful for strategy tagging and audits |
| `InfoInteger` | `bool` | Read arbitrary integer order property | Use for edge properties not surfaced as getters |
| `InfoDouble` | `bool` | Read arbitrary double order property | Handy for generic order inspectors |
| `InfoString` | `bool` | Read arbitrary string order property | Use when building generic dashboards |
| `StoreState` | `void` | Snapshot order state | Call before `OrderModify()` if you need delta checks |
| `CheckState` | `bool` | Compare current order to stored snapshot | Detect broker-side or external changes cleanly |
| `Select` | `bool` | Select active order by ticket | Use this before reading properties of a known order |
| `SelectByIndex` | `bool` | Select active order by pool index | Use in pending-order loops over `OrdersTotal()` |

---

## CHistoryOrderInfo — Historical Orders

`CHistoryOrderInfo` is the history counterpart to `COrderInfo` for completed,
expired, or cancelled orders.

> Canonical MQL5 reference: [HistorySelect](https://www.mql5.com/en/docs/trading/historyselect) · [TimeSetup](https://www.mql5.com/en/docs/standardlibrary/tradeclasses/chistoryorderinfo/chistoryorderinfotimesetup) · [TimeSetupMsc](https://www.mql5.com/en/docs/standardlibrary/tradeclasses/chistoryorderinfo/chistoryorderinfotimesetupmsc) · [OrderType](https://www.mql5.com/en/docs/standardlibrary/tradeclasses/chistoryorderinfo/chistoryorderinfoordertype)

| Method | Return Type | Brief purpose | One-line usage note |
|--------|------------|---------------|---------------------|
| `Ticket` | `ulong` | Get history order ticket or select it | Use after `HistorySelect()` has loaded the range you need |
| `TimeSetup` | `datetime` | Get order placement time | Useful for latency and order-age analytics |
| `TimeSetupMsc` | `ulong` | Get placement time in milliseconds | Use for precise sequencing in history analysis |
| `OrderType` | `ENUM_ORDER_TYPE` | Get historical order type | Distinguish what kind of pending order was used |
| `TypeDescription` | `string` | Get historical order type as text | Prefer for reports and audit trails |
| `State` | `ENUM_ORDER_STATE` | Get terminal order state | Read to distinguish filled vs cancelled vs expired |
| `StateDescription` | `string` | Get state as text | Use in human-readable reports |
| `TimeExpiration` | `datetime` | Get expiration time | Helps explain why an order disappeared |
| `TimeDone` | `datetime` | Get completion or cancellation time | Pair with setup time to measure order lifetime |
| `TimeDoneMsc` | `ulong` | Get completion or cancellation time in milliseconds | Use for exact event reconstruction |
| `TypeFilling` | `ENUM_ORDER_TYPE_FILLING` | Get fill policy used | Useful when reconciling broker behaviour historically |
| `TypeFillingDescription` | `string` | Get fill policy as text | Better than raw enums in reports |
| `TypeTime` | `ENUM_ORDER_TYPE_TIME` | Get expiration mode used | Audit whether GTC or timed expiry was applied |
| `TypeTimeDescription` | `string` | Get expiration mode as text | Use in post-trade summaries |
| `Magic` | `long` | Get EA magic number | Filter historical orders by strategy instance |
| `PositionId` | `long` | Get linked position id | Join history orders back to positions and deals |
| `VolumeInitial` | `double` | Get originally requested volume | Compare against final fills or remaining size |
| `VolumeCurrent` | `double` | Get remaining volume at completion | Useful when analysing partial fills and cancellations |
| `PriceOpen` | `double` | Get requested order price | Compare with execution or market context later |
| `StopLoss` | `double` | Get historical stop loss | Recover original risk envelope from history |
| `TakeProfit` | `double` | Get historical take profit | Recover original reward target from history |
| `PriceCurrent` | `double` | Get recorded current-price field | Use only as stored history metadata, not live pricing |
| `PriceStopLimit` | `double` | Get stop-limit secondary price | Relevant only for stop-limit history |
| `Symbol` | `string` | Get order symbol | Use for grouping historical orders by instrument |
| `Comment` | `string` | Get order comment | Useful for reconstructing strategy reason tags |
| `InfoInteger` | `bool` | Read arbitrary integer history property | Use for properties not covered by convenience getters |
| `InfoDouble` | `bool` | Read arbitrary double history property | Handy for generic back-office inspectors |
| `InfoString` | `bool` | Read arbitrary string history property | Use in generalised reporting helpers |
| `SelectByIndex` | `bool` | Select a history order by history index | Use after `HistoryOrdersTotal()` iteration |
