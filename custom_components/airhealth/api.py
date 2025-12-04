"""API for AirHealth."""
import logging
from typing import Any

import aiohttp

_LOGGER = logging.getLogger(__name__)

# Define custom exceptions for better error handling
class AirHealthApiException(Exception):
    """Base exception for AirHealth API errors."""

class AirHealthAuthError(AirHealthApiException):
    """Exception for authentication errors."""

class AirHealthDataError(AirHealthApiException):
    """Exception for data retrieval errors."""

class AirHealthApiClient:
    """Generic API Client for AirHealth."""

    BASE_URL = "https://api-public.airhealthservices.au/api"

    def __init__(self, api_key: str, session: aiohttp.ClientSession):
        """Initialize the API client."""
        self._api_key = api_key
        self._session = session

    async def async_get_data(self, endpoint_path: str, sal_code: str) -> dict[str, Any]:
        """Get data from a specific API endpoint."""
        url = f"{self.BASE_URL}{endpoint_path}?sal={sal_code}"
        headers = {"Authorization": f"Api-Key {self._api_key}"}

        _LOGGER.debug("Fetching data from: %s", url)
        async with self._session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            if response.status in (401, 403):
                raise AirHealthAuthError("API Key or SAL code is invalid.")
            _LOGGER.error(
                "Failed to fetch data from AirHealth API (%s): %s - %s",
                endpoint_path,
                response.status,
                await response.text(),
            )
            raise AirHealthDataError(f"API request failed with status: {response.status}")
