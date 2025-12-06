# Design Decisions

Key architectural decisions for the AirHealth integration.

## DataUpdateCoordinator

**Why:** Centralize API data fetching to avoid redundant calls.
**Implementation:** Single coordinator fetches all enabled endpoints and provides data to sensors.

## Scheduled Updates

**Why:** AirHealth API updates at specific times (7:00 AM, 7:30 AM, 9:00 AM AEST).
**Implementation:** Time-based triggers for each endpoint instead of polling intervals.

## Cached Data Fallback

**Why:** Environmental data changes slowly; stale data better than no data.
**Implementation:** Return cached data on API failures, only fail if no cache exists.

## Service Integration Type

**Why:** AirHealth is a cloud service, not a physical device.
**Implementation:** Single device grouping all sensors, `cloud_polling` IoT class.

## Three Sensors Per Forecast

**Why:** API returns 3-day forecasts; Home Assistant sensors represent single values.
**Implementation:** Separate sensors for day 0, 1, and 2 of each forecast type.

## Two-Step Config Flow

**Why:** Validate credentials before asking about endpoint subscriptions.
**Implementation:** Step 1: API key + SAL code validation. Step 2: Endpoint selection.

## No External Dependencies

**Why:** Simpler installation and better compatibility.
**Implementation:** Use Home Assistant's built-in `aiohttp` for API calls.
