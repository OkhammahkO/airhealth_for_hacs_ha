"""Fixtures for AirHealth tests."""

from collections.abc import Generator
from unittest.mock import AsyncMock, patch

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.airhealth.const import (
    CONF_API_KEY,
    CONF_SAL_CODE,
    DOMAIN,
    ENDPOINT_AQ_WOODSMOKE,
    ENDPOINT_GRASS_POLLEN,
    ENDPOINT_OTHER_ALLERGENS,
)


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Enable custom integrations."""
    yield


@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    """Return mock config entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        title="AirHealth (SAL 12345)",
        data={
            CONF_API_KEY: "test_key",
            CONF_SAL_CODE: "12345",
            ENDPOINT_GRASS_POLLEN: True,
            ENDPOINT_OTHER_ALLERGENS: True,
            ENDPOINT_AQ_WOODSMOKE: True,
        },
        unique_id="12345",
    )


@pytest.fixture
def mock_airhealth_api() -> Generator[AsyncMock]:
    """Mock AirHealthApiClient."""
    with patch("custom_components.airhealth.AirHealthApiClient", autospec=True) as mock:
        client = mock.return_value

        async def mock_get_data(path: str, sal_code: str):
            if "grass-pollen" in path:
                return {
                    "sal": sal_code,
                    "forecast": [
                        {"date": "2025-12-04", "grass_level": "Low"},
                        {"date": "2025-12-05", "grass_level": "Moderate"},
                        {"date": "2025-12-06", "grass_level": "High"},
                    ],
                }
            if "other-allergens" in path:
                return {
                    "sal": sal_code,
                    "forecast": [
                        {
                            "date": "2025-12-04",
                            "overall_level": "Low",
                            "allergens": [
                                {"name": "Plantain", "level": "Low"},
                                {"name": "Birch", "level": "Low"},
                            ],
                        },
                        {
                            "date": "2025-12-05",
                            "overall_level": "Moderate",
                            "allergens": [
                                {"name": "Plantain", "level": "Moderate"},
                                {"name": "Birch", "level": "Low"},
                            ],
                        },
                        {
                            "date": "2025-12-06",
                            "overall_level": "High",
                            "allergens": [
                                {"name": "Plantain", "level": "High"},
                                {"name": "Birch", "level": "Moderate"},
                            ],
                        },
                    ],
                }
            return {
                "sal": sal_code,
                "forecast": [
                    {
                        "date": "2025-12-04",
                        "aq_level": "Good",
                        "woodsmoke_level": "Low",
                        "supporting_data": [
                            {"name": "PM2.5", "level": "Good"},
                            {"name": "O3", "level": "Good"},
                        ],
                    },
                    {
                        "date": "2025-12-05",
                        "aq_level": "Fair",
                        "woodsmoke_level": "Moderate",
                        "supporting_data": [
                            {"name": "PM2.5", "level": "Fair"},
                            {"name": "O3", "level": "Good"},
                        ],
                    },
                    {
                        "date": "2025-12-06",
                        "aq_level": "Poor",
                        "woodsmoke_level": "High",
                        "supporting_data": [
                            {"name": "PM2.5", "level": "Poor"},
                            {"name": "O3", "level": "Fair"},
                        ],
                    },
                ],
            }

        client.async_get_data = AsyncMock(side_effect=mock_get_data)
        yield mock
