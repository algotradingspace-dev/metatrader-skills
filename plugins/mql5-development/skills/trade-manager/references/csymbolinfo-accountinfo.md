# CSymbolInfo and CAccountInfo Class Reference

## CSymbolInfo — Instrument Metadata

`CSymbolInfo` is the broad market and instrument metadata wrapper used for
quote refresh, quantisation, trade rules, margin rules, sessions, and
instrument descriptors.

> Canonical MQL5 reference: [RefreshRates](https://www.mql5.com/en/docs/standardlibrary/tradeclasses/csymbolinfo/csymbolinforefreshrates) · [IsSynchronized](https://www.mql5.com/en/docs/standardlibrary/tradeclasses/csymbolinfo/csymbolinfoissynchronized) · [VolumeHigh](https://www.mql5.com/en/docs/standardlibrary/tradeclasses/csymbolinfo/csymbolinfovolumehigh) · [VolumeLow](https://www.mql5.com/en/docs/standardlibrary/tradeclasses/csymbolinfo/csymbolinfovolumelow)

| Method | Return Type | Brief purpose | One-line usage note |
|--------|------------|---------------|---------------------|
| `Refresh` | `void` | Refresh symbol property cache | Call before reading stale-sensitive metadata in long-lived objects |
| `RefreshRates` | `bool` | Refresh quotes | Use before bid/ask-dependent execution logic |
| `Name` | `string` | Get or set symbol name | Initialise once per object before repeated property reads |
| `Select` | `bool` | Ensure symbol is selected in Market Watch | Use before relying on synchronisation-sensitive fields |
| `IsSynchronized` | `bool` | Check terminal/server sync state | Gate trading logic when symbols may be newly loaded |
| `Volume` | `long` | Get last deal volume | Use for quick market-activity snapshots |
| `VolumeHigh` | `long` | Get session high volume | Useful for intraday participation context |
| `VolumeLow` | `long` | Get session low volume | Useful for thinning-liquidity detection |
| `Time` | `datetime` | Get last quote time | Detect stale symbols before placing trades |
| `Spread` | `int` | Get spread in points | Use for spread filters and breakeven padding |
| `SpreadFloat` | `bool` | Check whether spread is floating | Dynamic-spread instruments need wider guardrails |
| `TicksBookDepth` | `int` | Get DOM depth setting | Relevant only when order-book data matters |
| `StopsLevel` | `int` | Get minimum stop distance in points | Validate SL/TP placement against this before sending |
| `FreezeLevel` | `int` | Get freeze distance in points | Check this before modifying live orders or positions |
| `Bid` | `double` | Get current bid | Use for sell-side valuation and fills |
| `BidHigh` | `double` | Get session high bid | Useful for intraday range context |
| `BidLow` | `double` | Get session low bid | Useful for intraday range context |
| `Ask` | `double` | Get current ask | Use for buy-side valuation and fills |
| `AskHigh` | `double` | Get session high ask | Useful for intraday range context |
| `AskLow` | `double` | Get session low ask | Useful for intraday range context |
| `Last` | `double` | Get current last price | Useful on exchange-style symbols with trade last |
| `LastHigh` | `double` | Get session high last | Good for exchange session analytics |
| `LastLow` | `double` | Get session low last | Good for exchange session analytics |
| `TradeCalcMode` | `ENUM_SYMBOL_CALC_MODE` | Get contract calculation mode | Use when sizing risk across instrument classes |
| `TradeCalcModeDescription` | `string` | Get calculation mode as text | Prefer in logs and diagnostics |
| `TradeMode` | `ENUM_SYMBOL_TRADE_MODE` | Get trade availability mode | Check before trying to place trades on restricted symbols |
| `TradeModeDescription` | `string` | Get trade mode as text | Useful in user-facing diagnostics |
| `TradeExecution` | `ENUM_SYMBOL_TRADE_EXECUTION` | Get execution mode | Align order logic to exchange, market, or instant execution |
| `TradeExecutionDescription` | `string` | Get execution mode as text | Prefer in reports and setup logs |
| `SwapMode` | `ENUM_SYMBOL_SWAP_MODE` | Get swap calculation mode | Important for swing and overnight strategies |
| `SwapModeDescription` | `string` | Get swap mode as text | Use for readable overnight-cost diagnostics |
| `SwapRollover3days` | `ENUM_DAY_OF_WEEK` | Get triple-swap day | Use when planning holding periods across rollover |
| `SwapRollover3daysDescription` | `string` | Get triple-swap day as text | Prefer in risk dashboards |
| `MarginInitial` | `double` | Get initial margin value | Use in margin-aware risk checks |
| `MarginMaintenance` | `double` | Get maintenance margin value | Use in margin-survival analytics |
| `MarginLong` | `double` | Get long-position margin rate | Use for directional margin modelling |
| `MarginShort` | `double` | Get short-position margin rate | Use for directional margin modelling |
| `MarginLimit` | `double` | Get margin rate for limit orders | Useful when planning pending-order books |
| `MarginStop` | `double` | Get margin rate for stop orders | Use when breakout systems stage many stop orders |
| `MarginStopLimit` | `double` | Get margin rate for stop-limit orders | Relevant only for stop-limit workflows |
| `TradeTimeFlags` | `int` | Get allowed expiration-mode flags | Decode alongside symbol constants when building order policies |
| `TradeFillFlags` | `int` | Get allowed filling-mode flags | Use before forcing broker-incompatible filling modes |
| `Digits` | `int` | Get quote precision | Normalise display and price math from this |
| `Point` | `double` | Get one-point size | Base pip and point conversion on this value |
| `TickValue` | `double` | Get generic tick value | Use as a starting point, then prefer profit/loss-specific variants when available |
| `TickValueProfit` | `double` | Get tick value for profitable position | Useful on asymmetric or converted instruments |
| `TickValueLoss` | `double` | Get tick value for losing position | Use when risk sizing requires worst-case conversion |
| `TickSize` | `double` | Get minimum price increment | Normalise prices and offsets to this |
| `ContractSize` | `double` | Get contract size | Needed for futures and CFD sizing math |
| `LotsMin` | `double` | Get minimum lot size | Clamp calculated volume before sending |
| `LotsMax` | `double` | Get maximum lot size | Reject oversized scaling logic from this ceiling |
| `LotsStep` | `double` | Get lot increment step | Round all volumes to this before sending orders |
| `LotsLimit` | `double` | Get max aggregate allowed volume | Use to prevent broker-side net exposure rejections |
| `SwapLong` | `double` | Get long swap value | Model overnight carry costs for longs |
| `SwapShort` | `double` | Get short swap value | Model overnight carry costs for shorts |
| `CurrencyBase` | `string` | Get base currency | Useful in cross-asset exposure summaries |
| `CurrencyProfit` | `string` | Get profit currency | Needed for PnL conversion context |
| `CurrencyMargin` | `string` | Get margin currency | Needed when account and symbol margin currencies differ |
| `Bank` | `string` | Get quote source or bank | Mostly useful for diagnostics |
| `Description` | `string` | Get symbol description | Use in UI or reporting, not trade logic |
| `Path` | `string` | Get Market Watch tree path | Useful when auto-grouping instruments |
| `SessionDeals` | `long` | Get current-session deal count | Good for exchange session activity filters |
| `SessionBuyOrders` | `long` | Get session buy-order count | Use for order-flow style diagnostics |
| `SessionSellOrders` | `long` | Get session sell-order count | Use for order-flow style diagnostics |
| `SessionTurnover` | `double` | Get session turnover | Useful for liquidity and participation checks |
| `SessionInterest` | `double` | Get current open-interest summary | Relevant on exchange-traded symbols |
| `SessionBuyOrdersVolume` | `double` | Get buy-order volume in session | Use for order-flow monitoring |
| `SessionSellOrdersVolume` | `double` | Get sell-order volume in session | Use for order-flow monitoring |
| `SessionOpen` | `double` | Get session open price | Base intraday regime logic on this if needed |
| `SessionClose` | `double` | Get session close price | Useful for session recap reporting |
| `SessionAW` | `double` | Get session average weighted price | Relevant on exchange-style instruments |
| `SessionPriceSettlement` | `double` | Get settlement price | Useful for exchange and futures analytics |
| `SessionPriceLimitMin` | `double` | Get session lower price limit | Check against limit-down conditions |
| `SessionPriceLimitMax` | `double` | Get session upper price limit | Check against limit-up conditions |
| `InfoInteger` | `bool` | Read arbitrary integer symbol property | Use for flags not surfaced by convenience getters |
| `InfoDouble` | `bool` | Read arbitrary double symbol property | Use for generic instrument inspectors |
| `InfoString` | `bool` | Read arbitrary string symbol property | Useful in reusable symbol dashboards |
| `NormalizePrice` | `double` | Normalise price to symbol precision and rules | Always normalise pending prices and stop levels before send |

---

## CAccountInfo — Account State

`CAccountInfo` is the account-state wrapper for permissions, balances, margin
health, and pre-trade account-level checks.

> Canonical MQL5 reference: [TradeMode](https://www.mql5.com/en/docs/standardlibrary/tradeclasses/caccountinfo/caccountinfotrademode) · [ENUM_ACCOUNT_TRADE_MODE](https://www.mql5.com/en/docs/constants/environment_state/accountinformation#enum_account_trade_mode) · [TradeModeDescription](https://www.mql5.com/en/docs/standardlibrary/tradeclasses/caccountinfo/caccountinfotrademodedescription) · [StopoutMode](https://www.mql5.com/en/docs/standardlibrary/tradeclasses/caccountinfo/caccountinfostopoutmode)

| Method | Return Type | Brief purpose | One-line usage note |
|--------|------------|---------------|---------------------|
| `Login` | `long` | Get account number | Useful for environment tagging and audit logs |
| `TradeMode` | `ENUM_ACCOUNT_TRADE_MODE` | Get account trade mode | Check this before enabling live execution paths |
| `TradeModeDescription` | `string` | Get trade mode as text | Prefer in setup diagnostics |
| `Leverage` | `long` | Get leverage | Use as context, but still validate actual margin with broker checks |
| `StopoutMode` | `ENUM_ACCOUNT_STOPOUT_MODE` | Get stop-out mode | Needed when interpreting margin call thresholds |
| `StopoutModeDescription` | `string` | Get stop-out mode as text | Better for logs and dashboards |
| `TradeAllowed` | `bool` | Check whether manual trading is allowed | Gate all trade actions if this is false |
| `TradeExpert` | `bool` | Check whether expert trading is allowed | This is the direct wrapper guard for EA permissions |
| `LimitOrders` | `int` | Get max allowed pending orders | Use when managing large pending-order grids |
| `MarginMode` | `ENUM_ACCOUNT_MARGIN_MODE` | Get account margin model | Netting vs retail hedging logic often starts here |
| `MarginModeDescription` | `string` | Get margin mode as text | Use in initialisation logs |
| `Balance` | `double` | Get account balance | Useful for sizing models based on settled capital |
| `Credit` | `double` | Get account credit | Include if the broker uses promotional credit |
| `Profit` | `double` | Get current floating profit | Good for account-level drawdown monitoring |
| `Equity` | `double` | Get current equity | Prefer equity over balance for live risk halts |
| `Margin` | `double` | Get reserved margin | Use with `FreeMargin()` for safety checks |
| `FreeMargin` | `double` | Get available free margin | Reject trades when this gets too compressed |
| `MarginLevel` | `double` | Get current margin level | Useful for hard circuit breakers |
| `MarginCall` | `double` | Get margin-call threshold | Use in broker-specific risk dashboards |
| `MarginStopOut` | `double` | Get stop-out threshold | Keep a safety buffer above this level |
| `Name` | `string` | Get client or account name | Useful in audit logs, not trade logic |
| `Server` | `string` | Get server name | Log this to distinguish demo and live environments |
| `Currency` | `string` | Get deposit currency | Needed for cash-risk reporting |
| `Company` | `string` | Get broker or company name | Useful for environment tagging |
| `InfoInteger` | `long` | Read arbitrary integer account property | Use for account fields not covered by convenience getters |
| `InfoDouble` | `double` | Read arbitrary double account property | Use in generic account dashboards |
| `InfoString` | `string` | Read arbitrary string account property | Useful for reusable tooling |
| `OrderProfitCheck` | `double` | Model profit for a hypothetical order | Use to estimate cash outcome before execution |
| `MarginCheck` | `double` | Model required margin for a hypothetical order | Pair with symbol-level checks before sending |
| `FreeMarginCheck` | `double` | Model remaining free margin after a trade | Reject orders that leave insufficient headroom |
| `MaxLotCheck` | `double` | Estimate maximum feasible lot size | Use as an upper bound, then still round to lot step |
