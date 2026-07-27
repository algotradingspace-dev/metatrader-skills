---
name: economic-calendar
description: >
  MQL5 economic calendar API reference skill. Use for: querying calendar
  countries or events; looking up calendar metadata by id, country, or currency
  code; retrieving historical or latest economic values; incremental polling with
  change_id for efficient live filters; wiring calendar-based trade-blocking
  logic into Expert Advisors. Trigger: "CalendarCountries", "CalendarEventById",
  "CalendarValueHistory", "CalendarValueLast", "economic calendar",
  "calendar filter", "news filter", "CalendarEventByCountry",
  "CalendarValueHistoryByEvent", "change_id".
---

# Economic Calendar

Use this skill when an EA needs direct access to the terminal economic-calendar
database instead of scraping external news feeds.

This is a Reference skill: the body is a routing table into function-group
summaries. Read the relevant section for the API function you need.

---

## Purpose

Catalogs the MQL5 economic calendar API: metadata lookups for countries and
events, historical value queries, incremental polling via `change_id`, and
usage rules for calendar data in EAs.

---

## When to Use

- Mapping country or currency filters to economic calendar events
- Pulling event metadata for scheduling or impact analysis
- Reading historical calendar values for backtests or live filters
- Polling only the latest changes using `change_id`

**Do NOT use** for:
- Hardcoded news-avoidance times (simpler) -> use `market-regime` news filter
- Scraping external news feeds via WebRequest -> use `network`

---

## CAL-1: Countries, Events, and Calendar Metadata Lookups

| Function | Purpose | Usage note |
|----------|---------|------------|
| `CalendarCountries(countries[])` | Returns the list of countries present in the calendar database | Use when building dynamic filter menus or validating codes |
| `CalendarCountryById(id, country)` | Resolves one country description by numeric id | Country codes follow ISO 3166-1 alpha-2 naming |
| `CalendarEventById(id, event)` | Resolves one event description by id | Use when a stored event id needs metadata |
| `CalendarEventByCountry(code, events[])` | Returns all events for a country code | Best for region-specific event scans |
| `CalendarEventByCurrency(currency, events[])` | Returns all events for a currency code | Useful when trading a currency basket |
| `CalendarValueById(id, value)` | Resolves one calendar value record by value id | Use for point lookups after storing a value id |

### Metadata rules

- Country filters use codes like `US`, `DE`, `EU`; currency filters use codes
  like `USD`, `EUR`
- Country and currency filters are exact selectors, not fuzzy searches
- Cache metadata ids first, then use history calls for the heavier data path

---

## CAL-2: Historical Values, Incremental Polling, and Server-Time Rules

| Function | Purpose | Usage note |
|----------|---------|------------|
| `CalendarValueHistory(values, from, to, country, currency)` | Returns all matching values in a time range | Use for broad history pulls or multi-country scans |
| `CalendarValueHistoryByEvent(event_id, values, from, to)` | Returns values for one event across a time range | Use when event id is known and the series is the interest |
| `CalendarValueLast(change_id, values, country, currency)` | Returns only values added since previous state | Passing `change_id=0` initialises without returning a backlog |
| `CalendarValueLastByEvent(change_id, event_id, values)` | Returns only new values for one event | Use for low-overhead listeners tied to specific indicators |

### Value-handling rules

- All calendar times use `TimeTradeServer()`, not local machine time
- `change_id` is the key to efficient live polling; keep it between calls
- Calendar value numeric fields are stored scaled by one million; divide by
  `1,000,000` after checking for `LONG_MIN`
- Fixed-size arrays can trigger `ERR_CALENDAR_MORE_DATA`; use dynamic arrays

---

## References

- `docs/mql5_com_-_docs/calendar.md`
- `docs/mql5_com_-_docs/calendar-calendarcountries.md`
- `docs/mql5_com_-_docs/calendar-calendarcountrybyid.md`
- `docs/mql5_com_-_docs/calendar-calendareventbycountry.md`
- `docs/mql5_com_-_docs/calendar-calendareventbycurrency.md`
- `docs/mql5_com_-_docs/calendar-calendareventbyid.md`
- `docs/mql5_com_-_docs/calendar-calendarvaluebyid.md`
- `docs/mql5_com_-_docs/calendar-calendarvaluehistory.md`
- `docs/mql5_com_-_docs/calendar-calendarvaluehistorybyevent.md`
- `docs/mql5_com_-_docs/calendar-calendarvaluelast.md`
- `docs/mql5_com_-_docs/calendar-calendarvaluelastbyevent.md`
