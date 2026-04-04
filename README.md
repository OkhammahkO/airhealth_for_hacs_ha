# AirHealth for Home Assistant
> Australian pollen & air quality forecasts

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![Built with Claude Code](https://img.shields.io/badge/built%20with-Claude-blueviolet)](https://claude.ai)

- AirHealth is the company behind [Melbourne Pollen](https://www.melbournepollen.com.au/) (and its sister sites).
- In addition to the websites and mobile apps, they offer a [paid API](https://api-public.airhealthservices.au/docs/) for data access.
- This repo is a [HACS](https://www.hacs.xyz/) custom component for integrating this data into [Home Assistant](https://www.home-assistant.io/).
- AirHealth provides 3-day forecasts (today, tomorrow, in 2 days) with "levels":

| Sensor | Details | Updated (AEST) |
|--------|----------|----------------|
| 🌿 Grass pollen | — | 7:30 AM daily |
| 🌸 Other allergens | Alternaria, Olive, Eucalypts, more | 9:00 AM daily |
| 💨 Air quality | PM2.5, O3 | 9:00 AM, 1:00 PM, 5:00 PM, 9:00 PM daily |
| 🔥 Woodsmoke | — | 9:00 AM daily |

## Requirements

- Home Assistant + [HACS](https://www.hacs.xyz/)
- AirHealth API subscription — [get one here](https://www.airhealthlab.com/index.php/airhealth-api) (paid service)

## Installation

1. HACS → Integrations → ⋮ → Custom repositories
2. Add `https://github.com/OkhammahkO/airhealth_for_hacs_ha` as an Integration
3. Install "AirHealth" and restart Home Assistant
4. Settings → Devices & Services → Add Integration → search "AirHealth"
5. Enter your API key and [SAL code](https://api-public.airhealthservices.au/docs/#find-location) (your location ID), then select your subscribed endpoints

## Support

- [Home Assistant Community thread](https://community.home-assistant.io/t/placeholder) — questions, discussion, feedback
- [Open an issue](https://github.com/OkhammahkO/airhealth_for_hacs_ha/issues) — bugs & feature requests

## License

MIT

---

*Vibe coded with Claude. Use at your own risk.*