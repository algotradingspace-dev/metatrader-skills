# Trade Management Strategy Profiles

## Profile 1 — Sniper (High R:R, Low WR)

```
No partial close      — let full position run to 3:1 TP
Breakeven at 1.5:1    — protect after gaining ground
ATR trail from 2.0:1  — lock in extended moves
Target TP: 3:1        — minimum
Expected WR: 40-50%   — acceptable at this R:R
```

```mql5
g_TradeMgr = new CTradeManager(magic, 1.5, 2.0, 99.0, 0.0);
```

## Profile 2 — Scalper (Quick profit, tight management)

```
50% partial at 1.0:1  — lock half immediately
Breakeven at 0.8:1    — very early, capital protection mode
0.5x ATR trail        — tight trail for quick exits
Target TP: 1.5-2.0:1  — realistic at 60%+ WR
Expected WR: 60%+     — required at low R:R
```

```mql5
g_TradeMgr = new CTradeManager(magic, 0.8, 1.2, 1.0, 0.5);
```

## Profile 3 — Swing Trader (Multi-day positions)

```
33% at 1.0:1, 33% at 2.0:1, trail remainder
Breakeven at 1.0:1
2x ATR trail          — wide trail, let winners run
Target TP: 3-5:1 over days to weeks
Expected WR: 40%      — acceptable at 4:1 average R:R
```

```mql5
g_TradeMgr = new CTradeManager(magic, 1.0, 2.0, 1.0, 0.33);
```
