# Skill Authoring Standard

This document defines the contract for authoring and maintaining Claude Code
skills within the `metatrader-skills` plugin marketplace. Every skill in the
`skills/` directory of any plugin MUST conform to this standard.

---

## 1. Directory Layout

```
skills/<skill-name>/
  SKILL.md              # Required — the skill definition
  references/           # Optional — supporting reference docs
  scripts/              # Optional — reusable scripts/snippets
  assets/               # Optional — images, diagrams, templates
```

Each skill lives in its own directory under the plugin's `skills/` folder.
The directory name is the skill's canonical name.

---

## 2. SKILL.md YAML Frontmatter

Every `SKILL.md` MUST begin with YAML frontmatter containing exactly these
fields:

```yaml
---
name: <kebab-case-name>
description: >
  <Third-person statement of WHAT the skill does and WHEN it triggers.
  Include concrete trigger phrases. Maximum 500 characters.>
---
```

### Rules

- **name**: kebab-case, must match the parent directory name exactly.
- **description**: present tense, third person ("Use for", "Activates", "Handles").
  Must state the capability AND list at least 3 concrete trigger phrases.
  Examples: "Use for: computation...; Trigger: 'calculate', 'compute', 'solve'."
  Hard limit: 500 characters.

---

## 3. SKILL.md Body

Target length: **200–400 lines**. If the skill exceeds this, mandatory
sections MUST be extracted into `references/*.md` files and summaries
left in the main body.

### Required Sections

| Section | Purpose |
|---------|---------|
| **Purpose** | One-paragraph summary of the skill's domain and value. |
| **When to use / When NOT to use** | Clear inclusion and exclusion criteria. Prevents false activation. |
| **Core guidance** | The primary methodology, principles, patterns, and decision trees. |
| **Code patterns** | Concrete, compilable MQL5 (or Python, TypeScript) examples. |
| **Common mistakes** | Antipatterns, gotchas, and pitfalls specific to this domain. |
| **References** | Links to `references/*.md` files OR to authoritative docs (MQL5 docs, official sources). |

### Reference Skill Variant

Some skills are primarily **reference catalogs** — enum tables, API
signatures, configuration keys — where the body would consist of little
more than structured data. These MAY use the **Reference skill** variant.

#### Eligibility

A skill qualifies for the Reference variant ONLY if:
- Its primary function is lookup/retrieval of structured values
- It has no meaningful "Core guidance" or "Code patterns" to teach
- The SKILL.md body (excluding frontmatter) stays **under 100 lines**

#### Structure

```yaml
---
name: <kebab-case-name>
description: >
  <same 500-char rule>
  Must include the phrase "Reference skill" or "Reference" in the
  description so agents can distinguish behaviour from lookup.
---
```

The SKILL.md body MUST contain exactly these sections:

| Section | Required? |
|---------|-----------|
| **Purpose** | Yes |
| **When to use / When NOT to use** | Yes |
| **Core guidance** | No — replace with "This is a reference skill. Go to references/." |
| **Code patterns** | No — same replacement |
| **Common mistakes** | No — same replacement |
| **References** | Yes — MUST list every file in `references/` with one-line annotation |

The body acts as a **routing table**: each `references/*.md` file is
listed with a short description of what it contains and when an agent
should read it.

#### Example

```markdown
## References

| File | Contents | Read when |
|------|----------|-----------|
| `references/enum-trade.md` | All `ENUM_TRADE_REQUEST_ACTIONS`, `ENUM_ORDER_TYPE`, `ENUM_POSITION_TYPE` values with descriptions | Building or debugging order/position logic |
| `references/enum-symbol.md` | Symbol info integer/double/string property IDs | Accessing symbol properties via `SymbolInfoInteger` / `SymbolInfoDouble` |
| `references/return-codes.md` | `TRADE_RETCODE_*` values | Interpreting modified-trade responses |
```

#### Limits

- SKILL.md body: **under 100 lines** (including the routing table).
- If the reference tables themselves exceed 500 lines total across all
  `references/*.md`, the raw data MUST be compressed (e.g. grouped
  tables, abbreviated descriptions) until under that threshold.
- A Reference skill is NOT exempt from the Prohibited Content rules
  (Section 5), the Scrub Policy, or the Review Checklist.

#### When to prefer this variant

Use the Reference variant for skills like `mql5-constants`,
`mql5-economic-calendar`, or `mql5-network` — where the bulk of the
value is in lookup tables, not methodology. For any skill that teaches
a workflow, design pattern, or decision process, use the standard
200–400 line body instead.

---

### Optional Sections

- Quick reference / cheat-sheet tables (prefer in `references/`)
- Configuration reference
- Workflow diagrams (use Mermaid code blocks)
- FAQ

---

## 4. Code Quality Rules

### MQL5 Code Blocks

- Every MQL5 example MUST be **compilable in isolation** or clearly annotated
  with `// Requires: ...` showing the prerequisite includes/declarations.
- Use `CTrade` for trade operations — never raw `OrderSend`.
- Use `PositionSelectByTicket` / `PositionGetTicket` for position iteration.
- **No pseudo-code** — every example must compile against the MQL5 standard
  library (stdlib).
- Include `#property` directives and `#include` statements where needed for
  clarity.

Example:

```mql5
//+------------------------------------------------------------------+
//| Compilable snippet — trailing stop by ATR                        |
//+------------------------------------------------------------------+
#include <Trade/Trade.mqh>
CTrade Trade;

void TrailStopATR(ulong ticket, double atrMultiplier)
  {
   if(!PositionSelectByTicket(ticket)) return;
   double atr = iATR(_Symbol, PERIOD_CURRENT, 14, 0);
   double newSL = SymbolInfoDouble(_Symbol, SYMBOL_BID)
                - atrMultiplier * atr;
   Trade.PositionModify(ticket, newSL, 0);
  }
```

### Non-MQL5 Code Blocks

Python, TypeScript, and shell examples must follow the same principle:
complete enough to run with reasonable setup, with imports shown.

---

## 5. Prohibited Content

The following are NEVER allowed in any skill file:

- **Broker names or references** (e.g., "on MetaTrader with BrokerX")
- **Affiliate links or referral codes**
- **Private domains** (use `example.com` for placeholders)
- **Account-specific details** (real account numbers, server names, API keys,
  passwords)
- **Financial advice** (anything that tells a reader what or when to trade)
- **Warranty or performance guarantees** (always disclaim)

---

## 6. Tone and Style

- **Concise, direct, technical.** No marketing fluff.
- Present tense, active voice where possible.
- Lists > prose for enumerating options, parameters, or steps.
- Code examples > descriptive explanation whenever possible.

---

## 7. Review Checklist

Before submitting a skill PR, verify:

- [ ] Directory name == skill name (kebab-case)
- [ ] `SKILL.md` has valid YAML frontmatter with `name` and `description`
- [ ] Description under 500 chars with trigger phrases
- [ ] Body is 200–400 lines (extracted to `references/` if longer)
- [ ] All 6 required sections present
- [ ] MQL5 examples use `CTrade` and compile-plausible patterns
- [ ] No prohibited content (brokers, affiliates, private domains, accounts)
- [ ] No financial advice or performance guarantees
- [ ] `references/`, `scripts/`, `assets/` used if applicable
