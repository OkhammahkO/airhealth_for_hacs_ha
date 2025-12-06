# Architectural Decision Records (ADR)

This document records significant architectural and implementation decisions made during the development of the AirHealth Home Assistant integration.

## Format

Each decision record includes:
- **Date**: When the decision was made
- **Status**: Accepted, Superseded, Deprecated
- **Context**: The situation requiring a decision
- **Decision**: What was decided
- **Consequences**: Impact of the decision

---

## ADR-001: Use DataUpdateCoordinator for API Data Fetching

**Date**: 2024-12-06
**Status**: Accepted

### Context

The integration needs to fetch data from multiple AirHealth API endpoints for different forecast types (grass pollen, other allergens, air quality/woodsmoke). Multiple sensors need access to the same data, and we need to avoid making redundant API calls.

### Decision

Implement a single `AirHealthDataUpdateCoordinator` that:
- Centralizes all API data fetching
- Manages update scheduling
- Provides data to all sensor entities
- Handles errors and caching gracefully

### Consequences

**Positive:**
- Single source of truth for API data
- Efficient API usage (no duplicate requests)
- Consistent error handling across all sensors
- Easy to implement caching and retry logic
- Sensors automatically update when coordinator refreshes

**Negative:**
- All sensors depend on coordinator lifecycle
- Slightly more complex initial setup

**Alternatives Considered:**
- Individual sensor polling: Rejected due to redundant API calls
- Polling service: Rejected as DataUpdateCoordinator is Home Assistant best practice

---

## ADR-002: Scheduled Updates at API-Specific Times

**Date**: 2024-12-06
**Status**: Accepted

### Context

AirHealth API provides forecasts that are updated at specific times each day:
- Grass pollen: 7:00 AM AEST
- Other allergens: 7:30 AM AEST
- Air quality/woodsmoke: 9:00 AM AEST

Polling more frequently would waste API calls; polling less frequently would miss updates.

### Decision

Implement scheduled time-based updates using `async_track_time_change`:
- Each enabled endpoint gets its own scheduled update time
- Updates trigger coordinator refresh
- Fallback 6-hour interval as backup

### Consequences

**Positive:**
- Efficient API usage aligned with data availability
- Fresh data shortly after API updates
- Reduces unnecessary API calls

**Negative:**
- Timezone dependency (AEST hardcoded in API)
- Less frequent updates than typical polling integrations
- Requires cleanup of time trackers on shutdown

