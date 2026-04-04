"""Constants for the AirHealth integration."""

from typing import Any

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
        "update_times": [(7, 30)],
    },
    ENDPOINT_OTHER_ALLERGENS: {
        "path": "/v1/other-allergens",
        "update_times": [(9, 0)],
    },
    ENDPOINT_AQ_WOODSMOKE: {
        "path": "/v1/aq-woodsmoke",
        "update_times": [(9, 0), (13, 0), (17, 0), (21, 0)],
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


def summarize_grass_pollen(level: str | None) -> str:
    """Generate summary for grass pollen level.

    Args:
        level: Grass pollen level (Low, Moderate, High, Extreme, None)

    Returns:
        Natural language summary (e.g., "Grass pollen is moderate")
    """
    if not level:
        return "Grass pollen is none"

    return f"Grass pollen is {level.lower()}"


def summarize_allergen_breakdown(
    overall_level: str | None,
    allergens: list[dict[str, Any]] | None
) -> str:
    """Generate summary for other allergens with selective breakdown.

    Args:
        overall_level: Overall allergen level
        allergens: List of allergen dicts with 'name' and 'level' keys

    Returns:
        Natural language summary following these rules:
        - None/Low: Just overall level, no sub-items
        - Moderate: Overall + moderate allergens only
        - High: Overall + high allergens only
        - Extreme: Overall + extreme AND high allergens

    Examples:
        >>> summarize_allergen_breakdown("Moderate", [
        ...     {"name": "Plantain", "level": "Moderate"},
        ...     {"name": "Birch", "level": "Low"}
        ... ])
        "Other allergens are moderate. Plantain is moderate"

        >>> summarize_allergen_breakdown("Extreme", [
        ...     {"name": "Birch", "level": "Extreme"},
        ...     {"name": "Olive", "level": "Extreme"},
        ...     {"name": "Plantain", "level": "High"},
        ...     {"name": "Cypress", "level": "Moderate"}
        ... ])
        "Other allergens are extreme. Birch and olive are extreme, and plantain is high"
    """
    if not overall_level:
        return "Other allergens are none"

    overall_lower = overall_level.lower()
    base = f"Other allergens are {overall_lower}"

    # For None/Low, return just the base (no sub-items)
    if not allergens or overall_level in ("None", "Low"):
        return base

    # Determine which levels to show based on overall level
    if overall_level == "Moderate":
        levels_to_show = ["Moderate"]
    elif overall_level == "High":
        levels_to_show = ["High"]
    elif overall_level == "Extreme":
        levels_to_show = ["Extreme", "High"]
    else:
        return base  # Fallback for unexpected levels

    # Group allergens by level (only include levels we want to show)
    level_groups: dict[str, list[str]] = {}
    for allergen in allergens:
        name = allergen.get("name", "Unknown")
        level = allergen.get("level", "Unknown")
        if level in levels_to_show:
            if level not in level_groups:
                level_groups[level] = []
            level_groups[level].append(name.lower())

    # Build sub-item text for each level group
    parts = []
    for level in ["Extreme", "High", "Moderate"]:  # Order matters for Extreme level
        if level not in level_groups:
            continue

        names = level_groups[level]
        level_lower = level.lower()

        if len(names) == 1:
            parts.append(f"{names[0]} is {level_lower}")
        elif len(names) == 2:
            parts.append(f"{names[0]} and {names[1]} are {level_lower}")
        else:
            # 3+ items: use Oxford comma
            names_str = ", ".join(names[:-1]) + f", and {names[-1]}"
            parts.append(f"{names_str} are {level_lower}")

    # Join parts with proper grammar
    if not parts:
        return base  # No allergens at relevant levels

    if len(parts) == 1:
        breakdown = parts[0]
    else:
        # Multiple level groups: separate with ", and"
        breakdown = ", and ".join(parts)

    return f"{base}. {breakdown.capitalize()}"
