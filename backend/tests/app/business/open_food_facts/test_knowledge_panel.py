from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from app.business.open_food_facts.knowledge_panel import PainReportCalculator, get_data_from_off
from app.config.exceptions import ResourceNotFoundException
from app.enums.open_food_facts.enums import LayingHenBreedingType
from app.schemas.open_food_facts.external import ProductData
from app.schemas.open_food_facts.internal import AnimalBreedingType, AnimalProductWeight


@pytest.mark.asyncio
async def test_get_data_from_off_success():
    """Test when the OFF API returns valid data"""
    barcode = "123456789"
    mock_response_data = {
        "hits": [{"categories_tags": ["en:cage-chicken-eggs", "other"], "labels_tags": ["organic"]}]
    }

    mock_response = AsyncMock()
    mock_response.json = MagicMock(return_value=mock_response_data)

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        result = await get_data_from_off(barcode)

    assert result == ProductData.model_validate(mock_response_data["hits"][0])


@pytest.mark.asyncio
async def test_get_data_from_off_no_hits():
    """Test when the OFF API returns no hits"""
    barcode = "000000000"
    mock_response_data = {"hits": []}

    mock_response = AsyncMock()
    mock_response.json = MagicMock(return_value=mock_response_data)

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        with pytest.raises(ResourceNotFoundException, match=f"Product not found: {barcode}"):
            await get_data_from_off(barcode)


@pytest.mark.asyncio
async def test_get_data_from_off_validation_error():
    """Test when the OFF API returns invalid data"""
    barcode = "999999999"
    mock_response_data = {"invalid_key": "invalid_value"}

    mock_response = AsyncMock()
    mock_response.json = MagicMock(return_value=mock_response_data)

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        with pytest.raises(ResourceNotFoundException, match=f"Product not found: {barcode}"):
            await get_data_from_off(barcode)


@pytest.mark.asyncio
async def test_get_data_from_off_http_exception():
    """Test when the OFF API returns an HTTP error"""
    barcode = "111111111"

    with patch("httpx.AsyncClient.get", side_effect=httpx.ReadTimeout("Network error")):
        with pytest.raises(ResourceNotFoundException, match=f"Product not found: {barcode}"):
            await get_data_from_off(barcode)


@pytest.mark.asyncio
async def test_compute_weight(product_data: ProductData):
    calculator = PainReportCalculator(product_data)

    result = calculator.compute_weights()
    assert result == AnimalProductWeight(egg_weight=200)


@pytest.mark.asyncio
async def test_compute_breading_type(product_data: ProductData):
    # product_data fixture contains the `en:cage-chicken-eggs` tag
    calculator = PainReportCalculator(product_data)

    result = calculator.compute_breeding_types()
    assert result == AnimalBreedingType(laying_hen_breeding_type=LayingHenBreedingType.FURNISHED_CAGE)
