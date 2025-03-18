from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from app.business.open_food_facts.knowledge_panel import get_data_from_off
from app.business.open_food_facts.pain_report_calculator import PainReportCalculator
from app.config.exceptions import ResourceNotFoundException
from app.enums.open_food_facts.enums import AnimalType, LayingHenBreedingType
from app.schemas.open_food_facts.external import ProductData
from app.schemas.open_food_facts.internal import BreedingTypeAndWeight


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
        with pytest.raises(ResourceNotFoundException, match=f"No hits returned by OFF API: {barcode}"):
            await get_data_from_off(barcode)


@pytest.mark.asyncio
async def test_get_data_from_off_validation_error():
    """Test when the OFF API returns invalid data"""
    barcode = "999999999"
    mock_response_data = {"invalid_key": "invalid_value"}

    mock_response = AsyncMock()
    mock_response.json = MagicMock(return_value=mock_response_data)

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        with pytest.raises(
                ResourceNotFoundException,
                match=f"Failed to validate product data retrieved from OFF: {barcode}"
        ):
            await get_data_from_off(barcode)


@pytest.mark.asyncio
async def test_get_data_from_off_http_call_exception():
    """Test when the OFF API returns an HTTP error"""
    barcode = "111111111"

    with patch("httpx.AsyncClient.get", side_effect=httpx.ReadTimeout("Network error")):
        with pytest.raises(ResourceNotFoundException, match=f"Can't get product data from OFF API: {barcode}"):
            await get_data_from_off(barcode)


@pytest.mark.asyncio
async def test_compute_weight(product_data: ProductData):
    calculator = PainReportCalculator(product_data)

    breeding_types = calculator._get_breeding_types()
    with patch("app.business.open_food_facts.knowledge_panel.randint", return_value=200):
        result = calculator._get_breeding_types_with_weights(breeding_types)

    # product_data fixture contains the `en:cage-chicken-eggs` tag
    assert result == [
        BreedingTypeAndWeight(
            animal_type=AnimalType.LAYING_HEN,
            breeding_type=LayingHenBreedingType.FURNISHED_CAGE,
            animal_product_weight=200,
        )
    ]


@pytest.mark.asyncio
async def test_compute_breading_type(product_data: ProductData):
    # product_data fixture contains the `en:cage-chicken-eggs` tag
    calculator = PainReportCalculator(product_data)

    result = calculator._get_breeding_types()
    assert result == [
        BreedingTypeAndWeight(animal_type=AnimalType.LAYING_HEN, breeding_type=LayingHenBreedingType.FURNISHED_CAGE)
    ]
