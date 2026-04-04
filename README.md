# AirHealth for Home Assistant
> Australian pollen & air quality forecasts

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![Built with Claude Code](https://img.shields.io/badge/built%20with-Claude-blueviolet)](https://claude.ai)

- [AirHealth](https://www.airhealthlab.com/) is the company behind [Melbourne Pollen](https://www.melbournepollen.com.au/) (and sister sites).
- In addition to the websites and mobile apps, they offer a [paid API](https://api-public.airhealthservices.au/docs/) for data access.
- It provides 3-day forecasts (today, tomorrow, day after) with severity levels (Low, Medium, High, etc.) across Australia. See summary below or their [docs](https://api-public.airhealthservices.au/docs/#endpoint-specs) for full details.
- This repository is a community-maintained [HACS](https://www.hacs.xyz/) custom integration for bringing the API data feed into [Home Assistant](https://www.home-assistant.io/). It is not maintained by Airhealth.
- This enables automations to manage air quality exposure, such as controlling air purifiers, notifications, and window operation.

## Sensor Overview
| Category | Details | Updated (AEST) |
|--------|----------|----------------|
| 🌿 Grass pollen | — | 7:30 AM daily |
| 🌸 Other allergens | Tree pollen (Birch, Cypress, Eucalypt, Olive, Plane), weed pollen (Plantain), and fungal spores (Alternaria) | 9:00 AM daily |
| 💨 Air quality | PM2.5, O3 | 9:00 AM, 1:00 PM, 5:00 PM, 9:00 PM daily |
| 🔥 Woodsmoke | — | 9:00 AM daily |


## Requirements

- Home Assistant + [HACS](https://www.hacs.xyz/)
- AirHealth account and API subscription - [get one here](https://api-public.airhealthservices.au/docs/) (paid service)

## Installation

1. HACS → Integrations → ⋮ → Custom repositories
2. Add `https://github.com/OkhammahkO/airhealth_for_hacs_ha` as an Integration
3. Install "AirHealth" and restart Home Assistant
4. Settings → Devices & Services → Add Integration → search "AirHealth"
5. Enter your API key and [SAL code](https://api-public.airhealthservices.au/docs/#find-location) (your location ID), then select your subscribed endpoints

## Support

- [Home Assistant Community thread](https://community.home-assistant.io/t/airhealth-hacs-integration-australian-pollen-air-quality/1001501/1) — questions, discussion, feedback
- [Open an issue](https://github.com/OkhammahkO/airhealth_for_hacs_ha/issues) — bugs & feature requests

## License

MIT

---

*Vibe coded with Claude. Use at your own risk.*