---
name: fintech-web-systems
description: >
  Elite TypeScript/React fintech and trading systems engineering skill. Use for ALL web-based
  trading infrastructure: decimal-safe money arithmetic, core trading metric implementations
  (Sharpe, Calmar, Drawdown, Profit Factor), real-time WebSocket market data feeds using
  Cloudflare Durable Objects, React hooks for live prices, trading dashboard UI components
  (PriceTicker, OrderBook), and OHLCV data ingestion pipelines. Precision is non-negotiable
  — never approximate money calculations. Trigger on: "trading dashboard", "live prices",
  "WebSocket feed", "order book", "price ticker", "OHLCV ingestion", "Sharpe Ratio TypeScript",
  "money arithmetic", "Decimal library", "profit factor", "fintech frontend".
  Note: For MQL5 EA implementations, use the mql5-* skills instead.
---

# Fintech Web Systems Skill

In fintech, a rounding error is a financial error. Latency is money. Build these systems
with precision as a first-class requirement, not an afterthought.

---

### CHUNK 1: Financial Arithmetic — Never Use Native Floats

```typescript
// WRONG — floating-point kills fintech
const price    = 19.99;
const quantity = 3;
const total    = price * quantity;  // → 59.97000000000001 !!!

// RIGHT — use Decimal.js for all calculations
import Decimal from 'decimal.js';

const priceD = new Decimal('19.99');  // Always pass as string
const totalD = priceD.times(3);      // Decimal { value: '59.97' }

// Store in database as integer cents — never as float
const priceCents = 1999;   // $19.99
const totalCents = priceCents * 3;   // 5997 — exact

// Format for display with Intl (handles locale, currency symbol)
const formatCurrency = (cents: number, currency = 'USD', locale = 'en-US'): string =>
  new Intl.NumberFormat(locale, {
    style: 'currency',
    currency,
    minimumFractionDigits: 2,
  }).format(cents / 100);

// Price formatting for trading UI (more decimal places)
const formatPrice = (value: number, decimals = 5): string =>
  new Decimal(value).toFixed(decimals);
```

**Storage rule:** Store all monetary values as integers in base units (cents for USD, satoshis for BTC, pips×10 for forex). Convert to display format only at render time.

---

### CHUNK 2: Core Trading Metrics in TypeScript

Performance metrics that match standard financial analysis definitions.

```typescript
// Profit Factor = Gross Profit / Gross Loss
const profitFactor = (trades: { pnl: number }[]): number => {
  const wins  = trades.filter(t => t.pnl > 0).reduce((s, t) => s + t.pnl, 0);
  const losses = Math.abs(trades.filter(t => t.pnl < 0).reduce((s, t) => s + t.pnl, 0));
  return losses === 0 ? Infinity : wins / losses;
};

// Win Rate + Expected Payoff
const tradingStats = (trades: { pnl: number }[]) => {
  const wins       = trades.filter(t => t.pnl > 0);
  const losses     = trades.filter(t => t.pnl < 0);
  const winRate    = wins.length / trades.length;
  const avgWin     = wins.reduce((s, t) => s + t.pnl, 0) / (wins.length || 1);
  const avgLoss    = Math.abs(losses.reduce((s, t) => s + t.pnl, 0)) / (losses.length || 1);
  const expectancy = winRate * avgWin - (1 - winRate) * avgLoss;
  return { winRate, avgWin, avgLoss, expectancy, pf: profitFactor(trades) };
};

// Maximum Drawdown (from equity curve array)
const maxDrawdown = (equity: number[]): number => {
  let peak = equity[0];
  let maxDD = 0;
  for(const val of equity) {
    if(val > peak) peak = val;
    const dd = (peak - val) / peak;
    if(dd > maxDD) maxDD = dd;
  }
  return maxDD * 100; // Returns as percentage
};

// Sharpe Ratio (annualized, daily returns)
const sharpeRatio = (returns: number[], riskFreeRate = 0.05): number => {
  const excess = returns.map(r => r - riskFreeRate / 252);
  const mean   = excess.reduce((s, r) => s + r, 0) / excess.length;
  const variance = excess.reduce((s, r) => s + Math.pow(r - mean, 2), 0) / excess.length;
  const std    = Math.sqrt(variance);
  return std === 0 ? 0 : (mean / std) * Math.sqrt(252);
};

// Recovery Factor = Net Profit / Max Drawdown
const recoveryFactor = (netProfit: number, maxDD: number): number =>
  maxDD === 0 ? 0 : netProfit / maxDD;

// Fixed fractional position sizing
const positionSize = (
  accountBalance: number,
  riskPercent: number,    // e.g. 0.01 for 1%
  stopLossDistance: number,
  tickValue: number
): number => {
  const riskAmount   = accountBalance * riskPercent;
  const riskPerUnit  = stopLossDistance * tickValue;
  return Math.floor(riskAmount / riskPerUnit);
};
```

