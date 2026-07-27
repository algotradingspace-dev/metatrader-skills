# Scrub Policy

Every migration from `legacy/` MUST pass through these rules before any
skill is published. The goal is zero prohibited content reaching the
marketplace while preserving the skill's technical value.

---

## Rule 1 — REMOVE OUTRIGHT

The following MUST be replaced with obvious placeholders. No exceptions.

| Category | Examples found in legacy | Replace with |
|----------|--------------------------|--------------|
| Real account numbers | `1234567` | `ACCOUNT_LOGIN` |
| Real order tickets | `9876543210` | `TICKET_ID` |
| Real IP addresses | `203.0.113.42` | `CLIENT_IP_ADDRESS` |
| Real server DNS names | `ExampleBroker-MT5-1` | `<broker-server>` |
| Broker company legal names | `Example Trading Ltd` | `<broker-company>` |
| Personal file paths | `C:\Users\<username>\...` | `C:\Users\<user>\AppData\...` (keep `<user>` placeholder) |
| Non-official download URLs | `mirror.example.invalid/cdn/...` | Replace with official MetaQuotes URL or `<official-download-url>` |

### How to replace

- Inline in code: `string server = "ExampleBroker-MT5-1"` → `string server = "<broker-server>"`
- In prose: "connection to ExampleBroker-MT5-1 lost" → "connection to `<broker-server>` lost"
- In journal/log examples: replace the entire line with an annotated equivalent showing only the pattern, not the values

**Do not** keep real data in comments, commit history, or adjacent files.

---

## Rule 2 — GENERALIZE Named Brokers Used as Examples

When a document uses a specific broker name (FTMO, RoboForex, TeleTrade,
IC Markets, BlackBull, Eightcap, etc.) as an example of behaviour:

1. Replace the brand name with a description of *what the broker does*
   that causes the behaviour the reader needs to handle.
2. Provide runtime resolution code/config where possible instead.

### Examples

| Before | After |
|--------|-------|
| "RoboForex/FTMO = UTC+3, TeleTrade = UTC+2" | "Brokers on UTC+3 server time (common for ECN) vs UTC+2 (common for STP). Resolve at runtime: `SymbolInfoInteger(_Symbol, SYMBOL_TRADE_CALC_MODE)` and `TimeTradeServer()`" |
| "Adjust if your broker operates on a different server time" | (Keep — already generic) |
| "Match broker (1:100 typical for prop firms)" | "Match the broker's maximum allowed leverage. Common range: 1:30–1:500." |

### Rationale

A specific broker name is a liability: the name can become outdated, the
behaviour may not apply to all versions of that broker's offering, and it
implies endorsement. Describing the *category of behaviour* keeps the
skill accurate regardless of which broker the reader uses.

---

## Rule 3 — KEEP BUT ISOLATE Prop Firm Rule Presets

Prop firm rule sets (daily/total drawdown limits, weekend rules, news
restrictions) are genuine technical content. They stay — but isolated.

### Structure

The main `SKILL.md` body uses a **configurable rule-set struct** with
generic field names. Concrete firm numbers go in exactly one place:

```
skills/<skill-name>/references/prop-firm-rules.md
```

That file MUST begin with a dated verification header:

```
# Prop Firm Rule Presets
> **Last verified:** 2026-07-27
> **Verify before use:** Prop firm challenge rules change frequently.
> These values may be outdated. Always check the firm's current challenge
> terms before configuring an EA.
```

### Code pattern in SKILL.md

```mql5
//+------------------------------------------------------------------+
//| Prop firm rule set struct — values from external config           |
//+------------------------------------------------------------------+
struct PropFirmRules
{
   double daily_dd_limit;     // e.g. 5.0 = 5%
   double total_dd_limit;     // e.g. 10.0 = 10%
   double halt_daily_buffer;  // EA halts before hard limit
   double halt_total_buffer;
   bool   no_weekend_hold;
   bool   news_restricted;
   int    min_trading_days;
};

// Load from references/prop-firm-rules.md or user inputs
PropFirmRules LoadRules() { ... }
```

### What stays in SKILL.md body

- References to "prop firm" in descriptions, trigger phrases, and
  conceptual guidance — these are needed for agent activation.
- The generic algorithm for computing halt thresholds from a
  `PropFirmRules` struct.
- Guidance on how to configure the struct from inputs.

### What goes into references/

- The table mapping concrete firm names to their current limits.
- Historical values (if kept for comparison).

### What is removed

- Hardcoded `input double InpMaxDailyDD = 4.0; // Stays 1% below FTMO's 5%`
  — replace with `input double InpMaxDailyDD = 4.0; // Set per firm rules`

---

## Rule 4 — AMBIGUOUS: Flag, Do Not Guess

Any content that does not clearly fall into Rule 1, 2, or 3 must be
**flagged in the migration report** and left unchanged until a human
reviews it.

### How to flag

In the migration PR or commit message, add a line like:

```
FLAG: skills/<name>/SKILL.md:42 — references "<content>". 
Rule 1/2/3? Decision needed: [context].
```

### Examples of ambiguous content

- A URL to a third-party tool that happens to include a broker name
  in its path — is the broker name incidental or intentional?
- A journal snippet that anonymises everything except a well-known
  server name that is publicly documented — is that "real data" or
  "known infrastructure"?
- An input default that happens to match a specific broker's
  recommendation without naming the broker — is it a proxy reference?

When in doubt: flag it. The agent must never silently pass ambiguous
content.

---

## Review Checklist for Scrub

- [ ] Rule 1: Real account numbers, tickets, IPs, server DNS, company names, personal paths, non-official URLs — all replaced with placeholders
- [ ] Rule 2: Named broker examples replaced with behaviour descriptions and runtime resolution
- [ ] Rule 3: Prop firm presets isolated to `references/prop-firm-rules.md` with dated header; SKILL.md uses generic struct
- [ ] Rule 4: All ambiguous content flagged for human review
- [ ] `git log` checked for any prohibited content in commit history pre-scrub
