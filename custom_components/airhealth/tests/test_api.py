"""Test AirHealth API client."""

from unittest.mock import AsyncMock

import aiohttp
import pytest

from custom_components.airhealth.api import (
    AirHealthApiClient,
    AirHealthAuthError,
    AirHealthDataError,
)


@pytest.fixture
def mock_session():
    """Create a mock aiohttp session."""
    return AsyncMock(spec=aiohttp.ClientSession)


@pytest.fixture
def api_client(mock_session):
    """Create an API client instance."""
    return AirHealthApiClient("test_api_key", mock_session)


async def test_async_get_data_success(api_client, mock_session):
    """Test successful API data fetch."""
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json = AsyncMock(
        return_value={
            "forecasts": [
                {"day": 0, "level": "Low"},
                {"day": 1, "level": "Moderate"},
            ]
        }
    )

    mock_session.get.return_value.__aenter__.return_value = mock_response

    result = await api_client.async_get_data("/forecast/grass", "12345")

    assert result == {
        "forecasts": [
            {"day": 0, "level": "Low"},
            {"day": 1, "level": "Moderate"},
        ]
    }
    mock_session.get.assert_called_once()
    args, kwargs = mock_session.get.call_args
    assert args[0] == "https://api-public.airhealthservices.au/api/forecast/grass?sal=12345"
    assert kwargs["headers"]["Authorization"] == "Api-Key test_api_key"


async def test_async_get_data_auth_error_401(api_client, mock_session):
    """Test API authentication error with 401 status."""
    mock_response = AsyncMock()
    mock_response.status = 401

    mock_session.get.return_value.__aenter__.return_value = mock_response

    with pytest.raises(AirHealthAuthError) as exc_info:
        await api_client.async_get_data("/forecast/grass", "12345")

    assert "API Key or SAL code is invalid" in str(exc_info.value)


async def test_async_get_data_auth_error_403(api_client, mock_session):
    """Test API authentication error with 403 status."""
    mock_response = AsyncMock()
    mock_response.status = 403

    mock_session.get.return_value.__aenter__.return_value = mock_response

    with pytest.raises(AirHealthAuthError) as exc_info:
        await api_client.async_get_data("/forecast/grass", "12345")

    assert "API Key or SAL code is invalid" in str(exc_info.value)


async def test_async_get_data_error_404(api_client, mock_session):
    """Test API data error with 404 status."""
    mock_response = AsyncMock()
    mock_response.status = 404
    mock_response.text = AsyncMock(return_value="Not found")

    mock_session.get.return_value.__aenter__.return_value = mock_response

    with pytest.raises(AirHealthDataError) as exc_info:
        await api_client.async_get_data("/forecast/invalid", "12345")

    assert "API request failed with status: 404" in str(exc_info.value)


async def test_async_get_data_error_500(api_client, mock_session):
    """Test API data error with 500 status."""
    mock_response = AsyncMock()
    mock_response.status = 500
    mock_response.text = AsyncMock(return_value="Internal server error")

    mock_session.get.return_value.__aenter__.return_value = mock_response

    with pytest.raises(AirHealthDataError) as exc_info:
        await api_client.async_get_data("/forecast/grass", "12345")

    assert "API request failed with status: 500" in str(exc_info.value)


async def test_async_get_data_network_timeout(api_client, mock_session):
    """Test API network timeout."""
    mock_session.get.side_effect = aiohttp.ClientError("Connection timeout")

    with pytest.raises(aiohttp.ClientError):
        await api_client.async_get_data("/forecast/grass", "12345")


async def test_async_get_data_url_construction(api_client, mock_session):
    """Test correct URL construction for different endpoints."""
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value={})

    mock_session.get.return_value.__aenter__.return_value = mock_response

    # Test grass endpoint
    await api_client.async_get_data("/forecast/grass", "12345")
    args, _ = mock_session.get.call_args
    assert args[0] == "https://api-public.airhealthservices.au/api/forecast/grass?sal=12345"

    # Test other allergens endpoint
    await api_client.async_get_data("/forecast/other", "67890")
    args, _ = mock_session.get.call_args
    assert args[0] == "https://api-public.airhealthservices.au/api/forecast/other?sal=67890"

    # Test air quality endpoint
    await api_client.async_get_data("/forecast/airquality", "11111")
    args, _ = mock_session.get.call_args
    assert args[0] == "https://api-public.airhealthservices.au/api/forecast/airquality?sal=11111"


async def test_async_get_data_authorization_header(api_client, mock_session):
    """Test correct authorization header format."""
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value={})

    mock_session.get.return_value.__aenter__.return_value = mock_response

    await api_client.async_get_data("/forecast/grass", "12345")

    _, kwargs = mock_session.get.call_args
    assert "headers" in kwargs
    assert "Authorization" in kwargs["headers"]
    assert kwargs["headers"]["Authorization"] == "Api-Key test_api_key"


async def test_async_get_data_json_parsing(api_client, mock_session):
    """Test JSON parsing of successful response."""
    test_data = {
        "forecasts": [
            {
                "day": 0,
                "level": "Moderate",
                "allergens": {
                    "birch": 2,
                    "plantain": 1,
                },
            }
        ],
        "issued": "2024-12-06T07:00:00Z",
    }

    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=test_data)

    mock_session.get.return_value.__aenter__.return_value = mock_response

    result = await api_client.async_get_data("/forecast/other", "12345")

    assert result == test_data
    assert result["forecasts"][0]["allergens"]["birch"] == 2
    assert result["issued"] == "2024-12-06T07:00:00Z"


async def test_api_client_initialization():
    """Test API client initialization."""
    session = AsyncMock(spec=aiohttp.ClientSession)
    client = AirHealthApiClient("my_api_key", session)

    assert client._api_key == "my_api_key"
    assert client._session is session
    assert client.BASE_URL == "https://api-public.airhealthservices.au/api"
