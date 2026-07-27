# Platform Setup — Installation, Startup & Uninstallation

## Windows Installation

Download `mt5setup.exe` (web installer — components downloaded during install).

**Requirements:**
- Windows 2008/7/8/10/11
- CPU with SSE2 support (Pentium 4 / Athlon 64+)

**Installation options (`Settings` button):**
- Custom installation folder via path or `Browse`
- Can install over existing platform (preserves settings, resets default profiles/templates and MQL5 programs)
- Multiple accounts → install separate platforms in different directories

**Silent/automatic install:**
```
mt5setup.exe /auto /path:"C:\Program Files\MyFolder"
```

**Beta install:**
```
mt5setup.exe /beta
```
Or from installed platform: `Help → Check Desktop Updates → Latest Beta Version`

---

## macOS Installation

Native installer using Wine under the hood. Fully automated: detects system,
downloads Wine, configures, installs MT5.

**Requirements:** macOS Catalina 10.15.7+ — supports Apple Silicon M1 and later

**Check Wine version** (visible in platform log on startup):
```
Terminal Windows 10 build 18362 on Wine 8.0.1
```

If upgrading, delete these folders first:
```
~/Library/Application Support/Metatrader 5
~/Library/Application Support/net.metaquotes.wine.metatrader5
```

**Data directory:**
```
~/Library/Application Support/net.metaquotes.wine.metatrader5/drive_c/Program Files/MetaTrader 5
```

To fully reset: delete both folders above.

**Language:** Set macOS language before installation; Wine picks up the current locale.

---

## Linux Installation

Uses Wine compatibility layer. Supports Ubuntu, Debian, Linux Mint, Fedora.

**One-command install** (no sudo):
```bash
wget <official-mt5-linux-installer-url>
chmod +x mt5linux.sh && ./mt5linux.sh
```
Replaced `<official-mt5-linux-installer-url>` with the current MetaQuotes
Linux installer URL from `metaquotes.net` or your broker's MT5 download page.

Script auto-detects distro, installs appropriate Wine, then launches MT5
installer. Accept Mono/Gecko packages when prompted. Restart OS after install.

**Keep Wine updated:**
```bash
sudo apt update && sudo apt upgrade
```

**Data directory:**
```
~/.mt5/drive_c/Program Files/MetaTrader 5
```

---

## Platform Start Modes

### Main Mode (default when installed to Program Files with UAC enabled)

Modifiable data stored separately from read-only program files.

**Data location:**
- Windows: `C:\Users\<username>\AppData\Roaming\MetaQuotes\Terminal\<instance_id>\`
- Windows XP: `C:\Documents and Settings\<username>\Application Data\MetaQuotes\Terminal\<instance_id>\`
- macOS: `~/Library/Application Support/net.metaquotes.wine.metatrader5/drive_c/Program Files/MetaTrader 5`
- Linux: `~/.mt5/drive_c/Program Files/MetaTrader 5`

`instance_id` = unique ID generated from installation path.

Activated when:
- Platform installed in Program Files
- UAC enabled
- Remote Desktop (RDP) connection

### Portable Mode

Forces data storage in the installation folder:
```
terminal.exe /portable
```

Requirements:
- If in Program Files: admin rights + UAC disabled
- If elsewhere: write permission to that folder

### Command-Line Switches

| Switch | Purpose |
|--------|---------|
| `/login:<account>` | Start with specific account pre-selected |
| `/config:<path>` | Use alternative config file (default: `common.ini`) |
| `/portable` | Run in portable mode (data inside installation folder) |
| `mt5setup.exe /auto /path:"<dir>"` | Silent install to custom path |
| `mt5setup.exe /beta` | Install/update to beta build |

Two copies cannot run from the same directory. Install multiple platforms in
separate folders for parallel instances.

---

## Uninstallation

Standard Windows uninstaller. **Warning:** deleting user data is irreversible —
no recovery after removal.

---

## References

- `docs/metatrader5_com_-_terminal_help_startworking_start_advanced/01_installation.md`
- `docs/metatrader5_com_-_terminal_help_startworking_start_advanced/02_install_mac.md`
- `docs/metatrader5_com_-_terminal_help_startworking_start_advanced/03_install_linux.md`
- `docs/metatrader5_com_-_terminal_help_startworking_start_advanced/04_start.md`
- `docs/metatrader5_com_-_terminal_help_startworking_start_advanced/15_deinstallation.md`
