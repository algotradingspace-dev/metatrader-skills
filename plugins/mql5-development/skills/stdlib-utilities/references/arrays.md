# Arrays — Sizing, Initialization, Copying, Search, Sort, and Extrema

## Array Sizing, Initialization, Copying, and Series Direction

| Function group | What it covers | Usage note |
|----------------|----------------|------------|
| `ArraySize`, `ArrayResize`, `ArrayFree` | Dynamic-array capacity management | Only dynamic arrays can be resized directly |
| `ArrayInitialize`, `ArrayFill`, `ArrayCopy` | Bulk initialisation and duplication | Useful for deterministic resets before a new calculation pass |
| `ArraySetAsSeries`, `ArrayGetAsSeries`, `ArrayIsSeries`, `ArrayIsDynamic` | Array semantics and orientation | Use these deliberately whenever bar-index meaning matters |
| `ArrayPrint`, `ArrayReverse` | Diagnostics and order manipulation | `ArrayPrint` is for journal inspection, not program output channels |

## Search, Sort, Extrema, and Compact Storage

| Function group | What it covers | Usage note |
|----------------|----------------|------------|
| `ArrayBsearch`, `ArraySort`, `ArrayCompare` | Search and ordering | Binary search assumes the array is already sorted |
| `ArrayMaximum`, `ArrayMinimum`, `ArrayRange` | Extrema and spread inspection | Useful for scan-based signal filters and quick diagnostics |
| `ArrayInsert`, `ArrayRemove` | Structural edits | These change element positions and should be treated as stateful mutations |
| `ArrayToFP16`, `ArrayFromFP16`, `ArrayToFP8`, `ArrayFromFP8` | Compact-storage conversion | Reserve these for storage or transport optimisation, not precision-critical calculations |
