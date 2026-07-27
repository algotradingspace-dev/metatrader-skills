---
name: network
description: >
  MQL5 network and outbound communication reference skill. Use for: calling
  WebRequest from an EA or script; opening raw TCP or TLS sockets; sending or
  reading bytes; checking socket readability, writability, or connection state;
  setting socket send/receive timeouts; using terminal-mediated SendMail,
  SendFTP, or SendNotification. Trigger: "WebRequest", "socket", "HTTP from EA",
  "REST call from MQL5", "send data to server", "SendMail", "SendFTP",
  "SendNotification", "TLS socket", "TCP socket", "outbound communication",
  "socket create", "socket connect".
---

# Network

Use this skill when an EA or script must reach beyond the terminal sandbox and
communicate with HTTP endpoints, raw TCP services, or terminal-mediated
outbound notification channels.

This is a Reference skill: the body is a routing table into function-group
summaries. Read the relevant section for the network API you need.

---

## Purpose

Catalogs the MQL5 outbound communication surface: socket lifecycle (create,
connect, read, send, close), TLS handshake and secure I/O, `WebRequest()` for
HTTP, and terminal-mediated sends (email, FTP, push notifications).

---

## When to Use

- Calling REST or webhook endpoints from Expert Advisors or scripts
- Opening raw TCP or TLS sockets from MQL5
- Sending or reading byte arrays from external services
- Polling for socket readiness or connection state
- Configuring send and receive timeouts for socket objects
- Using terminal-managed mail, FTP, or push notifications

**Do NOT use** for:
- File I/O -> use `stdlib-utilities`
- Database access -> use `stdlib-utilities`
- EA architecture -> use `ea-architect`

---

## NET-1: Socket Lifecycle, Timeouts, and Plain-TCP I/O

| Function | Purpose | Usage note |
|----------|---------|------------|
| `SocketCreate(flags)` | Creates a socket handle | Currently uses `SOCKET_DEFAULT`; returns `INVALID_HANDLE` on failure |
| `SocketConnect(socket, address, port, timeout)` | Connects the socket to a remote host | Use after creation and before any send/read operations |
| `SocketTimeouts(socket, send_ms, receive_ms)` | Sets OS-level send and receive timeouts | Persistent socket-object timeouts, separate from per-call timeout in `SocketRead()` |
| `SocketIsConnected(socket)` | Checks whether the socket remains connected | Use to guard long-lived sessions or reconnect logic |
| `SocketIsReadable(socket)` | Checks whether socket data is ready to read | Pair with non-blocking poll loops before `SocketRead()` |
| `SocketIsWritable(socket)` | Checks whether the socket can send more data | Useful in paced send loops or after partial writes |
| `SocketRead(socket, buffer, expected, timeout)` | Reads bytes from a plain socket | Per-call timeout is distinct from `SocketTimeouts()` |
| `SocketSend(socket, buffer, size)` | Sends bytes through a plain socket | Treat short writes or failures as transport-state problems |
| `SocketClose(socket)` | Closes the socket handle and frees resources | Always close handles explicitly; one program can only hold 128 sockets |

### Socket rules that matter

- Socket functions only work in Expert Advisors and scripts; calling them from
  indicators raises error `4014`
- One MQL5 program can open at most 128 sockets; exceeding that limit raises
  `ERR_NETSOCKET_TOO_MANY_OPENED`
- `SocketTimeouts()` configures the underlying socket object once, while
  `SocketRead()` also accepts an operation-specific timeout
- Invalid socket handles trigger `ERR_NETSOCKET_INVALIDHANDLE`

---

## NET-2: WebRequest, TLS Sockets, and Terminal-Mediated Sends

| Function | Purpose | Usage note |
|----------|---------|------------|
| `WebRequest()` | Sends synchronous HTTP requests | Requires URL whitelisted in terminal options; cannot run in Strategy Tester |
| `SocketTlsHandshake(socket, host)` | Starts TLS over an existing connected socket | Must complete before TLS read/send calls |
| `SocketTlsCertificate(socket)` | Retrieves peer-certificate information | Use for connection inspection or validation logging |
| `SocketTlsRead(socket, buffer, expected)` | Reads bytes from an established TLS session | Use only after handshake succeeds |
| `SocketTlsReadAvailable(socket)` | Checks how much TLS data is ready | Helpful for staged read loops or message framing |
| `SocketTlsSend(socket, buffer, size)` | Sends bytes over a TLS socket | Requires a live TLS session, not just a connected plain socket |
| `SendMail(subject, body)` | Sends terminal-configured email notifications | Terminal-side mail settings must already be configured |
| `SendFTP(path, data)` | Uploads data using terminal FTP settings | Treat as a terminal service, not a generic network stack replacement |
| `SendNotification(text)` | Sends a push notification | Also unavailable in the Strategy Tester |

### High-value gotchas

- `WebRequest()` is synchronous and blocks the calling thread; indicators are
  forbidden from using it
- Allowed URLs for `WebRequest()` are terminal configuration, not runtime code
- Tester runs cannot execute `WebRequest()` or terminal notification channels
- TLS calls build on a connected socket; do not skip the plain-socket creation
  and connection steps

---

## References

- `docs/mql5_com_-_docs/network.md`
- `docs/mql5_com_-_docs/network-socketcreate.md`
- `docs/mql5_com_-_docs/network-socketconnect.md`
- `docs/mql5_com_-_docs/network-socketclose.md`
- `docs/mql5_com_-_docs/network-socketisconnected.md`
- `docs/mql5_com_-_docs/network-socketisreadable.md`
- `docs/mql5_com_-_docs/network-socketiswritable.md`
- `docs/mql5_com_-_docs/network-socketread.md`
- `docs/mql5_com_-_docs/network-socketsend.md`
- `docs/mql5_com_-_docs/network-sockettimeouts.md`
- `docs/mql5_com_-_docs/network-sockettlshandshake.md`
- `docs/mql5_com_-_docs/network-sockettlscertificate.md`
- `docs/mql5_com_-_docs/network-sockettlsread.md`
- `docs/mql5_com_-_docs/network-sockettlsreadavailable.md`
- `docs/mql5_com_-_docs/network-sockettlssend.md`
- `docs/mql5_com_-_docs/network-webrequest.md`
- `docs/mql5_com_-_docs/network-sendmail.md`
- `docs/mql5_com_-_docs/network-sendftp.md`
- `docs/mql5_com_-_docs/network-sendnotification.md`
