# AirHealth Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

Home Assistant integration for [AirHealth](https://www.airhealthlab.com/index.php) API - Australian air quality data including grass pollen, allergens, air quality, and woodsmoke levels.

## Requirements

- AirHealth API subscription (get yours at [airhealthlab.com](https://www.airhealthlab.com/index.php/airhealth-api))

## Installation

### 1. Add to HACS

1. Open HACS → Integrations
2. Click ⋮ → Custom repositories
3. Add `https://github.com/OkhammahkO/airhealth_for_hacs_ha` as an Integration
4. Install "AirHealth" and restart Home Assistant

### 2. Configure

1. Settings → Devices & Services → Add Integration
2. Search for "AirHealth"
3. Enter your API key and SAL code
4. Select your subscribed endpoints

## Sensors

Provides 3-day forecasts (today, tomorrow, day 2) for:

- **Grass pollen**
- **Other allergens**
- **Air quality**
- **Woodsmoke**

## Support

[Open an issue](https://github.com/OkhammahkO/airhealth_for_hacs_ha/issues) for questions or problems.

## License

MIT License
