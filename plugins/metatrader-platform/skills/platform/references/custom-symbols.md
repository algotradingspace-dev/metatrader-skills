# Custom Symbols — Create, Configure, and Feed Synthetic Market Data

Custom-symbol functions are the platform-facing workflow for creating
synthetic symbols, editing their trading/session properties, and feeding
bars, ticks, or DOM snapshots into terminal-visible history. Treat this
as platform infrastructure: it defines what the terminal can display and
test, not a signal or trade decision framework.

---

## Custom-Symbol Lifecycle

> Canonical MQL5 reference: [CustomSymbolCreate](https://www.mql5.com/en/docs/customsymbols/customsymbolcreate) · [CustomSymbolSetInteger](https://www.mql5.com/en/docs/customsymbols/customsymbolsetinteger) · [CustomRatesUpdate](https://www.mql5.com/en/docs/customsymbols/customratesupdate) · [CustomRatesReplace](https://www.mql5.com/en/docs/customsymbols/customratesreplace)

| Topic | Practical rule |
|-------|----------------|
| Creation | `CustomSymbolCreate()` creates a symbol under the Custom tree and can clone a broker symbol as the initial property baseline |
| Property setup | `CustomSymbolSetInteger/Double/String()` plus margin/session setters define precision, quotes, sessions, and trade behaviour |
| Bar history | `CustomRatesUpdate()` merges bars, while `CustomRatesReplace()` and `CustomRatesDelete()` rewrite or purge intervals |
| Tick history | `CustomTicksAdd()` requires Market Watch selection; replace/delete variants are for full interval maintenance |
| DOM | `CustomBookAdd()` supplies a fresh market-depth snapshot subject to symbol book-depth limits |
| Removal | `CustomSymbolDelete()` removes the symbol and its custom history from the terminal |

---

## Operational Gotchas

- Custom symbol names and paths have strict length and character rules;
  duplicate names fail with custom-symbol errors
- M1 bars are the canonical stored rate granularity, so higher-timeframe
  history is derived by the terminal
- Tick ingestion and DOM updates are terminal-state operations, so symbol
  visibility and subscription state matter
- Session quote and session trade setters are weekday-specific; misconfigured
  sessions can make a synthetic symbol look available but non-tradable

---

## References

- `docs/mql5_com_-_docs/customsymbols.md`
- `docs/mql5_com_-_docs/customsymbols-custombookadd.md`
- `docs/mql5_com_-_docs/customsymbols-customratesdelete.md`
- `docs/mql5_com_-_docs/customsymbols-customratesreplace.md`
- `docs/mql5_com_-_docs/customsymbols-customratesupdate.md`
- `docs/mql5_com_-_docs/customsymbols-customsymbolcreate.md`
- `docs/mql5_com_-_docs/customsymbols-customsymboldelete.md`
- `docs/mql5_com_-_docs/customsymbols-customsymbolsetdouble.md`
- `docs/mql5_com_-_docs/customsymbols-customsymbolsetinteger.md`
- `docs/mql5_com_-_docs/customsymbols-customsymbolsetmarginrate.md`
- `docs/mql5_com_-_docs/customsymbols-customsymbolsetsessionquote.md`
- `docs/mql5_com_-_docs/customsymbols-customsymbolsetsessiontrade.md`
- `docs/mql5_com_-_docs/customsymbols-customsymbolsetstring.md`
- `docs/mql5_com_-_docs/customsymbols-customticksadd.md`
- `docs/mql5_com_-_docs/customsymbols-customticksdelete.md`
- `docs/mql5_com_-_docs/customsymbols-customticksreplace.md`
