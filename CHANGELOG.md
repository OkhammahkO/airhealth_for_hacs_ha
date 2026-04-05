# Changelog

All notable changes to this project will be documented in this file.

## [0.3.0] - 2026-04-05

### Added
- `translations/en.json` for Home Assistant UI string localisation
- Natural language summary helpers (`summarize_grass_pollen`, `summarize_allergen_breakdown`) for grass pollen and other allergen sensors

### Changed
- Update schedule now supports multiple times per endpoint (Air Quality/Woodsmoke now refreshes at 9:00 AM, 1:00 PM, 5:00 PM, and 9:00 PM AEST)
- Other allergens update time corrected to 9:00 AM AEST (was 7:00 AM)
- Sensor naming refactored to use Home Assistant `_attr_has_entity_name` convention

### Fixed
- Config flow `async_show_form` now passes explicit `errors={}` to prevent stale error display

## [0.2.0] - 2024-12-06

### Added
- Initial HACS release
- Config flow UI setup
- Grass pollen forecasts (3-day)
- Other allergen forecasts (3-day)
- Air quality and woodsmoke forecasts (3-day)
- Automatic scheduled updates at API times (7:30 AM, 9:00 AM, 1:00 PM, 5:00 PM, 9:00 PM AEST)
- Graceful fallback to cached data on failures
- Level icons (coloured circles) for pollen and allergen sensors
- Natural language summaries for grass pollen and other allergen sensors
- SAL code and API status metadata on all sensors
