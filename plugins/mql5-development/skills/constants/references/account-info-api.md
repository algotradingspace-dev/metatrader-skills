# Account Information API Access Patterns

## Signatures

```mql5
long   AccountInfoInteger(ENUM_ACCOUNT_INFO_INTEGER property_id);
double AccountInfoDouble(ENUM_ACCOUNT_INFO_DOUBLE property_id);
string AccountInfoString(ENUM_ACCOUNT_INFO_STRING property_id);
```

## Type Expectations

| Function | Returns | Typical property families |
|----------|---------|--------------------------|
| `AccountInfoInteger()` | `long` | login, leverage, trade flags, margin mode, trade mode |
| `AccountInfoDouble()` | `double` | balance, equity, margin, free margin, stop-out levels |
| `AccountInfoString()` | `string` | account name, server, currency, company |

## Casting Patterns

```mql5
bool tradeAllowed = (bool)AccountInfoInteger(ACCOUNT_TRADE_ALLOWED);
ENUM_ACCOUNT_TRADE_MODE tradeMode =
   (ENUM_ACCOUNT_TRADE_MODE)AccountInfoInteger(ACCOUNT_TRADE_MODE);
ENUM_ACCOUNT_STOPOUT_MODE stopoutMode =
   (ENUM_ACCOUNT_STOPOUT_MODE)AccountInfoInteger(ACCOUNT_MARGIN_SO_MODE);
double equity = AccountInfoDouble(ACCOUNT_EQUITY);
string currency = AccountInfoString(ACCOUNT_CURRENCY);
```

## Practical Usage Notes

- `AccountInfoInteger()` is the access path for `bool`, `int`, `long`,
  `datetime`, and enum-backed account properties
- `AccountInfoDouble()` is the canonical runtime source for sizing and margin
  checks such as `ACCOUNT_BALANCE`, `ACCOUNT_EQUITY`, and `ACCOUNT_MARGIN_FREE`
- `AccountInfoString()` is mainly for account identity and display context:
  server, company, and deposit currency
- Match the accessor to the property family; a wrong pairing is a modelling
  error, not just a formatting issue
- For risk sizing, combine `AccountInfoDouble(ACCOUNT_BALANCE)` or
  `ACCOUNT_EQUITY` with live symbol properties
