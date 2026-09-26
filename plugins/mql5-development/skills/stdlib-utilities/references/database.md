# Database — SQLite Open, Prepare, Bind, Execute, Transactions, Import/Export

MQL5 database functions wrap SQLite and are the right choice when array logic
is turning into ad hoc storage or query code.

## Database Lifecycle and Query Preparation

> Canonical MQL5 reference: [DatabaseOpen](https://www.mql5.com/en/docs/database/databaseopen) · [DatabaseClose](https://www.mql5.com/en/docs/database/databaseclose) · [DatabaseTableExists](https://www.mql5.com/en/docs/database/databasetableexists) · [DatabasePrepare](https://www.mql5.com/en/docs/database/databaseprepare)

| Function group | What it covers | Usage note |
|----------------|----------------|------------|
| `DatabaseOpen`, `DatabaseClose`, `DatabaseTableExists` | Database lifecycle | Disk databases need path discipline; memory databases are process-local |
| `DatabasePrepare`, `DatabaseBind`, `DatabaseBindArray`, `DatabaseReset`, `DatabaseFinalize` | Prepared-statement workflow | Use prepared statements for repeated queries instead of rebuilding SQL strings inside loops |
| `DatabaseRead`, `DatabaseReadBind` | Row retrieval | `DatabaseReadBind` is the cleanest path when a struct maps to the selected columns |
| `DatabasePrint` | Journal inspection of query results | Useful for debugging query shape without writing export code |

## Execute, Transactions, Import/Export, and Column Metadata

> Canonical MQL5 reference: [DatabaseExecute](https://www.mql5.com/en/docs/database/databaseexecute) · [DatabaseTransactionBegin](https://www.mql5.com/en/docs/database/databasetransactionbegin) · [DatabaseTransactionCommit](https://www.mql5.com/en/docs/database/databasetransactioncommit) · [DatabaseTransactionRollback](https://www.mql5.com/en/docs/database/databasetransactionrollback)

| Function group | What it covers | Usage note |
|----------------|----------------|------------|
| `DatabaseExecute` | Non-row-returning SQL execution | Use for inserts, updates, deletes, and DDL |
| `DatabaseTransactionBegin`, `DatabaseTransactionCommit`, `DatabaseTransactionRollback` | Bulk-write performance and atomicity | Batch writes inside transactions or performance will collapse |
| `DatabaseImport`, `DatabaseExport` | CSV ingress and egress | Useful when bridging tester results or external analysis workflows |
| `DatabaseColumnsCount`, `DatabaseColumnName`, `DatabaseColumnType`, `DatabaseColumnSize`, `DatabaseColumnText`, `DatabaseColumnInteger`, `DatabaseColumnLong`, `DatabaseColumnDouble`, `DatabaseColumnBlob` | Result introspection | Use when the result schema is dynamic or not known at compile time |