---

### CHUNK 3: WebSocket Market Data Feed (Cloudflare Durable Objects)

Persistent WebSocket connections that fan out price updates to all subscribed clients.

```typescript
export class MarketFeedDO implements DurableObject {
  private sessions: Map<string, WebSocket> = new Map();
  private prices: Record<string, number>   = {};

  async fetch(request: Request): Promise<Response> {
    const upgrade = request.headers.get('Upgrade');
    if(upgrade === 'websocket') {
      const [client, server] = Object.values(new WebSocketPair());
      server.accept();
      const id = crypto.randomUUID();
      this.sessions.set(id, server);

      // Send current prices on connect
      server.send(JSON.stringify({ type: 'snapshot', prices: this.prices }));

      server.addEventListener('message', (event) => {
        const msg = JSON.parse(event.data as string);
        if(msg.type === 'subscribe') {
          // Client subscribes to specific symbols
          server.send(JSON.stringify({ type: 'subscribed', symbols: msg.symbols }));
        }
      });

      server.addEventListener('close', () => this.sessions.delete(id));
      return new Response(null, { status: 101, webSocket: client });
    }

    // Internal price update endpoint (called by data ingestion worker)
    if(request.method === 'POST') {
      const update = await request.json() as { symbol: string; price: number; bid: number; ask: number };
      this.prices[update.symbol] = update.price;
      this.broadcast({ type: 'tick', ...update, timestamp: Date.now() });
      return new Response('ok');
    }
    return new Response('Not found', { status: 404 });
  }

  private broadcast(data: object) {
    const msg = JSON.stringify(data);
    for(const [id, ws] of this.sessions) {
      try { ws.send(msg); }
      catch { this.sessions.delete(id); }
    }
  }
}
```

---

### CHUNK 4: React Hook for Live Prices

```typescript
interface MarketDataState {
  prices:      Record<string, number>;
  connected:   boolean;
  error:       string | null;
  lastUpdated: Date | null;
}

export function useLiveMarketData(symbols: string[], wsUrl: string) {
  const [state, setState] = useState<MarketDataState>({
    prices: {}, connected: false, error: null, lastUpdated: null,
  });
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    let retryDelay = 1000;

    const connect = () => {
      const ws = new WebSocket(wsUrl);
      wsRef.current = ws;

      ws.onopen = () => {
        setState(s => ({ ...s, connected: true, error: null }));
        ws.send(JSON.stringify({ type: 'subscribe', symbols }));
        retryDelay = 1000; // Reset backoff on successful connect
      };

      ws.onmessage = (event) => {
        const msg = JSON.parse(event.data);
        if(msg.type === 'snapshot')
          setState(s => ({ ...s, prices: msg.prices, lastUpdated: new Date() }));
        if(msg.type === 'tick')
          setState(s => ({
            ...s,
            prices: { ...s.prices, [msg.symbol]: msg.price },
            lastUpdated: new Date()
          }));
      };

      ws.onclose = () => {
        setState(s => ({ ...s, connected: false }));
        // Exponential backoff reconnect (max 30s)
        setTimeout(connect, Math.min(retryDelay, 30000));
        retryDelay *= 2;
      };

      ws.onerror = () =>
        setState(s => ({ ...s, error: 'WebSocket connection failed' }));
    };

    connect();
    return () => wsRef.current?.close();
  }, [wsUrl, symbols.join(',')]);

  return state;
}
```

---

### CHUNK 5: Price Ticker and Order Book UI Components

**Price Ticker with flash animation on price change:**

```tsx
interface TickerProps {
  symbol: string;
  price: number;
  change: number;
  prevPrice: number;
}

function PriceTicker({ symbol, price, change, prevPrice }: TickerProps) {
  const [flash, setFlash] = useState<'up' | 'down' | null>(null);

  useEffect(() => {
    if(prevPrice === price) return;
    setFlash(price > prevPrice ? 'up' : 'down');
    const t = setTimeout(() => setFlash(null), 300);
    return () => clearTimeout(t);
  }, [price]);

  const flashClass = flash === 'up' ? 'bg-green-500/20' : flash === 'down' ? 'bg-red-500/20' : '';
  const changeClass = change >= 0 ? 'text-green-400' : 'text-red-400';

  return (
    <div className={`flex items-center gap-3 p-2 rounded transition-colors duration-300 ${flashClass}`}>
      <span className="font-mono font-bold text-white w-20">{symbol}</span>
      <span className="font-mono text-lg text-white">{formatPrice(price)}</span>
      <span className={`font-mono text-sm ${changeClass}`}>
        {change >= 0 ? '+' : ''}{change.toFixed(2)}%
      </span>
    </div>
  );
}
```

