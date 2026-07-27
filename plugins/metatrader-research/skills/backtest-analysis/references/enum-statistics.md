# ENUM_STATISTICS — Full `TesterStatistics()` Reference

All values are returned as `double`. Monetary values are in deposit currency.

## Double/Integer Values

| Identifier | Description | Type |
|------------|-------------|------|
| `STAT_INITIAL_DEPOSIT` | Initial deposit | double |
| `STAT_WITHDRAWAL` | Money withdrawn | double |
| `STAT_PROFIT` | Net profit (= GROSS_PROFIT + GROSS_LOSS) | double |
| `STAT_GROSS_PROFIT` | Sum of all profitable trades (>= 0) | double |
| `STAT_GROSS_LOSS` | Sum of all losing trades (<= 0) | double |
| `STAT_MAX_PROFITTRADE` | Largest single profitable trade | double |
| `STAT_MAX_LOSSTRADE` | Largest single losing trade | double |
| `STAT_CONPROFITMAX` | Max profit in a consecutive winning series | double |
| `STAT_CONPROFITMAX_TRADES` | Trade count forming CONPROFITMAX | int |
| `STAT_MAX_CONWINS` | Total profit of the longest winning series | double |
| `STAT_MAX_CONPROFIT_TRADES` | Trade count in longest winning series | int |
| `STAT_CONLOSSMAX` | Max loss in a consecutive losing series | double |
| `STAT_CONLOSSMAX_TRADES` | Trade count forming CONLOSSMAX | int |
| `STAT_MAX_CONLOSSES` | Total loss of the longest losing series | double |
| `STAT_MAX_CONLOSS_TRADES` | Trade count in longest losing series | int |
| `STAT_BALANCEMIN` | Minimum balance value | double |
| `STAT_BALANCE_DD` | Max balance drawdown in monetary terms | double |
| `STAT_BALANCEDD_PERCENT` | Balance DD% at moment of max monetary DD | double |
| `STAT_BALANCE_DDREL_PERCENT` | Max balance DD as percentage | double |
| `STAT_BALANCE_DD_RELATIVE` | Balance DD (currency) at moment of max %DD | double |
| `STAT_EQUITYMIN` | Minimum equity value | double |
| `STAT_EQUITY_DD` | Max equity drawdown in monetary terms | double |
| `STAT_EQUITYDD_PERCENT` | Equity DD% at moment of max monetary DD | double |
| `STAT_EQUITY_DDREL_PERCENT` | Max equity DD as percentage | double |
| `STAT_EQUITY_DD_RELATIVE` | Equity DD (currency) at moment of max %DD | double |
| `STAT_EXPECTED_PAYOFF` | Expected payoff per trade | double |
| `STAT_PROFIT_FACTOR` | GROSS_PROFIT / abs(GROSS_LOSS); DBL_MAX if no losses | double |
| `STAT_RECOVERY_FACTOR` | PROFIT / BALANCE_DD | double |
| `STAT_SHARPE_RATIO` | Sharpe ratio | double |
| `STAT_MIN_MARGINLEVEL` | Minimum margin level % | double |
| `STAT_CUSTOM_ONTESTER` | Custom criterion value from `OnTester()` | double |
| `STAT_DEALS` | Number of deals | int |
| `STAT_TRADES` | Number of trades | int |
| `STAT_PROFIT_TRADES` | Profitable trades | int |
| `STAT_LOSS_TRADES` | Losing trades | int |
| `STAT_SHORT_TRADES` | Short trades | int |
| `STAT_LONG_TRADES` | Long trades | int |
| `STAT_PROFIT_SHORTTRADES` | Profitable short trades | int |
| `STAT_PROFIT_LONGTRADES` | Profitable long trades | int |
| `STAT_PROFITTRADES_AVGCON` | Avg length of a profitable consecutive series | int |
| `STAT_LOSSTRADES_AVGCON` | Avg length of a losing consecutive series | int |
| `STAT_COMPLEX_CRITERION` | Complex optimisation criterion | double |

> Available only in `OnTester()`, `OnTesterInit()`, `OnTesterDeinit()`, `OnTesterPass()`.
> Call `FrameAdd("stats", 0, 0.0, TesterStatistics(STAT_PROFIT_FACTOR))` to pass values to controller.
