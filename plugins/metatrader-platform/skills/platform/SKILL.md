---
name: platform
description: >
  MetaTrader 5 platform operations reference skill. Use for: installing MT5 on
  Windows/macOS/Linux; configuring startup modes and CLI keys; managing SSL
  certificates and 2FA/TOTP; understanding file/folder layout; managing
  accounts and transfers; reading platform logs, Task Manager, and live update
  behaviour; keyboard shortcuts; chart analysis workspace and templates; trading
  UI, DOM, Market Watch, margin models; platform drawing objects; custom symbols;
  MQL5 chart operations API; MQL5 object API. For MQL5 constants, use the
  constants skill. For the Python module, use the python skill. For the HTTP
  bridge, use the httpapi skill.
---

# Platform

Platform-level reference for MetaTrader 5 installation, configuration,
security, account management, and runtime operations.

This is a Reference skill: the body is a routing table into `references/`.
Read the relevant reference file for the topic you need.

## References

| File | Contents | Read when |
|------|----------|-----------|
| `references/platform-setup.md` | Windows/macOS/Linux installation, portable mode, CLI switches, uninstallation | Installing or troubleshooting MT5; deploying to headless Linux; configuring beta or silent install |
| `references/security-auth.md` | SSL certificate auth, 2FA/TOTP setup (desktop + mobile), data encryption | Setting up extended auth; configuring 2FA; troubleshooting certificate issues |
| `references/platform-internals.md` | File/folder layout, platform logs, Task Manager, live update system, crash dumps | Locating log files; monitoring thread/CPU metrics; understanding platform data directories |
| `references/account-management.md` | Account types, switching, fund transfers, security options, mailbox limits | Managing demo/live accounts; transferring funds; configuring account security |
| `references/keyboard-shortcuts.md` | Chart window, global, Market Watch, Navigator, Toolbox, Data Window hotkeys | Looking up keyboard shortcuts for any MT5 surface |
| `references/openclaw-live-trading.md` | Prompt patterns, separation of concerns, account routing, safety defaults for live execution | Structuring agent prompts that route trading actions to a live MT5 account |
| `references/interface-quickstart.md` | Main UI areas (menu, toolbars, Market Watch, Navigator, Chart, Toolbox), settings, payments | Navigating the terminal for the first time; configuring platform settings |
| `references/chart-analysis.md` | Chart workspace, built-in indicators, templates, profiles, chart settings | Understanding chart UI workflows; managing templates and profiles; chart printing |
| `references/trading-ui.md` | Market Watch, DOM, one-click trading, options board, margin models, custom instruments | Understanding order-entry surfaces; margin calculation models; synthetic symbols |
| `references/platform-objects.md` | Drawing object families (arrows, channels, Fibonacci, Gann, Elliott, shapes, widgets) | Platform drawing workflow; object anchoring behaviour |
| `references/custom-symbols.md` | Custom symbol lifecycle, property setup, bar/tick/DOM feed, removal | Creating or maintaining synthetic symbols |
| `references/service-workflows.md` | Signals, Cloud Network, Market, Virtual Hosting, Community, Mobile | Configuring signal subscriptions; renting VPS; cloud optimization; market purchases |
| `references/chart-operations-api.md` | MQL5 `Chart*` functions: lifecycle, properties, templates, indicators, coordinate conversion | Writing MQL5 code that opens, configures, or reads chart data |
| `references/object-api.md` | MQL5 `Object*` functions: lifecycle, properties, discovery, text rendering | Writing MQL5 code that creates or manipulates graphical objects |
