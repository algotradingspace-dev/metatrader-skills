---
name: imported-backtest
description: >
  Handles importing MT5 Strategy Tester HTML reports uploaded by users as
  first-class backtest results. Covers parsing via the canonical ReportParser,
  equity reconstruction from broker or Darwinex fallback price data, broker
  server resolution, and integrating imported results into comparison and
  analysis pipelines. Use for: uploading .htm reports from external MT5
  sessions; reconstructing equity curves when no live terminal is available;
  making imported tests indistinguishable from native runs. Trigger on:
  "import backtest", "upload HTML report", "imported test", "import report".
---
# Imported Backtests

## Purpose

Users can run MT5 Strategy Tester on their own terminal and upload the
`.htm` report file. This skill handles the full pipeline: receive the
file, parse it into the same `TestResult` structure used by native runs,
reconstruct the equity curve from available price data (broker terminal or
Darwinex fallback), and surface the result in the comparison and analysis
UI with an "Imported" badge.

## When to use / When NOT to use

Use when:
- Implementing or debugging the `POST /api/tests/import-report` route
- Adding broker/server resolution for a new price-data source
- Fixing equity reconstruction for imported reports
- Building the import dialog UI or result badges

Do NOT use for:
- Native backtest execution (use `backtest-analysis` skill)
- Interpreting backtest metrics after import (use `analytics` skill)
- Generic file upload handling

## Core guidance

### Import pipeline

1. **Receive** — multipart POST with `.htm` file, user auth, optional
   broker/server override
2. **Persist** — save raw HTML to `{data-dir}/reports/{uuid}.htm`
3. **Parse** — call canonical `ReportParser.parseTestReport()` (same code
   native runs use) → produces `TestResult` with 80+ metrics
4. **Resolve broker** — map `report.loginServer` to a price-data context
   (configured MT5 account, Darwinex metadata, or none)
5. **Reconstruct equity** — run `reconstructEquity()` with the resolved
   context → save equity history to `{data-dir}/equity-history/{testId}.json`
6. **Persist** — store `TestRecord` + `TestResult` marked `source: 'imported'`

### Broker resolution (3-way)

```
report.loginServer → match config.accounts[*][*].server
  ├─ YES → ping({ broker, account })
  │        ├─ success → use broker price data
  │        └─ failure → Darwinex fallback
  └─ NO  → Darwinex fallback
             ├─ has symbol data → equity reconstructed
             └─ no data → equityStatus = 'unavailable'
```

The user can override auto-detection via the import dialog.

### Data model

`TestResult` gains optional fields to track import provenance:

- `source`: `'native' | 'imported'`
- `importedAt`: ISO timestamp
- `originalFileName`: uploaded filename
- `equityStatus`: `'ok' | 'approximate' | 'unavailable'`
- `equityUnavailableReason`, `equityMissingSymbols`: diagnostic info

These are nullable columns in PostgreSQL; existing rows default to
`source='native'`.

## Code patterns

### Import route skeleton

```typescript
// POST /api/tests/import-report
export async function POST(req: Request) {
  const form = await req.formData()
  const file = form.get('file') as File
  // validate: .htm, max 50MB
  // persist raw HTML to {data-dir}/reports/{uuid}.htm
  // parse via ReportParser.parseTestReport(filepath)
  // resolve broker context from report.loginServer
  // reconstruct equity
  // save TestRecord + TestResult
  // return 201 with test ID
}
```

### Equity reconstruction with graceful failure

```typescript
function reconstructEquityWithStatus(
  deals: Deal[],
  context: PriceDataContext
): EquityReconstructionResult {
  try {
    const result = reconstructEquity(deals, context)
    if (!result) {
      return {
        points: [],
        unavailableReason: 'reconstructor returned null',
        missingSymbols: []
      }
    }
    return result
  } catch (e) {
    return {
      points: [],
      unavailableReason: e.message,
      missingSymbols: []
    }
  }
}
```

## Common mistakes

- **Treating missing equity as fatal** — imported reports may lack price
  data. The `equityStatus` field and banner handle this gracefully. Never
  reject an import because equity cannot be reconstructed.
- **Leaving null returns** — `reconstructEquity()` returns `null` on
  failure. Wrap it to always return a result with diagnostic fields.
- **Skipping HTML sandboxing** — user-uploaded HTML is untrusted. Always
  serve via sandboxed iframe with strict CSP or strip scripts on ingest.
- **Hardcoding server → broker mappings** — read from `config.yaml` and
  ping to verify connectivity; server names change per deployment.

## References

| File | Content |
|------|---------|
| (none yet) | |
