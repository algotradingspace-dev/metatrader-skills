# CExpert — Event Orchestration, Trade Lifecycle, and Delegated Trailing

**Source families:** `standardlibrary-expertclasses-expertbaseclasses-cexpert*.md`, `standardlibrary-expertclasses-expertbaseclasses-cexperttrailing*.md`

`CExpert` is the orchestration shell for a standard-library EA. It wires
signal, money, trade, and trailing modules together, exposes all terminal-event
entry points, and owns the high-level processing loop. Trailing rules are
delegated to `CExpertTrailing`; those delegated methods are labelled below.

| Method | Return type | Purpose | Usage note |
|--------|------------|---------|------------|
| `Init` | `bool` | Initialises the expert instance | Override in the derived expert and return `false` to abort `OnInit()` |
| `InitSignal` | `bool` | Initialises the trading signal object | Wire the signal module here before the main loop is allowed to run |
| `InitTrailing` | `bool` | Initialises the trailing stop object | Create and attach the delegated trailing module during setup |
| `InitMoney` | `bool` | Initialises the money management object | Attach the sizing policy before any order-volume calculation occurs |
| `InitTrade` | `bool` | Initialises the trade object | Prepare the trade executor before opening, closing, or modifying anything |
| `ValidationSettings` | `bool` | Checks the settings | Centralise parameter validation so invalid expert state fails fast |
| `InitIndicators` | `bool` | Initialises necessary indicators and timeseries | Call after modules are attached so handles and series stay consistent |
| `InitParameters` | `bool` | Initialises parameters of Expert Advisor | Use for one-time normalisation of inputs before live processing begins |
| `Deinit` | `void` | Deinitialises the expert instance | Mirror initialisation work during `OnDeinit()` |
| `DeinitSignal` | `void` | Deinitialises trade signal object | Release signal resources in the reverse order of setup |
| `DeinitTrailing` | `void` | Deinitialises trailing object | Tear down the delegated trailing module before exit |
| `DeinitMoney` | `void` | Deinitialises money management object | Release sizing-state resources during expert shutdown |
| `DeinitTrade` | `void` | Deinitialises trade object | Use when trade helpers own resources that need explicit cleanup |
| `DeinitIndicators` | `void` | Deinitialises indicators and timeseries | Release indicator handles and cached series on shutdown |
| `Magic` | `void` | Sets the Expert Advisor ID (magic) | Set this before reusing any dependent signal, money, or trailing helper |
| `MaxOrders` (get) | `int` | Gets the maximum amount of allowed orders | Read it inside pre-trade guards before adding exposure |
| `MaxOrders` (set) | `void` | Sets the maximum amount of allowed orders | Configure it during startup to cap simultaneous orders |
| `OnTickProcess` | `void` | Sets the OnTick event handling flag | Enable only if this expert should process `OnTick()` |
| `OnTradeProcess` | `void` | Sets the OnTrade event handling flag | Turn this on when post-trade reconciliation is required |
| `OnTimerProcess` | `void` | Sets the OnTimer event handling flag | Enable only if the strategy uses timer-driven work |
| `OnChartEventProcess` | `void` | Sets a flag to handle the OnChartEvent event | Use when the expert listens to chart UI or custom events |
| `OnBookEventProcess` | `void` | Sets a flag to handle the OnBookEvent event | Enable only for strategies that react to depth-of-market updates |
| `OnTick` | `void` | OnTick event handler | Forward the terminal `OnTick()` event directly here |
| `OnTrade` | `void` | OnTrade event handler | Forward `OnTrade()` so trade-state hooks can run |
| `OnTimer` | `void` | OnTimer event handler | Forward `OnTimer()` when timer processing is enabled |
| `OnChartEvent` | `void` | OnChartEvent event handler | Forward chart events here for manual-control or debug overlays |
| `OnBookEvent` | `void` | OnBookEvent event handler | Forward book events here only if DOM logic is enabled |
| `Refresh` | `bool` | Updates all necessary data | Call before `Processing()` when prices, orders, or history may have changed |
| `Processing` | `bool` | Main processing algorithm | Use this as the expert's main orchestration loop per allowed cycle |
| `CheckOpen` | `bool` | Checks conditions to open a position | Override to gate entry flow before any direction-specific open logic |
| `CheckOpenLong` | `bool` | Checks necessity and conditions to open long position | Override with long-entry rules for the derived strategy |
| `CheckOpenShort` | `bool` | Checks necessity and conditions to open a short position | Override with short-entry rules for the derived strategy |
| `OpenLong` | `bool` | Opens a long position | Call only after the corresponding check passes or let `Processing()` call it |
| `OpenShort` | `bool` | Opens a short position | Use as the execution step after short-entry conditions are satisfied |
| `CheckClose` | `bool` | Checks conditions to close position | Override to gate generic exit flow before direction-specific exits |
| `CheckCloseLong` | `bool` | Checks conditions to close a long position | Override with long-exit logic that runs before `CloseLong()` |
| `CheckCloseShort` | `bool` | Checks conditions to close a short position | Override with short-exit logic that runs before `CloseShort()` |
| `CloseAll` | `bool` | Performs partial or full position closing | Use for emergency flattening or synchronised cleanup |
| `Close` | `bool` | Closes the opened position | Use for the currently selected working position |
| `CloseLong` | `bool` | Closes the long position | Call after long-close checks pass |
| `CloseShort` | `bool` | Closes the short position | Call after short-close checks pass |
| `CheckReverse` | `bool` | Checks necessity and conditions to reverse an open position | Override when the strategy can flip directly instead of exiting flat first |
| `CheckReverseLong` | `bool` | Checks necessity and conditions to reverse a long position | Override with long-to-short reversal criteria |
| `CheckReverseShort` | `bool` | Checks necessity and conditions to reverse a short position | Override with short-to-long reversal criteria |
| `ReverseLong` | `bool` | Performs reverse operation of a long position | Use only after reversal logic decides the long should flip |
| `ReverseShort` | `bool` | Performs reverse operation of a short position | Use only after reversal logic decides the short should flip |
| `CheckTrailingStop` | `bool` | Checks Trailing Stop conditions of the opened position | Use as the generic trailing gate before direction-specific trailing |
| `CheckTrailingStopLong` | `bool` | Checks Trailing Stop conditions of the opened long position | Delegate long-position trailing eligibility to the trailing subsystem |
| `CheckTrailingStopShort` | `bool` | Checks Trailing Stop conditions of the opened short position | Delegate short-position trailing eligibility to the trailing subsystem |
| `TrailingStopLong` | `bool` | Modifies parameters of the opened long position | Apply the long trailing result after the corresponding check passes |
| `TrailingStopShort` | `bool` | Modifies parameters of the opened short position | Apply the short trailing result after the corresponding check passes |
| `CheckTrailingOrderLong` | `bool` | Checks trailing conditions of Buy Limit/Stop orders | Use before modifying pending buy orders |
| `CheckTrailingOrderShort` | `bool` | Checks trailing conditions of Sell Limit/Stop orders | Use before modifying pending sell orders |
| `TrailingOrderLong` | `bool` | Modifies parameters of Buy Limit/Stop trailing order | Call after buy-order trailing conditions are satisfied |
| `TrailingOrderShort` | `bool` | Modifies parameters of Sell Limit/Stop trailing order | Call after sell-order trailing conditions are satisfied |
| `CheckDeleteOrderLong` | `bool` | Checks conditions to delete Buy Limit/Stop order | Override when stale buy orders should be removed automatically |
| `CheckDeleteOrderShort` | `bool` | Checks conditions to delete Sell Limit/Stop order | Override when stale sell orders should be removed automatically |
| `DeleteOrders` | `bool` | Deletes all orders | Use for reset, shutdown, or emergency cleanup flows |
| `DeleteOrder` | `bool` | Deletes the Limit/Stop order | Use for the currently selected pending order |
| `DeleteOrderLong` | `bool` | Deletes the Buy Limit/Stop order | Call after buy-order delete criteria are met |
| `DeleteOrderShort` | `bool` | Deletes the Sell Limit/Stop order | Call after sell-order delete criteria are met |
| `LotOpenLong` | `double` | Gets trade volume for buy operation | Ask the money module for size before opening a long |
| `LotOpenShort` | `double` | Gets trade volume for sell operation | Ask the money module for size before opening a short |
| `LotReverse` | `double` | Gets trade volume for position reverse | Use when a reversal needs a dedicated volume policy |
| `PrepareHistoryDate` | `void` | Sets starting date for tracking of trade history | Set this before collecting checkpoints or replaying historical state |
| `HistoryPoint` | `void` | Creates a checkpoint of trade history | Capture a baseline before comparing subsequent order/deal changes |
| `CheckTradeState` | `bool` | Compares the current state with the saved one and calls the corresponding event handler | Run after trade activity to fan out the specific trade-event callbacks |
| `WaitEvent` | `void` | Sets the event waiting flag | Use when the expert expects follow-up trade events after a request |
| `NoWaitEvent` | `void` | Resets the event waiting flag | Clear the wait state once reconciliation is complete |
| `TradeEventPositionStopTake` | `bool` | Handles the position Stop Loss/Take Profit triggered event | Override to customise logic after protective exits |
| `TradeEventOrderTriggered` | `bool` | Handles the pending order triggered event | Override to react when a pending order becomes a position |
| `TradeEventPositionOpened` | `bool` | Handles the position opened event | Override to attach post-entry bookkeeping or analytics |
| `TradeEventPositionVolumeChanged` | `bool` | Handles the position volume changed event | Override for partial fills, scale-ins, or scale-outs |
| `TradeEventPositionModified` | `bool` | Handles the position modified event | Override to react to stop or target changes |
| `TradeEventPositionClosed` | `bool` | Handles the position closed event | Override for post-exit accounting and reset logic |
| `TradeEventOrderPlaced` | `bool` | Handles the pending order placed event | Override to track newly staged pending orders |
| `TradeEventOrderModified` | `bool` | Handles the pending order modified event | Override to respond to pending-order parameter changes |
| `TradeEventOrderDeleted` | `bool` | Handles the pending order deleted event | Override for cleanup after pending-order removal |
| `TradeEventNotIdentified` | `bool` | Handles the non-identified event | Use as a fallback when state changes do not map cleanly to a known event |
| `TimeframeAdd` | `void` | Adds a timeframe for tracking | Register all extra timeframes before signal refresh begins |
| `TimeframesFlags` | `int` | Forms the timeframe flags | Use the bitmask when coordinating multi-timeframe refresh logic |
| `SelectPosition` | `void` | Selects a position to work with | Refresh the working position before close, reverse, or trail actions |
| `Signal` | `CExpertSignal*` | Gets the pointer to the trade signal object | Use to inspect or replace the delegated signal module after setup |

### CExpertTrailing Delegated Methods

| Method | Return type | Purpose | Usage note |
|--------|------------|---------|------------|
| `CExpertTrailing::CheckTrailingStopLong` | `bool` | Checks conditions to modify parameters of a long position | Implement this in the delegated trailing class that `CExpert` owns and calls |
| `CExpertTrailing::CheckTrailingStopShort` | `bool` | Checks conditions to modify parameters of a short position | Implement this in the delegated trailing class that `CExpert` owns and calls |

---

## References

- `docs/mql5_com_-_docs/standardlibrary-expertclasses-expertbaseclasses-cexpert*.md`
- `docs/mql5_com_-_docs/standardlibrary-expertclasses-expertbaseclasses-cexperttrailing*.md`
