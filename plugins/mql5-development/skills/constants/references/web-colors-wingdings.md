# Web Colors and Wingdings Reference

## Web Colors

140+ named `color` constants (full table in source file below).
Usage: pass any `clrXxx` constant to color properties via `ObjectSetInteger(chart_id, name, OBJPROP_COLOR, clrRed)`.
Common values: `clrRed`, `clrGreen`, `clrBlue`, `clrYellow`, `clrWhite`, `clrBlack`, `clrNONE` (0 = transparent).

> Full table: `docs/mql5_com_-_docs/constants-objectconstants-webcolors.md`

## Wingdings Character Codes

250+ Wingdings character codes for `OBJ_ARROW` (full table in source file below).
Usage: `ObjectSetInteger(chart_id, name, OBJPROP_ARROWCODE, code)` — e.g. code 241 = up arrow.
Only applies to `OBJ_ARROW` objects; ignored on all other object types.

> Full table: `docs/mql5_com_-_docs/constants-objectconstants-wingdings.md`
