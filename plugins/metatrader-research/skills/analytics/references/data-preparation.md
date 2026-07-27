# Data Preparation

Self-written guidance for structuring MetaTrader-derived data before analysis.

---

## Primary Data Shapes

Most MetaTrader analysis starts from one or more of these tables:

- deals or executions
- orders or order lifecycle events
- open or closed positions
- equity or balance time series
- candle or tick data
- parameter-set metadata for a strategy run

Bring each dataset into a tidy table before calculating metrics.

---

## Minimum Columns By Dataset

### Deal History

Keep at least:

- `ticket`
- `order`
- `position_id`
- `symbol`
- `type`
- `entry`
- `volume`
- `price`
- `profit`
- `commission`
- `swap`
- `time`

### Order History

Keep at least:

- `ticket`
- `position_id`
- `symbol`
- `type`
- `state`
- `volume_initial`
- `volume_current`
- `price_open`
- `sl`
- `tp`
- `time_setup`
- `time_done`

### Candle Data

Keep at least:

- `time`
- `symbol`
- `timeframe`
- `open`
- `high`
- `low`
- `close`
- `tick_volume`

---

## Normalization Rules

Apply these rules consistently:

- convert all timestamps to UTC-aware datetimes
- standardize symbol names exactly as supplied by the source system
- normalize numeric fields to real numeric dtypes before aggregation
- separate missing values from true zeros
- keep original IDs even if you later derive grouped summaries

Do not collapse tickets, position IDs, or order IDs too early. Those identifiers are often needed later to reconstruct trade lifecycle behavior.

---

## Join Strategy

Use joins deliberately:

- join deals to orders by order ticket when analyzing execution lifecycle
- join deals to position IDs when analyzing full trade outcomes
- join strategy-run metadata by run ID rather than by filenames when possible
- join candle data only when the analysis truly needs market context around trades

Avoid broad many-to-many joins that duplicate trade rows silently.

---

## Equity Curve Preparation

If equity data is not already present, derive a clean curve from realized results carefully.

Minimum fields:

- timestamp
- realized P&L
- cumulative P&L or equity
- optional balance and floating P&L if available

For drawdown analysis, document whether the curve is:

- closed-equity only
- balance only
- full equity including floating P&L

That choice materially changes the interpretation of risk.

---

## Parameter Metadata

For EA variant analysis, attach run metadata explicitly:

- EA name and version
- parameter-set label
- symbol
- timeframe
- date range
- modeling mode if relevant
- account assumptions such as deposit or leverage

Without that metadata, comparison tables become unreliable quickly.

---

## Practical Rule

Do not start with plots. Start with clean tables, explicit keys, known timezones, and a reproducible dataset schema.