# Chart Analysis Workspace — Charts, Indicators, and Templates

MetaTrader chart analysis is split between technical analysis on price
charts and fundamental analysis via news plus the Economic Calendar.
The chart workspace supports up to 100 open charts and 21 timeframes
from `M1` through `MN1`.

---

## Chart Workspace

| Topic | Detail |
|-------|--------|
| Chart types | Bar, candlestick, line |
| Timeframes | M1, M2, M3, M4, M5, M6, M10, M12, M15, M20, M30, H1, H2, H3, H4, H6, H8, D1, W1, MN1 |
| Max open charts | 100 |
| Customisation | Chart type, colours, scale, OHLC line display, multi-chart layout |
| Indicators | Built-in indicators and Market/Code Base downloads accessible as chart-level tools |
| Fundamentals | News + Economic Calendar integrated into the same analysis workflow |

---

## Templates and Profiles

| Topic | Practical rule |
|-------|----------------|
| Templates | Stored as `.tpl` under `MQL5\Profiles\Templates`; can include indicators, objects, and EA parameters |
| Built-in templates | `default.tpl`, `tester.tpl`, and `debug.tpl` are special-purpose defaults |
| Profiles | Stored under `MQL5\Profiles\Charts`; preserve chart set, placement, and applied templates |
| Account-specific profile | A profile named with the account number is auto-applied on account switch |
| Safety | Platform settings can disable EAs automatically when changing profiles |

### UI Workflows

- Manage active and deleted charts, inspect chart object lists, and adjust
  chart settings before debugging template or profile behaviour
- Templates are reusable chart recipes; profiles are reusable workspaces
- Deleted charts, chart-object lists, print settings are terminal-level
  maintenance tools, not coding APIs

---

## References

- `docs/metatrader5_com_-_terminal_help/charts_analysis.md`
- `docs/metatrader5_com_-_terminal_help/charts_analysis-charts.md`
- `docs/metatrader5_com_-_terminal_help/charts_analysis-charts_advanced.md`
- `docs/metatrader5_com_-_terminal_help/charts_analysis-charts_analysis_get_indicators.md`
- `docs/metatrader5_com_-_terminal_help/charts_analysis-fundamental.md`
- `docs/metatrader5_com_-_terminal_help/charts_analysis-indicators.md`
- `docs/metatrader5_com_-_terminal_help/charts_analysis-mql5_charts.md`
- `docs/metatrader5_com_-_terminal_help/charts_advanced-charts_deleted.md`
- `docs/metatrader5_com_-_terminal_help/charts_advanced-charts_manage.md`
- `docs/metatrader5_com_-_terminal_help/charts_advanced-charts_objects_list.md`
- `docs/metatrader5_com_-_terminal_help/charts_advanced-charts_print.md`
- `docs/metatrader5_com_-_terminal_help/charts_advanced-charts_settings.md`
- `docs/metatrader5_com_-_terminal_help/charts_advanced-templates_profiles.md`
