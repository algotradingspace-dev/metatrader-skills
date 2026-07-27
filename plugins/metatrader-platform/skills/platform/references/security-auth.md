# Security & Authentication

## Security Overview

MetaTrader 5 employs multiple layers of security:

| Layer | Description |
|-------|-------------|
| **Data Encryption** | All client-server traffic compressed and encrypted with 128-bit keys |
| **Extended Authentication** | Optional SSL certificate-based auth (in addition to password) |
| **Server Authentication** | Platform verifies the trade server's identity (mutual) |
| **Config File Protection** | Config files encrypted; copying from another platform's `/Config` folder won't work |
| **Password Field Protection** | Input fields protected against screen-reading/keylogging tools |
| **Database Encryption** | Mail, trade, and symbol databases encrypted; auto-deleted if moved to another platform |

---

## Extended Authentication (SSL Certificates)

Enabled server-side. Standard password auth remains active alongside certificates.

### How It Works

1. Server generates a certificate signed with its private key (prevents forgery)
2. Platform prompts user to set a certificate password
3. Certificate saved as `.pfx` file in `/platform_folder/config/certificates/`
4. File named: `<account_number>_<company_id>_<client_name>.pfx`

### Certificate Password Requirements

- Minimum 5 characters
- Must contain at least 2 character types: lowercase, uppercase, digits
- Certificate cannot be used without password
- Never required for investor (read-only) password

### Storage Options

- **File-based:** `.pfx` in `config/certificates/` folder
- **Windows Certificate Store:** Auto-install via "Add the certificate to the Windows storage" option
  - If using system store, the `.pfx` file on disk can be deleted
  - Platform checks system store first, then disk folder

### Certificate Transfer

To use the same account on another machine:
1. Export the `.pfx` file from the certificates folder
2. Transfer securely to the new machine
3. Import into the new platform's certificates folder or Windows store

---

## 2FA / TOTP (One-Time Passwords)

Server must enable OTP support. Can be optional or mandatory per broker/regulation.
OTPs are valid for **30 seconds**, then auto-regenerate.

### Desktop Setup

1. Open Authenticator app on mobile device
2. Tap "+" to add account
3. Scan QR code displayed in the MT5 platform
4. Enter the received code in the "One-Time Password" field
5. Click "Enable 2FA"

### Mobile Setup (iPhone)

1. Settings → OTP (first access requires setting 4-digit PIN)
2. Select "Bind to account"
3. Enter: server name, account number, master password
4. Keep "Bind" enabled → tap "Bind" button
5. OTP shown at top of OTP section with blue lifetime bar

Extras:
- **Change Password** — change the generator PIN
- **Synchronize Time** — sync device time with reference server (critical for OTP validity)
- Unlimited accounts can be bound

### Mobile Setup (Android)

1. Accounts → tap + icon (first access requires 4-digit PIN)
2. Enter: server name, account number, master password
3. Keep "Bind" enabled → tap "Bind"
4. OTP displayed at top with blue lifetime bar

### Compatible Authenticator Apps

- MetaTrader mobile app (iPhone / Android) — built-in OTP generator
- Google Authenticator
- Microsoft Authenticator
- LastPass Authenticator
- Authy

### Important Notes

- OTP required for **every** connection to the account
- Time synchronization between device and server is critical
- If transferring funds, the OTP of the source account is required
- To unbind: repeat the process with "Bind" toggle disabled
- OTP not required for investor (read-only) password connections

---

## Platform-Level Security Measures

- All data exchange: compressed + encrypted with 128-bit keys
- Server authentication is mutual (client proves identity; server also proves it is legitimate)
- Config files in `/Config/` are encrypted; cannot be copied to another platform instance
- All databases (mail, trade, symbol) are encrypted; auto-deleted if moved to a different platform
- Password fields protected from memory-scraping tools

---

## References

- `docs/metatrader5_com_-_terminal_help_startworking_start_advanced/05_extended_authorization.md`
- `docs/metatrader5_com_-_terminal_help_startworking_start_advanced/06_otp.md`
- `docs/metatrader5_com_-_terminal_help_startworking_start_advanced/10_security.md`
