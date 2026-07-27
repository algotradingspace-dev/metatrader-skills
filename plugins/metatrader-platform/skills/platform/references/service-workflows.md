# Service Workflows — Signals, Cloud Network, Market, Hosting, Community, Mobile

---

## SV-1: Signals Service

The Signals service is the terminal UI for browsing providers, monitoring
performance, and configuring copy-trading subscriptions.

| Topic | Terminal-side rule |
|-------|--------------------|
| Monitoring | Provider pages expose growth, drawdown, subscriber count, and trade-history context used for selection |
| Subscription | Copy settings control deposit usage, slippage tolerance, and protective confirmation behaviour |
| Continuity | Subscriptions depend on the terminal or VPS staying online so copying remains active |
| Roles | Provider and subscriber workflows are distinct: one publishes signal performance, the other configures risk and mirroring |

**References:**
- `docs/metatrader5_com_-_terminal_help/signals.md`
- `docs/metatrader5_com_-_terminal_help/signals-signal_monitoring.md`
- `docs/metatrader5_com_-_terminal_help/signals-signal_provider.md`
- `docs/metatrader5_com_-_terminal_help/signals-signal_subscriber.md`

---

## SV-2: MQL5 Cloud Network

The MQL5 Cloud Network extends Strategy Tester optimisation beyond local
agents by renting distributed compute agents.

| Topic | Terminal-side rule |
|-------|--------------------|
| Install | MetaTester agents can be installed and managed without treating them as a full trading terminal |
| Use | Cloud agents are primarily for optimisation acceleration, not live-trading execution |
| Cost | Charges combine agent runtime and traffic consumption, so poor search quality or excess data transfer has a direct price |
| Selection | Agent productivity and tester mode determine whether remote agents are worth using |

**References:**
- `docs/metatrader5_com_-_terminal_help/mql5cloud.md`
- `docs/metatrader5_com_-_terminal_help/mql5cloud-mql5cloud_calculation.md`
- `docs/metatrader5_com_-_terminal_help/mql5cloud-mql5cloud_install.md`
- `docs/metatrader5_com_-_terminal_help/mql5cloud-mql5cloud_use.md`

---

## SV-3: Market Service

The Market tab is the terminal-native storefront for Expert Advisors,
indicators, and utilities.

| Topic | Terminal-side rule |
|-------|--------------------|
| Discovery | Ratings, reviews, price, and category filters are the first screening layer |
| Trial path | Demo versions and tester usage are the safe evaluation path before payment |
| Purchase and rent | Market apps support outright purchase and limited-term rentals depending on the listing |
| Activation | Products are tied to a finite activation model, so machine changes and redeployments must be planned |

**References:**
- `docs/metatrader5_com_-_terminal_help/market.md`
- `docs/metatrader5_com_-_terminal_help/market-market_buy.md`
- `docs/metatrader5_com_-_terminal_help/market-market_rent.md`
- `docs/metatrader5_com_-_terminal_help/market-market_sell.md`

---

## SV-4: Virtual Hosting

Virtual Hosting is the terminal-managed VPS layer for running EAs, indicators,
and signal subscriptions close to the broker server.

| Topic | Terminal-side rule |
|-------|--------------------|
| Migration | Migration is one-way from the local terminal state to the hosted instance |
| Modes | Hosting can migrate the whole environment, expert stack only, or signal copying only |
| Monitoring | The hosting panel exposes status, journal access, and resource-health checks |
| Renewal | Renewal rules depend on active usage and remaining subscription state |

**References:**
- `docs/metatrader5_com_-_terminal_help/virtual_hosting.md`
- `docs/metatrader5_com_-_terminal_help/virtual_hosting-virtual_hosting_migration.md`
- `docs/metatrader5_com_-_terminal_help/virtual_hosting-virtual_hosting_server.md`
- `docs/metatrader5_com_-_terminal_help/virtual_hosting-virtual_hosting_terminal.md`

---

## SV-5: MQL5 Community Services

The MQL5.community account is the shared identity and wallet behind Market,
Cloud Network, Signals, Storage, and platform chat services.

| Topic | Terminal-side rule |
|-------|--------------------|
| Identity | One MQL5.community account ties together purchases, rentals, cloud usage, and subscriptions |
| Communication | Built-in chat and messaging synchronise with the broader MQL5 service ecosystem |
| Storage | Community services also back cross-machine code or asset synchronisation workflows |
| Billing | Service spending and earnings roll into the same account-level wallet and history |

**References:**
- `docs/metatrader5_com_-_terminal_help/mql5community.md`

---

## SV-6: Mobile Trading

Mobile Trading is the handset and tablet extension of the MetaTrader platform,
not a reduced watchlist-only companion.

| Topic | Terminal-side rule |
|-------|--------------------|
| Analysis | Mobile terminals retain multi-timeframe charting, indicators, and analytical objects |
| Trading | Market and pending-order workflows remain available from the device UI |
| Account access | Mobile terminals connect to the same broker accounts and messaging services as desktop |
| Coordination | Mobile is a companion execution and monitoring surface, not a replacement for tester, Market install, or VPS migration workflows |

**References:**
- `docs/metatrader5_com_-_terminal_help/mobile_trading.md`
