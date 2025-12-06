# Project Notes

This document tracks the current state of the AirHealth integration project, including development status, known issues, and future plans.

## Current Status

**Version**: 0.2.0 (HACS-ready release)
**Status**: Ready for publication
**Last Updated**: 2024-12-06

### Implementation Status

- [x] Core integration structure
- [x] Config flow (two-step: credentials + endpoints)
- [x] DataUpdateCoordinator with scheduled updates
- [x] API client with error handling
- [x] Sensor platform (grass, other allergens, air quality, woodsmoke)
- [x] Device grouping
- [x] Basic test suite
- [x] Documentation (README, CONTRIBUTING, DECISIONS, CHANGELOG)
- [x] HACS configuration
- [x] MIT License
- [ ] Comprehensive test coverage
- [ ] GitHub Actions CI/CD
- [ ] pyproject.toml configuration

### Supported Features

1. **Grass Pollen Forecasts** (3-day)
   - Daily total pollen levels
   - Detailed allergen breakdown
   - Update time: 7:00 AM AEST

2. **Other Allergen Forecasts** (3-day)
   - Plantain, birch, and other allergens
   - Individual allergen levels
   - Update time: 7:30 AM AEST

3. **Air Quality & Woodsmoke** (3-day)
   - Air quality index
   - Woodsmoke levels
   - Supporting air quality data
   - Update time: 9:00 AM AEST

4. **Integration Features**
   - Automatic scheduled updates at API-specific times
   - Graceful fallback to cached data on failures
   - Config flow UI setup
   - Device grouping for all sensors
   - Rich sensor attributes with full API data

## Known Issues

### Current Issues

