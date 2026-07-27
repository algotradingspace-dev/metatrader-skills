# File I/O Constants

## File Opening Flags (bitmask — combine with `|`)

| Identifier | Value | Description |
|------------|-------|-------------|
| `FILE_READ` | 1 | Open for reading |
| `FILE_WRITE` | 2 | Open for writing |
| `FILE_BIN` | 4 | Binary mode (no string conversion) |
| `FILE_CSV` | 8 | CSV mode (elements separated by delimiter) |
| `FILE_TXT` | 16 | Plain text (CSV without delimiter handling) |
| `FILE_ANSI` | 32 | ANSI strings (1 byte/char) |
| `FILE_UNICODE` | 64 | Unicode strings (2 bytes/char) — default if neither specified |
| `FILE_SHARE_READ` | 128 | Shared read from multiple programs |
| `FILE_SHARE_WRITE` | 256 | Shared write from multiple programs |
| `FILE_REWRITE` | 512 | Allow `FileCopy()`/`FileMove()` rewrite |
| `FILE_COMMON` | 4096 | Path in `\Terminal\Common\Files` shared folder |

Priority: `FILE_CSV` > `FILE_BIN` > `FILE_TXT`; `FILE_UNICODE` > `FILE_ANSI`.

## ENUM_FILE_POSITION — `FileSeek(handle, offset, origin)`

| Identifier | Description |
|------------|-------------|
| `SEEK_SET` | From file beginning |
| `SEEK_CUR` | From current pointer position |
| `SEEK_END` | From file end |

## ENUM_FILE_PROPERTY_INTEGER — `FileGetInteger(handle, prop)`

| Identifier | Description |
|------------|-------------|
| `FILE_EXISTS` | Check existence |
| `FILE_CREATE_DATE` | Creation date |
| `FILE_MODIFY_DATE` | Last modification date |
| `FILE_ACCESS_DATE` | Last access date |
| `FILE_SIZE` | Size in bytes |
| `FILE_POSITION` | Current pointer position |
| `FILE_END` | End-of-file flag |
| `FILE_LINE_END` | End-of-line flag |
| `FILE_IS_COMMON` | Opened in shared folder |
| `FILE_IS_TEXT` | Opened as text |
| `FILE_IS_BINARY` | Opened as binary |
| `FILE_IS_CSV` | Opened as CSV |
| `FILE_IS_ANSI` | Opened as ANSI |
| `FILE_IS_READABLE` | Readable flag |
| `FILE_IS_WRITABLE` | Writable flag |

> When calling by file name (not handle), only `FILE_EXISTS`, `FILE_CREATE_DATE`, `FILE_MODIFY_DATE`, `FILE_ACCESS_DATE`, `FILE_SIZE` are available.

## Codepage Constants — `FileOpen()`, `CharArrayToString()`, `StringToCharArray()`

| Constant | Value | Description |
|----------|-------|-------------|
| `CP_ACP` | 0 | Current Windows ANSI code page (default) |
| `CP_OEMCP` | 1 | Current OEM code page |
| `CP_MACCP` | 2 | Macintosh code page (legacy) |
| `CP_THREAD_ACP` | 3 | ANSI code page for current thread |
| `CP_SYMBOL` | 42 | Symbol code page |
| `CP_UTF7` | 65000 | UTF-7 |
| `CP_UTF8` | 65001 | UTF-8 |

## MessageBox Return Codes — `MessageBox()` return value

| Constant | Value | Button pressed |
|----------|-------|----------------|
| `IDOK` | 1 | OK |
| `IDCANCEL` | 2 | Cancel |
| `IDABORT` | 3 | Abort |
| `IDRETRY` | 4 | Retry |
| `IDIGNORE` | 5 | Ignore |
| `IDYES` | 6 | Yes |
| `IDNO` | 7 | No |
| `IDTRYAGAIN` | 10 | Try Again |
| `IDCONTINUE` | 11 | Continue |

## MessageBox Type Flags (bitmask) — `MessageBox(text, caption, flags)`

| Constant | Value | Buttons shown |
|----------|-------|---------------|
| `MB_OK` | 0x00 | OK (default) |
| `MB_OKCANCEL` | 0x01 | OK, Cancel |
| `MB_ABORTRETRYIGNORE` | 0x02 | Abort, Retry, Ignore |
| `MB_YESNOCANCEL` | 0x03 | Yes, No, Cancel |
| `MB_YESNO` | 0x04 | Yes, No |
| `MB_RETRYCANCEL` | 0x05 | Retry, Cancel |
| `MB_CANCELTRYCONTINUE` | 0x06 | Cancel, Try Again, Continue |
