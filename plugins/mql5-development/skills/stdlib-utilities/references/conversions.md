# Conversions — Numeric, Text, Color, Time, and Struct Serialization

## Numeric and Text Conversions

> Canonical MQL5 reference: [DoubleToString](https://www.mql5.com/en/docs/convert/doubletostring) · [IntegerToString](https://www.mql5.com/en/docs/convert/integertostring) · [ShortToString](https://www.mql5.com/en/docs/convert/shorttostring) · [CharToString](https://www.mql5.com/en/docs/convert/chartostring)

| Function group | What it covers | Usage note |
|----------------|----------------|------------|
| `DoubleToString`, `IntegerToString`, `ShortToString`, `CharToString` | Primitive-to-string rendering | Use when logs or exported values need explicit formatting control |
| `StringToDouble`, `StringToInteger`, `StringToCharArray`, `CharArrayToString` | Text-to-value and buffer conversion | Treat text parsing as a validation boundary for external input |
| `NormalizeDouble`, `StringFormat`, `EnumToString` | Formatting and stable presentation | `StringFormat` is the main structured logging helper |

## Colors, Time Rendering, and Struct Serialization

> Canonical MQL5 reference: [ColorToString](https://www.mql5.com/en/docs/convert/colortostring) · [ColorToARGB](https://www.mql5.com/en/docs/convert/colortoargb) · [StringToColor](https://www.mql5.com/en/docs/convert/stringtocolor) · [StringToTime](https://www.mql5.com/en/docs/convert/stringtotime)

| Function group | What it covers | Usage note |
|----------------|----------------|------------|
| `ColorToString`, `ColorToARGB`, `StringToColor` | Colour conversion paths | Use when bridging terminal colour values with text config or serialized payloads |
| `StringToTime`, `TimeToString` | Human-readable time conversion | Be explicit about expected format and timezone assumptions around the converted value |
| `StructToCharArray`, `CharArrayToStruct` | Struct serialisation | Use only when both ends agree on layout and field ordering |
