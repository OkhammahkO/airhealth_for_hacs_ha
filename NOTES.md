# Project Notes

Development notes and current status for the AirHealth integration.

## Current Status

**Version:** 0.2.0
**Status:** Ready for HACS publication
**Last Updated:** 2024-12-06

## Features

- Grass pollen forecasts (3-day)
- Other allergen forecasts (3-day)
- Air quality and woodsmoke forecasts (3-day)
- Scheduled updates at API times (7:00 AM, 7:30 AM, 9:00 AM AEST)
- Config flow UI setup
- Graceful error handling with cached data fallback

## Known Limitations

- Single SAL code per config entry (no multi-location support yet)
- Update times are API-defined, not user-configurable
- No historical data storage

## API Details

- **Base URL:** `https://api-public.airhealthservices.au/api`
- **Authentication:** API key + SAL code
- **Endpoints:** `/forecast/grass/:sal`, `/forecast/other/:sal`, `/forecast/airquality/:sal`
- **Response:** JSON with 3-day forecast arrays

## Future Enhancements

- Multi-location support (multiple SAL codes)
- Configurable update intervals
- Historical data tracking
- Alert system for high pollen/poor air quality
- Custom Lovelace card

## Testing

Run tests:
```bash
pytest custom_components/airhealth/tests/
```

## Deployment Checklist

- [ ] Version in manifest.json matches tag
- [ ] CHANGELOG.md updated
- [ ] Git tag created
- [ ] GitHub release published
- [ ] HACS installation tested
