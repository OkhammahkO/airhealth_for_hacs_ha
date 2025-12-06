# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2024-12-06

### Added
- Initial HACS-ready release
- Config flow for easy setup through Home Assistant UI
- Support for grass pollen forecasts (3-day)
- Support for other allergen forecasts (3-day)
- Support for air quality and woodsmoke forecasts (3-day)
- Automatic scheduled updates at API-specific times (7:00 AM, 7:30 AM, 9:00 AM AEST)
- DataUpdateCoordinator for centralized data fetching
- Graceful fallback to cached data on API failures
- Device grouping for all sensors under AirHealth service
- Comprehensive sensor attributes with detailed allergen breakdowns
- Error handling with custom exceptions
- Basic test suite with pytest fixtures
- Complete documentation (README, API details, best practices)

### Technical Details
- Async/await patterns throughout
- Custom API client with proper error handling
- Cloud polling IoT class with scheduled updates
- PARALLEL_UPDATES = 0 for sensor serialization
- Unique ID strategy for entity management
- Proper lifecycle management (setup/unload)

## [Unreleased]

### Planned
- Enhanced error recovery strategies
- Configuration options for update intervals
- Additional sensor attributes based on user feedback
- Expanded test coverage
- GitHub Actions CI/CD pipeline

---

[0.2.0]: https://github.com/OkhammahkO/prj-airhealth/releases/tag/v0.2.0
