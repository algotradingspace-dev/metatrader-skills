# Event Handlers — Signatures, Codes, Trade Transactions, Tester Chain

## Handler Signatures and Queue Deduplication

> Canonical MQL5 reference: [OnStart](https://www.mql5.com/en/docs/event_handlers/onstart) · [OnInit](https://www.mql5.com/en/docs/event_handlers/oninit) · [OnDeinit](https://www.mql5.com/en/docs/event_handlers/ondeinit) · [OnTick](https://www.mql5.com/en/docs/event_handlers/ontick)

| Handler | Program type | Signature | Fires when |
|---------|-------------|-----------|------------|
| `OnStart` | Script, Service | `int OnStart(void)` | Once at launch |
| `OnInit` | EA, Indicator | `int OnInit(void)` | On load, re-attach, input change |
| `OnDeinit` | EA, Indicator | `void OnDeinit(const int reason)` | On unload, symbol/TF change |
| `OnTick` | EA only | `void OnTick(void)` | Every new price tick |
| `OnCalculate` | Indicator only | `int OnCalculate(...)` | Price data change (2 overloads) |
| `OnTimer` | EA, Indicator | `void OnTimer(void)` | Periodic timer tick |
| `OnTrade` | EA only | `void OnTrade(void)` | After any trade server event |
| `OnTradeTransaction` | EA only | `void OnTradeTransaction(const MqlTradeTransaction&, const MqlTradeRequest&, const MqlTradeResult&)` | Each individual transaction |
| `OnBookEvent` | EA, Indicator | `void OnBookEvent(const string& symbol)` | Market depth change (requires `MarketBookAdd()`) |
| `OnChartEvent` | EA, Indicator | `void OnChartEvent(const int id, const long& lparam, const double& dparam, const string& sparam)` | Mouse, keyboard, object, custom events |
| `OnTester` | EA only | `double OnTester(void)` | After each tester pass |
| `OnTesterInit` | EA only | `int OnTesterInit(void)` | Before optimisation starts |
| `OnTesterDeinit` | EA only | `void OnTesterDeinit(void)` | After optimisation ends |
| `OnTesterPass` | EA only | `void OnTesterPass(void)` | Each frame from test agent arrives |

**Queue deduplication rules (critical for performance):**

> Canonical MQL5 reference: [NewTick](https://www.mql5.com/en/docs/runtime/event_fire#newtick) · [ChartEvent](https://www.mql5.com/en/docs/standardlibrary/controls/cappdialog/cappdialogchartevent) · [BookEvent](https://www.mql5.com/en/docs/runtime/event_fire#bookevent)

| Event | Dedup rule |
|-------|------------|
| `NewTick` | If already queued or processing → new tick discarded (never backlogged) |
| `Timer` | Same rule — discarded if already in queue or processing |
| `ChartEvent` | Same rule — discarded if already in queue or processing |
| `BookEvent` | **Never skipped** — always queued even while processing previous one |

**`OnTradeTransaction` vs `OnTrade`:**
- `OnTradeTransaction` fires for each individual atomic transaction (add order, add deal, etc.)
- `OnTrade` fires after one or more transactions complete — it is always called after the related `OnTradeTransaction` calls
- One `OrderSend` may produce multiple `OnTradeTransaction` calls and one or several `OnTrade` calls — **do not assume 1:1 ratio**

---

## OnInit Return Codes

| Code | Value | Effect |
|------|-------|--------|
| `INIT_SUCCEEDED` | 0 | Normal start, test runs |
| `INIT_FAILED` | 1 | EA forcibly unloaded; indicator stays but non-operational; test aborted |
| `INIT_PARAMETERS_INCORRECT` | – | Optimisation row highlighted red, pass skipped; agent receives next task |
| `INIT_AGENT_NOT_SUITABLE` | – | Agent receives no more tasks for the entire optimisation run |

`INIT_PARAMETERS_INCORRECT` and `INIT_AGENT_NOT_SUITABLE` are meaningful only in the Strategy Tester.

---

## OnDeinit Reason Codes

> Canonical MQL5 reference: [REASON_PROGRAM](https://www.mql5.com/en/docs/constants/namedconstants/uninit) · [ExpertRemove](https://www.mql5.com/en/docs/common/expertremove) · [REASON_INITFAILED](https://www.mql5.com/en/docs/constants/namedconstants/uninit#reason_initfailed) · [OnInit](https://www.mql5.com/en/docs/event_handlers/oninit)

| Constant | Value | Meaning |
|----------|-------|---------|
| `REASON_PROGRAM` | 0 | `ExpertRemove()` called |
| `REASON_REMOVE` | 1 | Removed from chart |
| `REASON_RECOMPILE` | 2 | Recompiled |
| `REASON_CHARTCHANGE` | 3 | Symbol or TF changed |
| `REASON_CHARTCLOSE` | 4 | Chart closed |
| `REASON_PARAMETERS` | 5 | Inputs changed |
| `REASON_ACCOUNT` | 6 | Account switch or reconnect |
| `REASON_TEMPLATE` | 7 | Template applied |
| `REASON_INITFAILED` | 8 | `OnInit()` returned non-zero |
| `REASON_CLOSE` | 9 | Terminal closed |

```mql5
void OnDeinit(const int reason) {
   PrintFormat("Deinit reason: %d (%s)", reason, EnumToString((ENUM_DEINIT_REASON)reason));
}
```

---

## OnTradeTransaction Lifecycle

`OnTradeTransaction` is fired for every atomic trade state change. Filter by `trans.type` before acting.

```mql5
void OnTradeTransaction(
   const MqlTradeTransaction& trans,
   const MqlTradeRequest&     request,
   const MqlTradeResult&      result)
{
   switch(trans.type) {
      case TRADE_TRANSACTION_ORDER_ADD:
      case TRADE_TRANSACTION_ORDER_UPDATE:
      case TRADE_TRANSACTION_ORDER_DELETE:
      case TRADE_TRANSACTION_DEAL_ADD:
      case TRADE_TRANSACTION_HISTORY_ADD:
         break;
   }
   // request and result are populated ONLY for TRADE_TRANSACTION_REQUEST type
}
```

**Critical: to read deal/order data after a `TRADE_TRANSACTION_DEAL_ADD` transaction, call `HistorySelect()` first:**
```mql5
case TRADE_TRANSACTION_DEAL_ADD: {
   HistorySelect(0, TimeCurrent());
   ulong deal_ticket = trans.deal;
   if(HistoryDealSelect(deal_ticket)) {
      double profit = HistoryDealGetDouble(deal_ticket, DEAL_PROFIT);
   }
}
```

**When to use which:**
- `OnTradeTransaction` for per-deal or per-order detail (log every fill, update tracking on exact execution)
- `OnTrade` for coarser post-trade reconciliation (recount open positions, sync state after any change)
- Both can coexist in the same EA

---

## Tester Event Handler Chain

The four tester handlers form a coordinated chain across two EA instances:
the **test agent EA** (runs passes) and the **controller EA** (collects results).

```
Optimisation flow:
  Controller EA loaded on chart
       |
       +-- OnTesterInit()           set ParameterSetRange(), init result storage
       |
       |  [for each optimisation pass]:
       |     Test agent EA: OnInit() -> OnTick()... -> OnDeinit() -> OnTester()
       |                                                                   |
       |                                             FrameAdd(value,...)   |
       |     Controller EA: OnTesterPass()           receive frame          |
       |
       +-- OnTesterDeinit()         final aggregation; FrameNext() for late frames
```

**`OnTester()` — custom optimisation criterion:**
```mql5
double OnTester() {
   double profit     = TesterStatistics(STAT_PROFIT);
   double drawdown   = TesterStatistics(STAT_BALANCE_DD);
   double trades     = TesterStatistics(STAT_TRADES);
   if(trades < 30 || drawdown <= 0) return 0;
   return profit / drawdown;
}
```

**`OnTesterInit()` — set optimisation ranges programmatically:**
```mql5
int OnTesterInit() {
   ParameterSetRange("InpRiskPercent", true,  1.0, 0.5, 0.25, 3.0);
   ParameterSetRange("InpATRPeriod",   true,  14,  10,  1,    30);
   ParameterSetRange("InpMagicNumber", false, 10001, 0, 0, 0);
   return INIT_SUCCEEDED;
}
```

**`OnTesterPass()` — receive frames:**
```mql5
void OnTesterPass() {
   ulong   pass;
   string  name;
   long    id;
   double  value;
   double  data[];
   while(FrameNext(pass, name, id, value, data)) {
      // process each frame
   }
}
```

**Gotcha:** Frames may arrive late. Call `FrameNext()` in `OnTesterDeinit()` to capture stragglers.

---

## References

- `docs/mql5_com_-_docs/event_handlers.md`
- `docs/mql5_com_-_docs/event_handlers-oninit.md`
- `docs/mql5_com_-_docs/event_handlers-ondeinit.md`
- `docs/mql5_com_-_docs/event_handlers-ontick.md`
- `docs/mql5_com_-_docs/event_handlers-ontimer.md`
- `docs/mql5_com_-_docs/event_handlers-ontrade.md`
- `docs/mql5_com_-_docs/event_handlers-ontradetransaction.md`
- `docs/mql5_com_-_docs/event_handlers-onbookevent.md`
- `docs/mql5_com_-_docs/event_handlers-onchartevent.md`
- `docs/mql5_com_-_docs/event_handlers-oncalculate.md`
- `docs/mql5_com_-_docs/event_handlers-onstart.md`
- `docs/mql5_com_-_docs/event_handlers-ontester.md`
- `docs/mql5_com_-_docs/event_handlers-ontesterinit.md`
- `docs/mql5_com_-_docs/event_handlers-ontesterdeinit.md`
- `docs/mql5_com_-_docs/event_handlers-ontesterpass.md`
