# Platform Internals — Files, Folders, Logs, Task Manager, Updates

## File & Folder Structure

### Read-Only Files (Installation Directory)

Located in `/Program Files/platform folder/`:
- `terminal.exe` — main executable
- `Sounds/*.wav` — standard audio files

### User Data (Data Directory)

Main mode: `<AppData>/MetaQuotes/Terminal/<instance_id>/`

```
<instance_id>/
├── Bases/
│   └── <ServerName>/
│       ├── alerts/                    # Alert database
│       ├── favorites/                 # Navigator favorites
│       ├── hotkeys/                   # Keyboard shortcut database
│       ├── news.dat                   # Newsletter database
│       ├── request-queues/            # Open request queue windows
│       ├── selected-xxxxx.dat         # Symbols in Market Watch
│       └── symbols-xxxxx.dat          # All available symbols on server
├── Config/
│   ├── certificates/                  # *.pfx SSL certificate files
│   ├── accounts.dat                   # Account list + settings (encrypted)
│   ├── common.ini                     # Platform interface settings, last-used values
│   ├── interface.dat                  # UI settings, window positions, indicators
│   ├── servers.dat                    # Trade server connection settings (encrypted)
│   └── <server>.srv                   # Per-server connection settings (encrypted)
├── crash/                             # Crash dump files (auto-sent to MetaQuotes)
│   └── yyyymmdd_hhmmss.dmp
├── Logs/
│   └── YYYYMMDD.LOG                   # Platform journal logs (one file per day)
├── MQL5/
│   ├── Experts/                       # EA .ex5 compiled + .mq5 source files
│   ├── Files/                         # EA runtime read/write sandbox (only writable dir)
│   ├── Images/                        # *.bmp image files
│   ├── Include/                       # *.mqh shared include files
│   ├── Indicators/                    # Custom indicator files
│   ├── Libraries/                     # *.ex5 library files
│   ├── Logs/
│   │   └── YYYYMMDD.LOG              # Expert Advisor journal logs
│   ├── Presets/                       # *.set EA parameter files
│   ├── Profiles/
│   │   ├── Charts/
│   │   │   ├── Default/               # Default chart templates (*.chr + order.wnd)
│   │   │   └── <ProfileName>/         # Named profile subdirs
│   │   └── Templates/                 # Chart templates
│   └── Scripts/                       # Script files
└── Profiles/
    ├── Charts/
    │   ├── Default/                   # Default profile (chart + order.wnd)
    │   └── <ProfileName>/             # Custom profiles
    ├── Deleted/                       # Templates of deleted charts (for re-opening)
    └── Tester/                        # Last-used *.set files per EA
```

Key facts:
- `Files/` is the only directory EAs/scripts can read/write to at runtime (sandboxed)
- Log files named `YYYYMMDD.LOG` by date; one per day of operation
- `.ex5` = compiled; `.mq5` = source code

---

## Platform Logs

Two types of logs:
1. **Platform Journal** — stored in `Logs/` directory (platform events)
2. **Expert Journal** — stored in `MQL5/Logs/` directory (EA/script events)

### Log Entry Fields

| Field | Description |
|-------|-------------|
| Time | Date/time per user's local timezone |
| Source | Component that generated the entry (e.g. "LiveUpdate", EA name) |
| Message | Event description |

### Event Types (Icons)
- Error messages
- Informational messages
- Warning messages

### Journal Commands

| Command | Action |
|---------|--------|
| Open | Open log folder + save current entries to file |
| Send | Send log to admin via internal mail |
| Alerts | Open EA alert window (Experts journal only) |
| Viewer | Open log viewer program |
| Clear | Remove entries from tab (files remain on disk) |
| Auto Scroll | Auto-scroll to latest entry |
| Auto Arrange | Auto-size columns on window resize |
| Grid | Toggle table grid lines |

### Log Viewer

- Search: exact word match, case sensitive
- Filter: Full / No connection / Errors only
- Time range filter available
- `F3` = find next

---

## Task Manager

Open with `Ctrl+T` or Tools menu. Monitor platform resource consumption.

### Thread Types

| Thread | Purpose |
|--------|---------|
| Summary | Aggregate stats for all threads |
| GUI | Main platform UI thread |
| Experts/Scripts | Per-EA resource usage (shows debug/profile mode) |
| Symbol | Per-instrument calculations (prices, profits, charts, indicators) |
| Worker | Background/service threads |
| Thread Pool | OS-managed thread pool |
| System | OS + third-party DLL resources |

### Metrics

| Metric | Description |
|--------|-------------|
| CPU % | Processor load by this thread |
| Cycles | Computational cycles per second |
| Context Switches | Thread switches (>1000/sec may indicate thread contention) |
| Stack (KB) | Used/allocated stack memory |
| Kernel Time | Time in kernel mode (high = driver/hardware issues) |
| User Time | Time in user mode |
| Thread ID | Thread identifier |

### Header Stats

- Thread count
- Handle count (resource pointers)
- RAM consumed

### Managing MQL5 Programs

- **Show** — navigate to program in Navigator
- **Properties** — open input parameters
- **Remove** — remove from chart

---

## Live Update System

Automatic, cannot be disabled. Checks for updates on every server connection.

### Process

1. Platform connects to trade server
2. Checks for component updates
3. Downloads in background to:
   `C:\Users\<username>\AppData\Roaming\MetaQuotes\WebInstall`
4. Shared across all platform instances (no re-download)
5. Dialog prompts to install or defer ("Later" = installs on next start)
6. Update log source column: `LiveUpdate`

### Failure Handling

- Retries after 1 hour on failure
- Only downloads missing data on retry

### UAC Considerations

- If UAC enabled: confirmation dialog appears
- Admin: approve the operation
- Non-admin: enter admin credentials

### Manual Updates

- Help → Check Desktop Updates
- Documentation manuals can be updated separately

---

## References

- `docs/metatrader5_com_-_terminal_help_startworking_start_advanced/07_structure.md`
- `docs/metatrader5_com_-_terminal_help_startworking_start_advanced/11_autoupdate.md`
- `docs/metatrader5_com_-_terminal_help_startworking_start_advanced/12_journal.md`
- `docs/metatrader5_com_-_terminal_help_startworking_start_advanced/13_task_manager.md`
