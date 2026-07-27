# Conversions — Numeric, Text, Color, Time, and Struct Serialization

## Numeric and Text Conversions

| Function group | What it covers | Usage note |
|----------------|----------------|------------|
| `DoubleToString`, `IntegerToString`, `ShortToString`, `CharToString` | Primitive-to-string rendering | Use when logs or exported values need explicit formatting control |
| `StringToDouble`, `StringToInteger`, `StringToCharArray`, `CharArrayToString` | Text-to-value and buffer conversion | Treat text parsing as a validation boundary for external input |
| `NormalizeDouble`, `StringFormat`, `EnumToString` | Formatting and stable presentation | `StringFormat` is the main structured logging helper |

## Colors, Time Rendering, and Struct Serialization

| Function group | What it covers | Usage note |
|----------------|----------------|------------|
| `ColorToString`, `ColorToARGB`, `StringToColor` | Colour conversion paths | Use when bridging terminal colour values with text config or serialized payloads |
| `StringToTime`, `TimeToString` | Human-readable time conversion | Be explicit about expected format and timezone assumptions around the converted value |
| `StructToCharArray`, `CharArrayToStruct` | Struct serialisation | Use only when both ends agree on layout and field ordering |
