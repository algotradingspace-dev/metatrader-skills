# trading-web-systems

Agent skill for web-based trading and fintech systems engineering in
TypeScript/React.

## Included skills

- **Fintech Web Systems** — decimal-safe money arithmetic (Decimal.js),
  core trading metrics in TypeScript (Sharpe, Calmar, Drawdown, Profit
  Factor), real-time WebSocket market data feeds via Cloudflare Durable
  Objects, React live-price hooks with auto-reconnect, PriceTicker/OrderBook
  dashboard components, and idempotent OHLCV ingestion pipelines on D1.

## Usage

```bash
claude plugin install ./plugins/trading-web-systems
```

Then reference the skill by name in your prompts (e.g. "use
fintech-web-systems — build a live order book component").

For MQL5 Expert Advisors, use the `mql5-development` plugin instead.