None currently tracked. See [GitHub Issues](https://github.com/OkhammahkO/prj-airhealth/issues) for reported problems.

### Known Limitations

1. **Timezone Dependency**: Update times are hardcoded to AEST (Australian Eastern Standard Time) as specified by the API
2. **No Multi-Location Support**: Currently supports single SAL code per config entry
3. **Fixed Update Schedule**: Update times are API-defined and not user-configurable
4. **No Historical Data**: Integration doesn't store historical forecast data
5. **Limited Test Coverage**: Basic tests present but comprehensive coverage needed

## Development Notes

### API Characteristics

- **Base URL**: `https://api.airhealth.net.au/`
- **Authentication**: API key + SAL (Statistical Area Level) code
- **Endpoints**:
  - `/forecast/grass/:sal_code` - Grass pollen forecasts
  - `/forecast/other/:sal_code` - Other allergen forecasts
  - `/forecast/airquality/:sal_code` - Air quality & woodsmoke
- **Response Format**: JSON with 3-day forecast arrays
- **Update Times**: Different for each endpoint (7:00 AM, 7:30 AM, 9:00 AM AEST)
- **Rate Limiting**: Unknown, but scheduled updates minimize impact

### Technical Details

- **Platform**: Home Assistant custom component
- **Language**: Python 3.11+
- **Async**: Full async/await implementation
- **Dependencies**: None (uses HA core libraries)
- **IoT Class**: cloud_polling
- **Integration Type**: service

### Code Structure

```
custom_components/airhealth/
├── __init__.py           # Integration setup/unload
├── manifest.json         # Integration metadata
├── config_flow.py        # UI configuration flow
├── coordinator.py        # DataUpdateCoordinator
├── api.py               # API client
├── sensor.py            # Sensor platform
├── entity.py            # Base entity class
├── const.py             # Constants
├── strings.json         # Localization
└── tests/               # Test suite
    ├── conftest.py
    ├── test_init.py
    └── test_sensor.py
```

## Future Enhancements

### Planned Features

1. **Multi-Location Support**
   - Allow multiple config entries for different SAL codes
   - Support for multiple locations on dashboards

2. **Configurable Update Intervals**
   - Allow users to set custom fallback update intervals
   - Option to poll more frequently if desired

3. **Historical Data Tracking**
   - Store previous forecasts for accuracy tracking
   - Trend analysis over time

4. **Alert/Notification System**
   - Notify when pollen levels exceed thresholds
   - Alert on air quality warnings

5. **Dashboard Card**
   - Custom Lovelace card for AirHealth data
   - Visual representation of forecast trends

### Technical Improvements

1. **Enhanced Testing**
   - Config flow validation tests
   - API error handling tests
   - Coordinator refresh behavior tests
   - Integration tests with mocked API

2. **CI/CD Pipeline**
   - GitHub Actions for automated testing
   - Linting with ruff
   - Type checking with mypy
   - Coverage reporting

3. **Code Quality**
   - Comprehensive docstrings
   - Type hints for all functions
   - Pre-commit hooks

4. **Error Recovery**
   - Exponential backoff for API failures
   - Better retry strategies
   - User-facing error notifications

5. **Configuration Options**
   - Options flow for post-setup configuration
   - Enable/disable specific sensors
   - Adjust update schedules

## Questions & Uncertainties

### Open Questions

1. **API Rate Limiting**: What are the actual rate limits?
   - *Action*: Monitor usage and document findings

2. **SAL Code Changes**: Do SAL codes ever change or become invalid?
   - *Action*: Implement validation and error handling

3. **API Versioning**: Will there be API v2? Migration strategy?
   - *Action*: Monitor API documentation for updates

4. **Historical Data Storage**: Should we store forecast history?
   - *Decision Needed*: Balance utility vs. database size

5. **Timezone Handling**: How to handle DST transitions in AEST?
   - *Current*: Using AEST without DST adjustment
   - *Action*: Test during DST transitions

## Testing Notes

### Test Coverage Status

**Current Coverage**: ~40% (estimated)

**Covered**:
- Basic integration setup
- Sensor entity creation
- Mock API responses

**Not Covered**:
- Config flow validation
- API error scenarios
- Coordinator refresh behavior
- Scheduled update triggers
- Cached data fallback
- Authentication failures

**Test Environment**:
- Framework: pytest
- HA Plugin: pytest-homeassistant-custom-component
- Fixtures: Mock API client, config entry

## Deployment Checklist

### Pre-Release Checklist

- [x] Version number updated in manifest.json
- [x] CHANGELOG.md updated
- [x] README.md reviewed
- [x] All code committed
- [x] License file present
- [x] HACS configuration verified
- [ ] Tests passing
- [ ] GitHub release created
- [ ] Git tag created

### HACS Submission Checklist

- [x] Repository public
- [x] hacs.json present
- [x] README.md with installation instructions
- [x] LICENSE file
- [x] manifest.json valid
- [x] Integration in custom_components/ directory
- [ ] At least one release tag

## Performance Notes

### Benchmarks

*To be measured*:
- API response times
- Coordinator update duration
- Sensor state update time
- Memory footprint

### Optimization Opportunities

1. Cache API responses more aggressively
2. Reduce attribute data size if performance issues
3. Optimize coordinator refresh logic

## Community Feedback

### Feature Requests

*To be collected after release*

### Bug Reports

*To be tracked in GitHub Issues*

## References

- [AirHealth API Documentation](https://www.airhealth.net.au/)
- [Home Assistant Developer Docs](https://developers.home-assistant.io/)
- [HACS Integration Requirements](https://hacs.xyz/docs/publish/integration)
- [Integration Quality Scale](https://www.home-assistant.io/docs/quality_scale/)

## Maintenance Log

| Date       | Action                           | Notes                          |
|------------|----------------------------------|--------------------------------|
| 2024-12-06 | Initial HACS-ready release       | Version 0.2.0, ready to publish|
| 2024-12-06 | Created documentation files      | CHANGELOG, CONTRIBUTING, etc.  |

---

**Next Steps**:
1. Implement CI/CD with GitHub Actions
2. Expand test coverage
3. Create first GitHub release
4. Submit to HACS default repository (optional)
