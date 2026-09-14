# CDealInfo Class Reference

`CDealInfo` is the read-only wrapper for filled deal history.

> Canonical MQL5 reference: [HistorySelect](https://www.mql5.com/en/docs/trading/historyselect) · [TimeMsc](https://www.mql5.com/en/docs/standardlibrary/tradeclasses/cdealinfo/cdealinfotimemsc) · [DealType](https://www.mql5.com/en/docs/standardlibrary/tradeclasses/cdealinfo/cdealinfodealtype) · [ENUM_DEAL_TYPE](https://www.mql5.com/en/docs/constants/tradingconstants/dealproperties#enum_deal_type)

| Method | Return Type | Brief purpose | One-line usage note |
|--------|------------|---------------|---------------------|
| `Ticket` | `ulong` | Get deal ticket or select it | Use after `HistorySelect()` has loaded the target range |
| `Order` | `long` | Get parent order id | Join a deal back to the originating order |
| `Time` | `datetime` | Get execution time | Base deal chronology and session analytics on this |
| `TimeMsc` | `ulong` | Get execution time in milliseconds | Use for exact ordering of fills |
| `DealType` | `ENUM_DEAL_TYPE` | Get deal type | Distinguish buy, sell, balance, charge, and similar deal records |
| `TypeDescription` | `string` | Get deal type as text | Prefer in logs and reports |
| `Entry` | `ENUM_DEAL_ENTRY` | Get entry direction semantics | Use to detect in/out/inout flows on a position |
| `EntryDescription` | `string` | Get entry semantics as text | Makes history audits easier to read |
| `Magic` | `long` | Get EA magic number | Filter deal history by strategy |
| `PositionId` | `long` | Get related position id | Join deals to the same position lifecycle |
| `Volume` | `double` | Get deal volume | Important for scale-in and scale-out analysis |
| `Price` | `double` | Get deal execution price | Base slippage and fill-quality stats on this |
| `Commission` | `double` | Get commission charged to the deal | Include this in net performance analytics |
| `Swap` | `double` | Get swap on close | Useful for overnight cost attribution |
| `Profit` | `double` | Get realised financial result | This is the canonical realised PnL figure per deal |
| `Symbol` | `string` | Get deal symbol | Group deal streams by instrument |
| `Comment` | `string` | Get deal comment | Helpful for strategy tag reconstruction |
| `InfoInteger` | `bool` | Read arbitrary integer deal property | Use for properties not exposed as convenience getters |
| `InfoDouble` | `bool` | Read arbitrary double deal property | Good for generic history tools |
| `InfoString` | `bool` | Read arbitrary string deal property | Use in reporting helpers |
| `SelectByIndex` | `bool` | Select a deal by history index | Use while iterating `HistoryDealsTotal()` |
