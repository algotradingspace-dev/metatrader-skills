# Platform Interface Quick-Start

## Main UI Areas

| UI Area | Purpose | Key Detail |
|---------|---------|------------|
| **Main Menu** | All commands and functions — File, View, Insert, Charts, Tools, Window, Help | Entry point for all non-toolbar operations |
| **Toolbars** | Standard, Line Studies, Periodicity — duplicates common menu commands | Customisable; add/remove controls |
| **Market Watch** | Price data, tick charts, contract specifications, one-click trading | Right-click for context menu with symbol management |
| **Navigator** | Account switching, EA/indicator launch, Market/Code Base access, VPS rental | Drag items from Navigator onto chart to attach |
| **Chart** | Price chart display — 21 timeframes M1 through MN1 | Multiple chart types: bar, candlestick, line |
| **Toolbox** | Trade positions, news, history, alerts, mailbox, journals, Expert Advisors | Multi-tab; also used to place and modify orders |

---

## Account Opening (Quick-Start Flow)

1. Open **File → Open an Account** or right-click in Navigator
2. Select broker server or enter address manually
3. Choose **New demo account** or **Connect to existing**
4. Fill registration form; credentials are emailed or shown immediately

---

## Authorization / Login

- **Auto-login:** enabled by default when "Save password" is checked at login
- **Manual:** File → Login, or right-click the account in Navigator → Log In
- Login requires server address + account number + password

---

## Platform Settings (Tools → Options)

| Tab | Notable settings |
|-----|------------------|
| **Server** | Server address, proxy, data centre |
| **Charts** | Max bars in chart/history, colour schemes |
| **Trade** | Default lot, deviation, confirmation dialogs |
| **Expert Advisors** | Auto Trading master switch, allowed URL list for WebRequest |
| **Notifications** | Push notification token, email SMTP/IMAP config |
| **Events** | Sound and email events for price/trade triggers |

---

## Payments

- **Deposit/Withdrawal** accessible from the account menu or broker
  web-interface link in the Navigator
- Internal transfers between accounts of the same broker are handled
  through the Toolbox → Trade tab context menu

---

## References

- `docs/metatrader5_com_-_terminal_help/startworking.md`
- `docs/metatrader5_com_-_terminal_help/startworking-acc_open.md`
- `docs/metatrader5_com_-_terminal_help/startworking-authorization.md`
- `docs/metatrader5_com_-_terminal_help/startworking-interface.md`
- `docs/metatrader5_com_-_terminal_help/startworking-payments.md`
- `docs/metatrader5_com_-_terminal_help/startworking-settings.md`