**Order Book — shows bid/ask depth with visual fill bars:**

```tsx
function OrderBook({ bids, asks }: { bids: Level[]; asks: Level[] }) {
  const maxSize = Math.max(...bids.map(b => b.size), ...asks.map(a => a.size));

  return (
    <div className="font-mono text-sm">
      <div className="text-gray-400 grid grid-cols-2 gap-4 px-2 mb-1">
        <span>Price</span><span className="text-right">Size</span>
      </div>
      {asks.slice().reverse().map(level => (
        <OrderRow key={level.price} level={level} side="ask" maxSize={maxSize} />
      ))}
      {bids.map(level => (
        <OrderRow key={level.price} level={level} side="bid" maxSize={maxSize} />
      ))}
    </div>
  );
}

function OrderRow({ level, side, maxSize }: { level: Level; side: 'bid' | 'ask'; maxSize: number }) {
  const fill     = (level.size / maxSize) * 100;
  const bg       = side === 'bid' ? 'bg-green-500/15' : 'bg-red-500/15';
  const text     = side === 'bid' ? 'text-green-400' : 'text-red-400';

  return (
    <div className="relative grid grid-cols-2 gap-4 px-2 py-0.5 hover:bg-white/5">
      <div className={`absolute inset-y-0 right-0 ${bg}`} style={{ width: `${fill}%` }} />
      <span className={text}>{level.price.toFixed(5)}</span>
      <span className="text-right text-gray-300">{level.size.toFixed(2)}</span>
    </div>
  );
}
```

---

### CHUNK 6: OHLCV Data Ingestion Pipeline

Scheduled Cloudflare Worker that fetches and stores market data.

```typescript
export default {
  async scheduled(event: ScheduledEvent, env: Env, ctx: ExecutionContext) {
    await ingestMarketData(env);
  }
};

async function ingestMarketData(env: Env): Promise<void> {
  const symbols  = ['EURUSD', 'GBPUSD', 'XAUUSD', 'US500'];
  const interval = '15m';

  await Promise.allSettled(
    symbols.map(sym => fetchAndStoreOHLCV(sym, interval, env))
  );
}

async function fetchAndStoreOHLCV(symbol: string, interval: string, env: Env) {
  const url = `${env.DATA_PROVIDER_URL}/ohlcv/${symbol}?interval=${interval}&limit=100`;
  const res = await fetch(url, {
    headers: { 'X-API-Key': env.DATA_PROVIDER_KEY }
  });
  if(!res.ok) throw new Error(`Failed to fetch ${symbol}: ${res.status}`);

  const data: OHLCVBar[] = await res.json();
  const stmts = data.map(bar =>
    env.DB.prepare(`
      INSERT OR REPLACE INTO ohlcv (symbol, interval, timestamp, open, high, low, close, volume)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    `).bind(symbol, interval, bar.timestamp, bar.open, bar.high, bar.low, bar.close, bar.volume)
  );
  await env.DB.batch(stmts);
}
```

**Implementation checklist:**
```
□ All money values stored as integers (cents, basis points, or satoshis)
□ All calculations use Decimal.js — no native float arithmetic on monetary values
□ Numbers displayed using Intl.NumberFormat (locale-aware)
□ Timestamps stored as Unix seconds (not milliseconds) for consistency
□ WebSocket reconnects with exponential backoff (max 30s delay)
□ Price updates trigger only on actual change (prevent needless re-renders)
□ Order book limited to top 10–20 levels — don't render 1000 rows
□ Data ingestion uses INSERT OR REPLACE — idempotent on repeated runs
```

---

### SKILL SUMMARY

**What this skill enables:**
- Implement decimal-safe financial arithmetic in TypeScript
- Calculate all standard trading performance metrics (Sharpe, PF, MaxDD, Recovery Factor)
- Build real-time WebSocket price feeds using Cloudflare Durable Objects
- Create React hooks for live market data with auto-reconnect
- Build PriceTicker and OrderBook UI components with live flash animations
- Design OHLCV data ingestion pipelines with idempotent D1 storage

**When to use:**
- Building trading dashboards, portfolio trackers, or live price displays
- Implementing performance reporting in a TypeScript backend
- Adding real-time market data to any web application
- Designing data pipelines for historical OHLCV storage
- Any TypeScript/React project that needs financial precision calculations
