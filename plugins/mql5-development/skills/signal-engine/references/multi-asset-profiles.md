# Multi-Asset Signal Profiles

Different assets require different signal approaches due to liquidity and
volatility characteristics.

| Asset | Primary Strategy | Entry Method | Key Filter |
|-------|-----------------|-------------|------------|
| XAUUSD | SMC London Open | FVG limit order at midpoint | Asian range sweep + CHoCH |
| GBPUSD | London–NY overlap breakout | OB market order at close above | Session killzone |
| EURUSD | H4 trend continuation | EMA pullback to 21 EMA | H4 trend direction |
| US500/NAS100 | Gap fill + VWAP reclaim | VWAP reclaim on M15 | Pre-market gap >= 0.3% |
| XAGUSD | Gold follower | Delayed vs gold crossover | Gold/silver ratio extreme |
| BTCUSD | D1 OB + funding rate | D1 support OB limit | Funding rate negative = long |
