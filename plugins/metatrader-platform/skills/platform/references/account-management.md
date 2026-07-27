# Account Management & Mailbox

## Account Types

| Type | Notes |
|------|-------|
| Demo | Unlimited accounts, opened from within platform |
| Live | Opened by brokerage company only (not from platform) |

Accounts grouped by server name in the Navigator window. Expired demo accounts:
platform auto-creates replacement on same server (if broker permits).

---

## Switching Accounts

Double-click on account in Navigator (or select + Enter).

### Safety Settings

| Option | Purpose |
|--------|---------|
| Disable automated trading when switching accounts | Prevents accidental trades by running EAs on the wrong account |
| Keep personal settings and data at startup | When disabled, password must be entered manually every connection (more secure) |

---

## Account Operations

| Action | Method |
|--------|--------|
| Open demo account | Navigator context menu → "Open an Account" (or `Insert` key) |
| Connect | Double-click account, or select + Enter |
| Change password | Context menu → "Change Password" |
| Delete account | Context menu → "Delete" (or `Delete` key) |
| Add to Favorites | Context menu → "Add to Favorites" |
| Virtual hosting | Rent a server closest to broker for minimal network latency |

---

## Fund Transfers Between Accounts

Available for accounts on the same server only.

### Constraints

- Same trading server only
- Same account type only (live → live; demo → demo)
- Same deposit currency only
- Requires master password on **both** accounts
- If source account uses OTP/2FA: one-time password also required

### Process

1. Select target account in transfer dialog
2. Specify amount in deposit currency of current account
3. Amount cannot exceed current balance or free margin
4. Master password required for both accounts
5. OTP required on sending account if 2FA enabled

**Implementation:** Withdrawal operation on source account + deposit operation
on target account (balance operations).

---

## Mailbox (Internal Messaging)

### Attachment Limits

| Constraint | Limit |
|------------|-------|
| Single file size | 8 MB max |
| Total attachments size | 16 MB max |
| Number of files | 5 max |

---

## References

- `docs/metatrader5_com_-_terminal_help_startworking_start_advanced/08_account_manage.md`
- `docs/metatrader5_com_-_terminal_help_startworking_start_advanced/09_mail.md`
