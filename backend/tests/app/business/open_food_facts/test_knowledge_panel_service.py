import asyncio
from typing import Callable
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import httpx
import pytest

from app.business.open_food_facts.knowledge_panel_service import (
    get_data_from_off_search_a_licious,
    get_data_from_off_v3,
    get_generator,
    get_knowledge_panel_response,
    get_pain_reports,
    get_pain_reports_batch,
)
from app.config.exceptions import ResourceNotFoundException
from app.config.i18n import I18N
from app.enums.open_food_facts.enums import AnimalType
from app.schemas.open_food_facts.external import ProductData
from app.schemas.open_food_facts.internal import PainReport, ProductType


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


# --- get_pain_reports (isolated from the API layer) ---


@pytest.mark.asyncio
async def test_get_pain_reports_returns_computed_report(sample_product_data: ProductData):
    """Test that get_pain_reports returns a fully computed PainReport for a supported product"""
    with patch(
        "app.business.open_food_facts.knowledge_panel_service.get_data_from_off_v3",
        new_callable=AsyncMock,
        return_value=sample_product_data,
    ):
        result = await get_pain_reports(barcode="123456789", locale="en")

    assert result.product_type == ProductType(is_mixed=False, animal_types={AnimalType.LAYING_HEN})
    assert len(result.scenarios) == 1


@pytest.mark.asyncio
async def test_get_pain_reports_returns_empty_scenarios_for_egg_but_not_fresh_egg(liquid_eggs_product: ProductData):
    """
    Test that get_pain_reports catches EggButNotFreshEgg raised by the calculator
    and returns the pre-built PainReport with empty scenarios, instead of propagating the exception.
    """
    with patch(
        "app.business.open_food_facts.knowledge_panel_service.get_data_from_off_v3",
        new_callable=AsyncMock,
        return_value=liquid_eggs_product,
    ):
        result = await get_pain_reports(barcode="123456789", locale="en")

    assert result.scenarios == []
    assert result.product_name == "Liquid Eggs"


@pytest.mark.asyncio
async def test_get_pain_reports_propagates_resource_not_found(sample_product_data: ProductData):
    """Test that get_pain_reports lets ResourceNotFoundException from the OFF fetch bubble up unchanged"""
    with patch(
        "app.business.open_food_facts.knowledge_panel_service.get_data_from_off_v3",
        new_callable=AsyncMock,
        side_effect=ResourceNotFoundException("barcode not found"),
    ):
        with pytest.raises(ResourceNotFoundException, match="barcode not found"):
            await get_pain_reports(barcode="000000000", locale="en")


# --- get_pain_reports_batch ---


@pytest.mark.asyncio
async def test_get_pain_reports_batch_isolates_failures(sample_product_data: ProductData):
    """A failing barcode must not affect the results of the others in the same batch"""

    async def fake_get_data(barcode: str, locale: str):
        if barcode == "bad":
            raise ResourceNotFoundException(f"Can't get product data from OFF API: {barcode}")
        return sample_product_data

    with patch(
        "app.business.open_food_facts.knowledge_panel_service.get_data_from_off_v3",
        new_callable=AsyncMock,
        side_effect=fake_get_data,
    ):
        results = await get_pain_reports_batch(barcodes=["good1", "bad", "good2"], locale="en")

    assert isinstance(results["good1"], PainReport)
    assert isinstance(results["good2"], PainReport)
    assert isinstance(results["bad"], ResourceNotFoundException)


@pytest.mark.asyncio
async def test_get_pain_reports_batch_runs_concurrently(sample_product_data: ProductData):
    """Test that barcodes are fetched in parallel rather than sequentially"""
    call_order: list[str] = []

    async def fake_get_data(barcode: str, locale: str):
        call_order.append(f"start-{barcode}")
        # Reverse the completion order to prove tasks aren't awaited one-by-one
        await asyncio.sleep(0.02 if barcode == "first" else 0)
        call_order.append(f"end-{barcode}")
        return sample_product_data

    with patch(
        "app.business.open_food_facts.knowledge_panel_service.get_data_from_off_v3",
        new_callable=AsyncMock,
        side_effect=fake_get_data,
    ):
        results = await get_pain_reports_batch(barcodes=["first", "second"], locale="en")

    assert set(results.keys()) == {"first", "second"}
    # Both starts happen before the slower one ends, proving concurrent execution
    assert call_order.index("start-second") < call_order.index("end-first")


# --- get_generator ---


def test_get_generator_returns_egg_generator_for_single_laying_hen(pain_report: PainReport):
    translator = I18N().get_translator(locale="en")
    product_type = ProductType(is_mixed=False, animal_types={AnimalType.LAYING_HEN})

    generator = get_generator(pain_report, product_type, locale="en", translator=translator)

    assert generator.__class__.__name__ == "EggKnowledgePanelGenerator"


@pytest.mark.parametrize(
    "product_type",
    [
        ProductType(is_mixed=False, animal_types={AnimalType.BROILER_CHICKEN}),
        ProductType(is_mixed=True, animal_types={AnimalType.LAYING_HEN, AnimalType.BROILER_CHICKEN}),
        ProductType(is_mixed=False, animal_types=set()),
    ],
)
def test_get_generator_raises_for_unsupported_product_type(pain_report: PainReport, product_type: ProductType):
    """
    Test that get_generator refuses any product type it doesn't have a renderer for
    (mixed products, or single animal types other than laying hen), instead of silently
    falling through to the wrong panel.
    """
    translator = I18N().get_translator(locale="en")

    with pytest.raises(ResourceNotFoundException, match="Unsupported product type"):
        get_generator(pain_report, product_type, locale="en", translator=translator)
