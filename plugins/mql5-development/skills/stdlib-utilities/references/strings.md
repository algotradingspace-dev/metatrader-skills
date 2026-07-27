# Strings — Construction, Search, Replace, Split, and Trim

## String Construction and Character Access

| Function group | What it covers | Usage note |
|----------------|----------------|------------|
| `StringAdd`, `StringConcatenate`, `StringInit`, `StringFill` | Building or padding strings | Use for deterministic message construction and fixed-width formatting |
| `StringLen`, `StringBufferLen`, `StringReserve`, `StringSetLength` | Length and capacity management | Reserve capacity when repeated concatenation would otherwise churn allocations |
| `StringGetCharacter`, `StringSetCharacter`, `StringSubstr` | Character-level and substring access | Indexing is zero-based |
| `StringCompare`, `StringToLower`, `StringToUpper` | Comparison and case normalisation | Normalise casing before symbolically comparing command tokens or config keys |

## Search, Replace, Split, and Trim

| Function group | What it covers | Usage note |
|----------------|----------------|------------|
| `StringFind` | Substring search | Returns a zero-based position or a not-found outcome you must handle explicitly |
| `StringReplace` | In-place replacement | Treat it as a mutating operation rather than a pure lookup |
| `StringSplit` | Tokenisation by separator | Watch for empty tokens when adjacent separators occur |
| `StringTrimLeft`, `StringTrimRight` | Whitespace cleanup | Useful before numeric conversion or command dispatch |
