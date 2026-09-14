# CPositionInfo Class Reference

`CPositionInfo` is the read-only wrapper for currently open position state,
selection helpers, and snapshot comparison.

> Canonical MQL5 reference: [TimeMsc](https://www.mql5.com/en/docs/standardlibrary/tradeclasses/cdealinfo/cdealinfotimemsc) · [TimeUpdate](https://www.mql5.com/en/docs/standardlibrary/tradeclasses/cpositioninfo/cpositioninfotimeupdate) · [TimeUpdateMsc](https://www.mql5.com/en/docs/standardlibrary/tradeclasses/cpositioninfo/cpositioninfotimeupdatemsc) · [PositionType](https://www.mql5.com/en/docs/standardlibrary/tradeclasses/cpositioninfo/cpositioninfopositiontype)

| Method | Return Type | Brief purpose | One-line usage note |
|--------|------------|---------------|---------------------|
| `Time` | `datetime` | Get position open time | Use for session-based holding-period rules |
| `TimeMsc` | `ulong` | Get position open time in milliseconds | Useful when you need stable ordering across same-second events |
| `TimeUpdate` | `datetime` | Get last position update time | Use to detect whether the broker changed the position recently |
| `TimeUpdateMsc` | `ulong` | Get last position update time in milliseconds | Prefer this when deduplicating rapid updates |
| `PositionType` | `ENUM_POSITION_TYPE` | Get long or short side | Gate buy vs sell management paths from this value |
| `TypeDescription` | `string` | Get position side as text | Use in logs instead of raw enum values |
| `Magic` | `long` | Get opening EA magic | Filter multi-strategy books before managing a position |
| `Identifier` | `long` | Get persistent position identifier | Use when broker ticket changes are possible |
| `Volume` | `double` | Get open position volume | Re-read before partial-close calculations |
| `PriceOpen` | `double` | Get open price | Base breakeven and RR calculations on this |
| `StopLoss` | `double` | Get current stop loss | Compare before sending a modify request |
| `TakeProfit` | `double` | Get current take profit | Preserve existing TP when only moving SL |
| `PriceCurrent` | `double` | Get current market price for the symbol | Use for unrealised RR or trailing-stop logic |
| `Commission` | `double` | Get position commission | Include this in net PnL analytics if needed |
| `Swap` | `double` | Get accumulated swap | Important for overnight or swing holding cost |
| `Profit` | `double` | Get floating profit | Use only as a convenience view, not a replacement for price math |
| `Symbol` | `string` | Get position symbol | Needed in generic portfolio loops |
| `Comment` | `string` | Get position comment | Handy for strategy tags when magic numbers are shared |
| `InfoInteger` | `bool` | Read arbitrary integer position property | Use for properties not covered by convenience getters |
| `InfoDouble` | `bool` | Read arbitrary double position property | Use to avoid dropping to raw `PositionGetDouble()` |
| `InfoString` | `bool` | Read arbitrary string position property | Useful for generic inspectors |
| `Select` | `bool` | Select current-symbol position | Works best in single-position-per-symbol flows |
| `SelectByIndex` | `bool` | Select position by list index | Iterate positions backwards when mutating the book |
| `SelectByMagic` | `bool` | Select position by symbol and magic | Use to scope management to one EA instance |
| `SelectByTicket` | `bool` | Select position by ticket | Prefer this in hedging accounts with multiple same-symbol positions |
| `StoreState` | `void` | Snapshot current position fields | Call before a broker action if you need before-and-after comparison |
| `CheckState` | `bool` | Compare current state to stored snapshot | Use to detect whether the position changed externally |
