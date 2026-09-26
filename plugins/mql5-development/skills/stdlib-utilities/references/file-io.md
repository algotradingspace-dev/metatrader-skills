# File I/O — Sandbox, Open Modes, Read/Write, Search, and Folder Maintenance

## File Sandbox Rules

MQL5 file operations are sandboxed to the terminal data folder or the shared
common-files folder.

- File operations cannot escape the MQL5 sandbox
- Pick the open flags deliberately: text/CSV vs binary changes which read/write
  helpers are valid
- Named pipes also flow through `FileOpen()`, so handle discipline matters even
  when the target is not a normal file

## File Handle Lifecycle

> Canonical MQL5 reference: [FileOpen](https://www.mql5.com/en/docs/files/fileopen) · [FileClose](https://www.mql5.com/en/docs/files/fileclose) · [FileGetInteger](https://www.mql5.com/en/docs/files/filegetinteger) · [FileSize](https://www.mql5.com/en/docs/files/filesize)

| Function group | What it covers | Usage note |
|----------------|----------------|------------|
| `FileOpen`, `FileClose` | File-handle lifecycle | Opening a file for writing also creates missing subfolders in the specified sandbox path |
| `FileGetInteger`, `FileSize`, `FileTell`, `FileSeek` | File metadata and pointer movement | Use these to inspect encoding, size, current offset, and reposition the cursor safely |
| `FileIsExist`, `FileIsEnding`, `FileIsLineEnding` | Existence and end-of-file checks | Prefer these checks before assuming a read loop can continue |
| `TerminalInfoString(TERMINAL_DATA_PATH / TERMINAL_COMMONDATA_PATH)` | Resolve the actual sandbox roots | Use when you need to coordinate terminal-local and common-file locations |

## Text, Binary, Array, and Struct Read/Write

> Canonical MQL5 reference: [FileReadBool](https://www.mql5.com/en/docs/files/filereadbool) · [FileReadDatetime](https://www.mql5.com/en/docs/files/filereaddatetime) · [FileReadNumber](https://www.mql5.com/en/docs/files/filereadnumber) · [FileReadString](https://www.mql5.com/en/docs/files/filereadstring)

| Function group | What it covers | Usage note |
|----------------|----------------|------------|
| `FileReadBool`, `FileReadDatetime`, `FileReadNumber`, `FileReadString` | CSV/TXT parsing helpers | These parse delimited text rather than raw binary bytes |
| `FileReadDouble`, `FileReadFloat`, `FileReadInteger`, `FileReadLong`, `FileReadArray`, `FileReadStruct` | Binary reads | Use only when the file format actually matches the target primitive or structure layout |
| `FileWrite`, `FileWriteString`, `FileWriteDouble`, `FileWriteFloat`, `FileWriteInteger`, `FileWriteLong`, `FileWriteArray`, `FileWriteStruct` | Text and binary writes | Pair with the matching file mode and flush before you depend on persistence mid-run |
| `FileFlush`, `FileLoad`, `FileSave` | Buffer persistence and bulk transfers | `FileLoad`/`FileSave` are the shortest path for whole-array binary transfer |

**Serialization gotchas:**
- Struct read/write is only safe when the binary layout matches exactly
- Text helpers convert strings into typed values; malformed CSV content becomes
  data-quality risk, not just I/O risk
- Bound array size and file mode determine whether bulk operations succeed cleanly

## Search, Copy, Move, and Folder Maintenance

> Canonical MQL5 reference: [FileFindFirst](https://www.mql5.com/en/docs/files/filefindfirst) · [FileFindNext](https://www.mql5.com/en/docs/files/filefindnext) · [FileFindClose](https://www.mql5.com/en/docs/files/filefindclose) · [FileCopy](https://www.mql5.com/en/docs/files/filecopy)

| Function group | What it covers | Usage note |
|----------------|----------------|------------|
| `FileFindFirst`, `FileFindNext`, `FileFindClose` | Enumerating files by filter | Always close the search handle after iteration completes |
| `FileCopy`, `FileMove`, `FileDelete` | File maintenance | Use for rename, duplication, or cleanup inside allowed folders |
| `FolderCreate`, `FolderDelete`, `FolderClean` | Folder lifecycle | `FolderDelete` requires the folder to be empty; `FolderClean` is the bulk cleanup helper |
| `FileSelectDialog` | User file/folder selection dialog | This is an interactive utility path, not a background automation primitive |