**Implementation**: See [coordinator.py:47-69](custom_components/airhealth/coordinator.py#L47-L69)

---

## ADR-003: Graceful Fallback to Cached Data

**Date**: 2024-12-06
**Status**: Accepted

### Context

API requests can fail due to network issues, rate limiting, or service outages. Environmental health data changes slowly and previously fetched forecasts remain valuable even if updates fail temporarily.

### Decision

When API fetch fails with `AirHealthDataError`:
- Log warning but don't fail the entire update
- Return previously cached data if available
- Only raise `UpdateFailed` if no cached data exists

Authentication errors (`AirHealthAuthError`) always fail immediately as they indicate configuration issues.

### Consequences

**Positive:**
- Integration remains functional during temporary API issues
- User sees stale but useful data vs. no data
- Better user experience during network problems

**Negative:**
- Stale data might mislead users if they don't notice update time
- Could mask persistent API problems

**Mitigation:**
- Log warnings clearly when using cached data
- Sensors show last update time in attributes

**Implementation**: See [coordinator.py:92-101](custom_components/airhealth/coordinator.py#L92-L101)

---

## ADR-004: Service Integration Type with Device Grouping

**Date**: 2024-12-06
**Status**: Accepted

### Context

AirHealth provides a cloud-based forecasting service. Sensors represent different data points from the same service rather than separate physical devices.

### Decision

- Integration type: `service` (in manifest.json)
- IoT class: `cloud_polling`
- All sensors grouped under single "AirHealth" device
- Device info includes manufacturer and model

### Consequences

**Positive:**
- Clean UI presentation with single device card
- Accurate representation of the service architecture
- Easy to find all AirHealth sensors together
- Proper categorization in Home Assistant

**Negative:**
- Cannot assign different sensors to different devices
- All sensors share same device lifecycle

**Implementation**: See [entity.py:14-30](custom_components/airhealth/entity.py#L14-L30)

---

## ADR-005: Three Sensors Per Forecast Type (Day 0, 1, 2)

**Date**: 2024-12-06
**Status**: Accepted

### Context

AirHealth API returns 3-day forecasts in array format. Home Assistant sensors represent single values, not arrays.

### Decision

Create separate sensor entities for each day:
- `sensor.airhealth_grass_day0` - Today
- `sensor.airhealth_grass_day1` - Tomorrow
- `sensor.airhealth_grass_day2` - Day after tomorrow

Similar pattern for other allergens, air quality, and woodsmoke.

### Consequences

**Positive:**
- Each sensor has clear, specific purpose
- Easy to use in automations and dashboards
- Aligns with Home Assistant sensor patterns
- Can track history separately per day

**Negative:**
- More entities (9-18 sensors depending on subscription)
- More complex entity setup code
- Duplicate data in attributes

**Alternatives Considered:**
- Single sensor with array in attributes: Rejected, not user-friendly
- JSON sensor: Rejected, requires custom frontend card

**Implementation**: See [sensor.py:42-94](custom_components/airhealth/sensor.py#L42-L94)

---

## ADR-006: PARALLEL_UPDATES = 0 for Sensor Platform

**Date**: 2024-12-06
**Status**: Accepted

### Context

Multiple sensors read from the same coordinator data. If sensors update in parallel, they might see inconsistent data during coordinator refresh.

### Decision

Set `PARALLEL_UPDATES = 0` in sensor platform to serialize updates.

### Consequences

**Positive:**
- All sensors see consistent coordinator data
- Prevents race conditions during updates
- Ensures atomic update of related sensors

**Negative:**
- Slightly slower sensor updates (negligible with coordinator pattern)

**Note:** This is a standard pattern for coordinator-based integrations.

**Implementation**: See [sensor.py:37](custom_components/airhealth/sensor.py#L37)

---

## ADR-007: Two-Step Config Flow (Credentials → Endpoints)

**Date**: 2024-12-06
**Status**: Accepted

### Context

Users have AirHealth subscriptions with different endpoint access. Not all users subscribe to all data types. Need to validate credentials before asking about endpoints.

### Decision

Implement two-step config flow:
1. **Step 1**: Collect and validate API key + SAL code
2. **Step 2**: User selects which endpoints they have subscribed to

### Consequences

**Positive:**
- Validates credentials before asking for more input
- Clear UX separation between authentication and configuration
- Prevents errors from unsubscribed endpoints
- User controls which data to import

**Negative:**
- Two-step process slightly longer
- Cannot auto-detect available endpoints from API

**Future Enhancement:** Could query API to auto-detect subscribed endpoints

**Implementation**: See [config_flow.py:33-87](custom_components/airhealth/config_flow.py#L33-L87)

---

## ADR-008: Custom Exception Classes

**Date**: 2024-12-06
**Status**: Accepted

### Context

Need to distinguish between different types of API failures for proper error handling and user feedback.

### Decision

Define custom exception hierarchy:
- `AirHealthError` - Base exception
- `AirHealthAuthError` - Authentication/authorization failures (401, 403)
- `AirHealthDataError` - Data fetch failures (network, timeouts, other HTTP errors)

### Consequences

**Positive:**
- Precise error handling based on failure type
- Better error messages to users
- Auth errors fail fast (config issue)
- Data errors allow fallback to cache

**Negative:**
- Additional exception classes to maintain

**Implementation**: See [api.py:10-18](custom_components/airhealth/api.py#L10-L18)

---

## ADR-009: No External Dependencies

**Date**: 2024-12-06
**Status**: Accepted

### Context

Integration needs to make HTTP requests to AirHealth API. Home Assistant provides aiohttp in core.

### Decision

Use Home Assistant's built-in `aiohttp.ClientSession` rather than external HTTP libraries.

Set `requirements = []` in manifest.json.

### Consequences

**Positive:**
- No additional dependencies to install
- Faster installation
- Better compatibility
- Uses Home Assistant's connection pooling

**Negative:**
- Tied to Home Assistant's aiohttp version
- Cannot use specialized HTTP client features

**Note:** This is the recommended approach for simple HTTP API integrations.

**Implementation**: See [manifest.json:11](custom_components/airhealth/manifest.json#L11)

---

## ADR-010: Sensor Attributes Include Raw API Data

**Date**: 2024-12-06
**Status**: Accepted

### Context

API returns rich data beyond simple forecast values (allergen breakdowns, air quality details, forecast issue times).

### Decision

Include full API response data in sensor attributes:
- Allergen-specific breakdowns (birch, plantain, etc.)
- Supporting air quality data
- Forecast issue times
- All available metadata

### Consequences

**Positive:**
- Power users can access detailed data
- Useful for debugging
- Supports advanced automations
- No information loss from API

**Negative:**
- Larger state objects
- Some data may be unused by most users

**Implementation**: See [sensor.py:120-178](custom_components/airhealth/sensor.py#L120-L178)

---

## Future Decisions to Document

As the integration evolves, document future decisions here:

- Multi-location support strategy
- Configurable update intervals
- Historical data storage approach
- Alert/notification features
- Dashboard card implementation
- API v2 migration (if applicable)

---

## Decision Review Process

1. Propose decision in GitHub issue
2. Discuss alternatives and trade-offs
3. Document decision in this file
4. Reference in code comments where implemented
5. Review decisions when requirements change
