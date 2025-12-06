"""Constants for the AirHealth integration."""

DOMAIN = "airhealth"

# Configuration Keys
CONF_API_KEY = "api_key"
CONF_SAL_CODE = "sal_code"

# Endpoint Keys (used in config flow, API calls, and data parsing)
ENDPOINT_GRASS_POLLEN = "grass_pollen"
ENDPOINT_OTHER_ALLERGENS = "other_allergens"
ENDPOINT_AQ_WOODSMOKE = "aq_woodsmoke"

# All available endpoints with their API path and update times (AEST)
API_ENDPOINTS = {
    ENDPOINT_GRASS_POLLEN: {
        "path": "/v1/grass-pollen",
        "update_hour": 7,
        "update_minute": 30,
    },
    ENDPOINT_OTHER_ALLERGENS: {
        "path": "/v1/other-allergens",
        "update_hour": 9,
        "update_minute": 0,
    },
    ENDPOINT_AQ_WOODSMOKE: {
        "path": "/v1/aq-woodsmoke",
        "update_hour": 7,
        "update_minute": 0,
    },
}


def get_level_icon(level: str | None) -> str:
    """Return colored circle icon for level.

    Args:
        level: The level string (Low, Moderate, High, Extreme, None)

    Returns:
        Colored circle emoji representing the level
    """
    if not level:
        return "⚪"

    level_icons = {
        "Low": "🟢",
        "None": "🟢",
        "Moderate": "🟡",
        "High": "🟠",
        "Extreme": "🔴",
    }
    return level_icons.get(level, "⚪")
