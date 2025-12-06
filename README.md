# AirHealth Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

Home Assistant integration for the [AirHealth Services](https://www.airhealthlab.com/index.php) API, providing Australian air quality data including:

- Grass pollen forecasts
- Other allergen forecasts (plantain, birch, etc.)
- Air quality levels
- Woodsmoke levels

## Features

- Fixed updates at API-specific times to conserve API quota usage.
- Detailed attributes including allergen breakdowns and supporting air quality data
- Easy configuration through Home Assistant UI

## Installation

### Getting API Access

Before installing this integration, you'll need an AirHealth API account and (paid) plan:

1. Visit the [AirHealth API website](https://www.airhealthlab.com/index.php/airhealth-api)
2. Contact AirHealth to confirm pricing and sign-up details (The API service is new so things may change)
3. Once your account and plan are set up, you'll be able to:
   - Generate an API key for your use
   - Use their tool to find your SAL (Statistical Area Level) code
4. Save your API key and SAL code (securely) - you'll need them during integration setup

### HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add `https://github.com/OkhammahkO/prj-airhealth` as a custom repository
6. Select "Integration" as the category
7. Click "Add"
8. Find "AirHealth" in the integration list and click "Download"
9. Restart Home Assistant

## Configuration

1. Go to Settings → Devices & Services
2. Click "+ Add Integration"
3. Search for "AirHealth"
4. Enter your API key and SAL code
5. Select which endpoints you have subscribed to:
   - Grass pollen forecast
   - Other allergens forecast
   - Air quality and woodsmoke forecast

## Usage

After configuration, you'll see sensors for each enabled endpoint:

- `sensor.airhealth_grass_day0` - Grass pollen today
- `sensor.airhealth_grass_day1` - Grass pollen tomorrow
- `sensor.airhealth_grass_day2` - Grass pollen in 2 days
- `sensor.airhealth_other_allergens_day0` - Other allergens today
- `sensor.airhealth_air_quality_day0` - Air quality today
- `sensor.airhealth_woodsmoke_day0` - Woodsmoke level today

Each sensor includes detailed attributes with additional data from the API.

## Requirements

- Home Assistant 2024.1.0 or newer
- AirHealth API subscription and credentials

## Support

For issues, feature requests, or questions, please [open an issue](https://github.com/OkhammahkO/prj-airhealth/issues).

## License

MIT License - see LICENSE file for details
