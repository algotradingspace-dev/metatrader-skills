# Raw OrderSend API — Structures, Retcodes, and OrderCheck

> Use when CTrade wrapper is insufficient or you need direct retcode control.

## MqlTradeRequest Key Fields

| Field | Type | Required for | Notes |
|-------|------|-------------|-------|
| `action` | ENUM_TRADE_ACTION | all | DEAL/PENDING/SLTP/MODIFY/REMOVE/CLOSE_BY |
| `magic` | ulong | all | EA identifier |
| `symbol` | string | all | instrument |
| `volume` | double | DEAL/PENDING | lots |
| `price` | double | PENDING/SLTP | 0 for market |
| `sl` | double | any | stop loss price |
| `tp` | double | any | take profit price |
| `deviation` | ulong | DEAL | max slippage in points |
| `type` | ENUM_ORDER_TYPE | all | BUY/SELL/BUY_LIMIT/SELL_STOP... |
| `type_filling` | ENUM_ORDER_TYPE_FILLING | DEAL | FOK/IOC/RETURN |
| `type_time` | ENUM_ORDER_TYPE_TIME | PENDING | GTC/DAY/SPECIFIED/SPECIFIED_DAY |
| `expiration` | datetime | SPECIFIED | order expiry time |
| `comment` | string | any | max 63 chars |
| `position` | ulong | MODIFY/CLOSE | position ticket |
| `position_by` | ulong | CLOSE_BY | counter-position ticket |

## MqlTradeResult Fields

| Field | Type | Notes |
|-------|------|-------|
| `retcode` | uint | server return code (10008-10036) |
| `deal` | ulong | deal ticket if filled |
| `order` | ulong | order ticket |
| `volume` | double | volume confirmed by server |
| `price` | double | execution price |
| `bid`/`ask` | double | current prices at execution |
| `comment` | string | server comment / error text |
| `request_id` | uint | async request ID (OrderSendAsync) |

## Key TRADE_RETCODE Values

| Code | Constant | Meaning |
|------|----------|---------|
| 10008 | TRADE_RETCODE_PLACED | order placed (async) |
| 10009 | TRADE_RETCODE_DONE | executed fully |
| 10010 | TRADE_RETCODE_DONE_PARTIAL | executed partially |
| 10013 | TRADE_RETCODE_INVALID | invalid request |
| 10014 | TRADE_RETCODE_INVALID_VOLUME | bad volume |
| 10015 | TRADE_RETCODE_INVALID_PRICE | bad price |
| 10016 | TRADE_RETCODE_INVALID_STOPS | bad SL/TP |
| 10018 | TRADE_RETCODE_MARKET_CLOSED | market closed |
| 10019 | TRADE_RETCODE_NO_MONEY | insufficient funds |
| 10021 | TRADE_RETCODE_PRICE_CHANGED | price requote |
| 10027 | TRADE_RETCODE_CLIENT_DISABLES_AT | auto-trading disabled |
| 10030 | TRADE_RETCODE_FROZEN | order/position frozen |
| 10036 | TRADE_RETCODE_CLOSE_ORDER_EXIST | close order already exists |

## OrderSend vs OrderSendAsync

```mql5
// Synchronous — wait for server response (most EAs)
bool ok = OrderSend(request, result);
if(!ok || result.retcode != TRADE_RETCODE_DONE)
   PrintFormat("OrderSend failed: retcode=%u comment=%s", result.retcode, result.comment);

// Async — fire and forget, confirmed in OnTradeTransaction
bool ok = OrderSendAsync(request, result);
// result.request_id links back to OnTradeTransaction trans.request_id
```

## OrderCheck Before Sending

```mql5
MqlTradeRequest req = {};
MqlTradeCheckResult chk = {};
if(OrderCheck(req, chk)) {
   // chk.margin       — margin required
   // chk.margin_free  — free margin after
   // chk.margin_level — margin level after (%)
   // chk.balance      — balance after
   // chk.retcode == 0 — OK
}
// Returns false if funds insufficient or fields invalid
```
