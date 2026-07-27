# Runtime Error Codes and Trade Return Codes

**Pattern:** `int err = GetLastError(); ResetLastError();`

## Key Runtime Error Groups

| Range | Group | Key examples |
|-------|-------|-------------|
| 0 | Success | `ERR_SUCCESS` |
| 4001-4025 | General | `ERR_INVALID_PARAMETER`(4003), `ERR_NOT_ENOUGH_MEMORY`(4004), `ERR_INVALID_POINTER`(4012) |
| 4101-4116 | Charts | `ERR_CHART_NOT_FOUND`(4103), `ERR_CHART_INDICATOR_NOT_FOUND`(4116) |
| 4201-4205 | Objects | `ERR_OBJECT_NOT_FOUND`(4202), `ERR_OBJECT_WRONG_PROPERTY`(4203) |
| 4301-4307 | Market | `ERR_MARKET_UNKNOWN_SYMBOL`(4301), `ERR_MARKET_NOT_SELECTED`(4302) |
| 4401-4407 | History | `ERR_HISTORY_NOT_FOUND`(4401), `ERR_HISTORY_TIMEOUT`(4403) |
| 4501-4525 | Global vars / misc | `ERR_GLOBALVARIABLE_NOT_FOUND`(4501) |
| 4601-4603 | Indicator buffers | `ERR_BUFFERS_WRONG_INDEX`(4602) |
| 4701-4758 | Account/Trade | `ERR_TRADE_DISABLED`(4752), `ERR_TRADE_SEND_FAILED`(4756) |
| 4801-4812 | Indicators | `ERR_INDICATOR_CANNOT_CREATE`(4802), `ERR_INDICATOR_WRONG_HANDLE`(4807) |
| 4901-4904 | Depth of Market | `ERR_BOOKS_CANNOT_SUBSCRIBE`(4904) |
| 5001-5027 | File ops | `ERR_CANNOT_OPEN_FILE`(5004), `ERR_FILE_NOT_EXIST`(5019) |
| 5050-5063 | Array ops | `ERR_INCOMPATIBLE_ARRAYS`(5050), `ERR_ZEROSIZE_ARRAY`(5053) |
| 5100-5114 | OpenCL | `ERR_OPENCL_NOT_SUPPORTED`(5100) |
| 5120-5129 | Database | `ERR_DATABASE_CONNECT`(5123), `ERR_DATABASE_EXECUTE`(5124) |
| 5200-5203 | WebRequest | `ERR_WEBREQUEST_TIMEOUT`(5202) |
| 5270-5275 | Sockets | `ERR_NETSOCKET_CANNOT_CONNECT`(5272) |
| 5300-5310 | Custom symbols | `ERR_CUSTOM_SYMBOL_EXIST`(5304) |
| 5400-5402 | Calendar | `ERR_CALENDAR_MORE_DATA`(5400) |
| 5700-5706 | Matrix/Vector | `ERR_MATRIX_INCONSISTENT`(5702) |
| 5800-5808 | ONNX | `ERR_ONNX_RUN_FAILED`(5803) |
| 65536+ | User errors | `ERR_USER_ERROR_FIRST` |

> Compile errors and warnings are MetaEditor diagnostics, not runtime `GetLastError()` values.

## TRADE_RETCODE — `MqlTradeResult.retcode` Values

| Code | Constant | Meaning |
|------|----------|---------|
| 10004 | `TRADE_RETCODE_REQUOTE` | Requote; retry with updated price |
| 10008 | `TRADE_RETCODE_PLACED` | Pending order placed |
| 10009 | `TRADE_RETCODE_DONE` | Request completed |
| 10010 | `TRADE_RETCODE_DONE_PARTIAL` | Partial fill |
| 10011 | `TRADE_RETCODE_ERROR` | Processing error |
| 10012 | `TRADE_RETCODE_TIMEOUT` | Timeout; recheck final order state |
| 10013 | `TRADE_RETCODE_INVALID` | Invalid request |
| 10016 | `TRADE_RETCODE_INVALID_STOPS` | Invalid SL/TP |
| 10018 | `TRADE_RETCODE_MARKET_CLOSED` | Market closed |
| 10019 | `TRADE_RETCODE_NO_MONEY` | Insufficient funds |
| 10030 | `TRADE_RETCODE_INVALID_FILL` | Filling type not supported |
| 10031 | `TRADE_RETCODE_CONNECTION` | No trade server connection |
| 10045 | `TRADE_RETCODE_FIFO_CLOSE` | Must close in FIFO order |
