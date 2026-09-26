# CExpertMoney — Sizing, Reverse Volume Policy, and Risk Percent Input

**Source family:** `standardlibrary-expertclasses-expertbaseclasses-cexpertmoney*.md`

`CExpertMoney` is the sizing-policy surface that the owning `CExpert` asks
for lot sizes and close decisions. Derived money-management classes decide
how large to open, how large to reverse, and whether the current position
should be closed under the selected risk policy.

> Canonical MQL5 reference: [ValidationSettings](https://www.mql5.com/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpert/cexpertvalidationsettings) · [CheckOpenLong](https://www.mql5.com/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpert/cexpertcheckopenlong) · [CheckOpenShort](https://www.mql5.com/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpert/cexpertcheckopenshort) · [CheckReverse](https://www.mql5.com/en/docs/standardlibrary/expertclasses/expertbaseclasses/cexpert/cexpertcheckreverse)

| Method | Return type | Purpose | Usage note |
|--------|------------|---------|------------|
| `Percent` | `void` | Sets the value of "Risk percent" parameter | Configure the risk budget before asking for any trade volume |
| `ValidationSettings` | `bool` | Checks the settings | Fail setup if the money-management inputs are inconsistent |
| `CheckOpenLong` | `double` | Gets the volume for a long position | Return the lot size to use for the next long entry |
| `CheckOpenShort` | `double` | Gets the volume for a short position | Return the lot size to use for the next short entry |
| `CheckReverse` | `double` | Gets the volume for reverse of the position | Return the volume policy to use when flipping the current position |
| `CheckClose` | `double` | Checks conditions to close the opened position | Use when the money model can veto or size the close-side action |

---

## References

- `docs/mql5_com_-_docs/standardlibrary-expertclasses-expertbaseclasses-cexpertmoney*.md`
