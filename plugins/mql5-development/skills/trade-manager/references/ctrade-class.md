# CTrade Class Reference

`CTrade` is the high-level write wrapper for order placement, position
management, and introspection of the last request, check result, and
execution result.

> Canonical MQL5 reference: [LogLevel](https://www.mql5.com/en/docs/standardlibrary/tradeclasses/ctrade/ctradeloglevel) · [SetExpertMagicNumber](https://www.mql5.com/en/docs/standardlibrary/tradeclasses/ctrade/ctradesetexpertmagicnumber) · [OnInit](https://www.mql5.com/en/docs/event_handlers/oninit) · [SetDeviationInPoints](https://www.mql5.com/en/docs/standardlibrary/tradeclasses/ctrade/ctradesetdeviationinpoints)

| Method | Return Type | Brief purpose | One-line usage note |
|--------|------------|---------------|---------------------|
| `LogLevel` | `void` | Set wrapper logging verbosity | Lower noise in production; raise it when diagnosing rejected requests |
| `SetExpertMagicNumber` | `void` | Set EA magic number on outgoing requests | Call once in `OnInit()` before any trade operations |
| `SetDeviationInPoints` | `void` | Set allowed slippage/deviation | Use symbol-appropriate deviation instead of hard-coded broker assumptions |
| `SetTypeFilling` | `void` | Force order filling policy | Use only when you know the broker accepts that filling mode |
| `SetTypeFillingBySymbol` | `bool` | Pick filling mode from symbol settings | Prefer this when trading multiple brokers or instruments |
| `SetAsyncMode` | `void` | Toggle asynchronous trade sending | Keep sync mode unless you already handle delayed result tracking |
| `SetMarginMode` | `void` | Align margin behaviour to account settings | Call during setup when you rely on margin-sensitive checks |
| `OrderOpen` | `bool` | Place a pending order with full parameter control | Use when `BuyLimit`/`SellStop` shortcuts are too narrow |
| `OrderModify` | `bool` | Modify a pending order | Reprice pending orders only after revalidating stop distance rules |
| `OrderDelete` | `bool` | Delete a pending order | Use for stale setups or session cutoffs |
| `PositionOpen` | `bool` | Open a position with explicit order type | Use for generic wrappers where buy/sell side is dynamic |
| `PositionModify` | `bool` | Change SL/TP on an open position | Re-read current SL/TP first to avoid redundant modify calls |
| `PositionClose` | `bool` | Close a position by symbol or ticket | Prefer ticket-based closes in hedging mode |
| `PositionClosePartial` | `bool` | Partially close an open position | Round the volume to broker lot step before calling it |
| `PositionCloseBy` | `bool` | Close one position with an opposite one | Only valid when opposite tickets actually exist |
| `Buy` | `bool` | Open a long position | Pass explicit SL/TP when the strategy requires hard risk controls |
| `Sell` | `bool` | Open a short position | Treat `price=0` as market execution, not a pending order |
| `BuyLimit` | `bool` | Place a buy limit order | Use for pullback entries below market |
| `BuyStop` | `bool` | Place a buy stop order | Use for breakout entries above market |
| `SellLimit` | `bool` | Place a sell limit order | Use for pullback shorts above market |
| `SellStop` | `bool` | Place a sell stop order | Use for downside breakout entries |
| `Request` | `void` | Copy last `MqlTradeRequest` structure | Pull the full request when debugging wrapper behaviour |
| `RequestAction` | `ENUM_TRADE_REQUEST_ACTIONS` | Read last request action | Use it to audit wrapper intent after helper calls |
| `RequestActionDescription` | `string` | Read last request action as text | Prefer this in journal output |
| `RequestMagic` | `ulong` | Read last request magic number | Verify the wrapper is tagging requests correctly |
| `RequestOrder` | `ulong` | Read last request order ticket | Use after pending-order operations |
| `RequestSymbol` | `string` | Read last request symbol | Handy in generic multi-symbol managers |
| `RequestVolume` | `double` | Read last request volume | Log this after normalised lot sizing |
| `RequestPrice` | `double` | Read last request price | Confirm the wrapper sent the expected trigger or market price |
| `RequestStopLimit` | `double` | Read last request stop-limit price | Relevant only for stop-limit flows |
| `RequestSL` | `double` | Read last request stop loss | Validate risk wiring before blaming broker retcodes |
| `RequestTP` | `double` | Read last request take profit | Pair with `RequestSL()` in post-send diagnostics |
| `RequestDeviation` | `ulong` | Read last request deviation | Check this when fills fail in volatile markets |
| `RequestType` | `ENUM_ORDER_TYPE` | Read last request order type | Use to audit generic order factories |
| `RequestTypeDescription` | `string` | Read last request order type as text | Prefer for human-readable logs |
| `RequestTypeFilling` | `ENUM_ORDER_TYPE_FILLING` | Read last request filling mode | Check this when broker rejects execution mode |
| `RequestTypeFillingDescription` | `string` | Read last request filling mode as text | Use in rejection diagnostics |
| `RequestTypeTime` | `ENUM_ORDER_TYPE_TIME` | Read last request expiration mode | Relevant for pending orders with lifetime rules |
| `RequestTypeTimeDescription` | `string` | Read last request expiration mode as text | Helps explain lifetime behaviour |
| `RequestExpiration` | `datetime` | Read last request expiration time | Verify time-zone assumptions for expiring orders |
| `RequestComment` | `string` | Read last request comment | Keep comments short enough for broker limits |
| `RequestPosition` | `ulong` | Read last request position ticket | Relevant for modify or close flows |
| `RequestPositionBy` | `ulong` | Read opposite ticket for close-by | Only meaningful for `PositionCloseBy()` |
| `CheckResult` | `void` | Copy last `MqlTradeCheckResult` structure | Use this after pre-check style calls |
| `CheckResultRetcode` | `uint` | Read validation retcode | Inspect before assuming a margin or stops failure |
| `CheckResultRetcodeDescription` | `string` | Read validation retcode as text | Prefer textual diagnostics in journals |
| `CheckResultBalance` | `double` | Read post-check balance snapshot | Useful in account simulation logs |
| `CheckResultEquity` | `double` | Read post-check equity snapshot | Compare against risk guardrails |
| `CheckResultProfit` | `double` | Read projected floating profit | Use when comparing modelled outcomes |
| `CheckResultMargin` | `double` | Read required margin from check result | Pair with account free margin before sending |
| `CheckResultMarginFree` | `double` | Read projected free margin | Reject trades that compress margin too far |
| `CheckResultMarginLevel` | `double` | Read projected margin level | Useful for leverage-aware risk policies |
| `CheckResultComment` | `string` | Read validation comment | Log this when request checking fails |
| `Result` | `void` | Copy last `MqlTradeResult` structure | Pull the full result after any send or modify call |
| `ResultRetcode` | `uint` | Read execution retcode | This is the first field to inspect on failure |
| `ResultRetcodeDescription` | `string` | Read execution retcode as text | Prefer this in user-facing diagnostics |
| `ResultDeal` | `ulong` | Read resulting deal ticket | Use for post-fill deal tracing |
| `ResultOrder` | `ulong` | Read resulting order ticket | Track pending-order lifecycle with this value |
| `ResultVolume` | `double` | Read executed volume | Important for partial fills |
| `ResultPrice` | `double` | Read confirmed execution price | Use for slippage analytics and journal output |
| `ResultBid` | `double` | Read broker bid at execution | Helps explain requotes and price drift |
| `ResultAsk` | `double` | Read broker ask at execution | Pair with `ResultBid()` for spread-aware diagnostics |
| `ResultComment` | `string` | Read broker comment | Often carries the most actionable failure text |
| `PrintRequest` | `void` | Print last request to journal | Fastest way to dump wrapper state while debugging |
| `PrintResult` | `void` | Print last result to journal | Use after failed sends before adding custom logging |
| `FormatRequest` | `string` | Format a request into text | Good for structured logging without manual field assembly |
| `FormatRequestResult` | `string` | Format request plus result into text | Use when you want one-line audit output per trade action |
