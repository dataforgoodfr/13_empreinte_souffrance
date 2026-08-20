from typing import Callable
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import httpx
import pytest

from app.business.open_food_facts.knowledge_panel_service import (
    get_data_from_off_search_a_licious,
    get_data_from_off_v3,
    get_knowledge_panel_response,
)
from app.config.exceptions import ResourceNotFoundException
from app.config.i18n import I18N
from app.schemas.open_food_facts.external import ProductData
from app.schemas.open_food_facts.internal import PainReport


@pytest.mark.asyncio
async def test_get_data_from_off_search_a_licious_success():
    """Test when the OFF API returns valid data"""
    barcode = "123456789"
    mock_response_data = {
        "hits": [
            {
                "categories_tags": ["en:cage-chicken-eggs", "other"],
                "labels_tags": ["organic"],
                "product_name": "Fake product name",
                "image_url": "https://example.com/image.jpg",
            }
        ]
    }

    mock_response = AsyncMock()
    mock_response.json = MagicMock(return_value=mock_response_data)
    mock_response.raise_for_status = Mock(return_value=None)

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        result = await get_data_from_off_search_a_licious(barcode, locale="en")

    assert result == ProductData.model_validate(mock_response_data["hits"][0])


@pytest.mark.asyncio
async def test_get_data_from_off_v3_success(sample_product_data: ProductData):
    """Test when the OFF API returns valid data"""
    barcode = "123456789"
    mock_response_data = {"product": sample_product_data}

    mock_response = AsyncMock()
    mock_response.json = MagicMock(return_value=mock_response_data)
    mock_response.raise_for_status = Mock(return_value=None)

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        result = await get_data_from_off_v3(barcode, locale="en")

    assert result == sample_product_data


@pytest.mark.asyncio
async def test_get_data_from_off_search_a_licious_no_hits():
    """Test when the OFF API returns no hits"""
    barcode = "000000000"
    mock_response_data = {"hits": []}

    mock_response = AsyncMock()
    mock_response.json = MagicMock(return_value=mock_response_data)
    mock_response.raise_for_status = Mock(return_value=None)

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        with pytest.raises(ResourceNotFoundException, match=f"No hits returned by OFF API: {barcode}"):
            await get_data_from_off_search_a_licious(barcode, locale="en")


@pytest.mark.asyncio
@pytest.mark.parametrize("get_data_from_off_function", [get_data_from_off_search_a_licious, get_data_from_off_v3])
async def test_get_data_from_off_validation_error(get_data_from_off_function: Callable):
    """Test when the OFF API returns invalid data"""
    barcode = "999999999"
    mock_response_data = {"product": "invalid_value"}

    mock_response = AsyncMock()
    mock_response.json = MagicMock(return_value=mock_response_data)
    mock_response.raise_for_status = Mock(return_value=None)

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        with pytest.raises(
            ResourceNotFoundException, match=f"Failed to validate product data retrieved from OFF: {barcode}"
        ):
            await get_data_from_off_function(barcode, locale="en")


@pytest.mark.asyncio
@pytest.mark.parametrize("get_data_from_off_function", [get_data_from_off_search_a_licious, get_data_from_off_v3])
async def test_get_data_from_off_http_call_exception(get_data_from_off_function: Callable):
    """Test when the OFF API returns an HTTP error"""
    barcode = "111111111"

    with patch("app.config.http_client.client.get", side_effect=httpx.ReadTimeout("Network error")):
        with pytest.raises(ResourceNotFoundException, match=f"Can't get product data from OFF API: {barcode}"):
            await get_data_from_off_function(barcode, locale="en")


@pytest.mark.parametrize(
    "pain_report",
    ["pain_report", "pain_report_with_two_animals"],
    indirect=True,
)
def test_get_knowledge_panel_response(pain_report):
    """Test the get_knowledge_panel_response function"""
    translator = I18N().get_translator(locale="en")

    # Generate knowledge panel response using the function
    response = get_knowledge_panel_response(pain_report=pain_report, locale="en", translator=translator)

    # Verify response structure
    assert "root" in response.panels
    assert "project_panel" in response.panels

    # Verify each panel has the required fields
    for panel in response.panels.values():
        assert hasattr(panel, "elements")
        assert hasattr(panel, "title_element")


def test_get_knowledge_panel_response_missing_quantity(pain_report_missing_quantity: PainReport):
    """Test that only root panel is generated when quantity is missing"""
    translator = I18N().get_translator(locale="en")

    response = get_knowledge_panel_response(
        pain_report=pain_report_missing_quantity, locale="en", translator=translator
    )

    # Verify response structure
    assert "root" in response.panels
    assert "project_panel" in response.panels

    # Verify each panel has the required fields
    for panel in response.panels.values():
        assert hasattr(panel, "elements")
        assert hasattr(panel, "title_element")
