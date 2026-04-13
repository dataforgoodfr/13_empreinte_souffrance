import logging
from typing import Callable, List

import httpx
from pydantic import ValidationError

from app.business.open_food_facts.egg_knowledge_panel_generator import EggKnowledgePanelGenerator
from app.business.open_food_facts.pain_report_calculator import PainReportCalculator
from app.config.exceptions import EggButNotFreshEgg, ResourceNotFoundException
from app.enums.open_food_facts.enums import AnimalType
from app.schemas.open_food_facts.external import ProductData, ProductResponse, ProductResponseSearchALicious
from app.schemas.open_food_facts.internal import (
    KnowledgePanelResponse,
    PainReport,
    ProductType,
)

logger = logging.getLogger("app")


async def get_data_from_off_v3(barcode: str, locale: str) -> ProductData:
    """
    Retrieve useful product data from OFF API v3 to compute the breeding type and the quantity of animal product

    If an error occurs, we raise a ResourceNotFoundException to return a clean response to OFF

    Args:
        barcode: The product barcode
        locale: alpha2 locale (fr, en...)
    Returns:
        A ProductData containing the name, image_url, categories, labels tags and other tags
    Raises:
        ResourceNotFoundException: If the product cannot be found or data validation fails
    """
    url = f"https://world.openfoodfacts.org/api/v3/product/{barcode}.json"
    product_name_with_locale = f"product_name_{locale}"

    try:
        async with httpx.AsyncClient(
            headers={"User-Agent": "my-app/1.0"},
            follow_redirects=True,
            timeout=20.0,
        ) as client:
            response = await client.get(url)
            response.raise_for_status()
            json_response = response.json()

    except Exception as e:
        logger.warning(f"OFF API error: {type(e).__name__}: {e}")
        raise ResourceNotFoundException(f"Can't get product data from OFF API: {barcode}") from e

    if product := json_response.get("product"):
        if product_name_with_locale in product:
            product["product_name"] = product[product_name_with_locale]
    else:
        raise ResourceNotFoundException(f"No hits returned by OFF API: {barcode}")

    try:
        product_response = ProductResponse.model_validate(json_response)
    except Exception as e:
        logger.error(f"Failed to validate product data: {e}")
        raise ResourceNotFoundException(f"Failed to validate product data retrieved from OFF: {barcode}") from e

    return product_response.product


async def get_data_from_off_search_a_licious(barcode: str, locale: str) -> ProductData:
    """
    Retrieve useful product data from OFF search-a-licious API
    to compute the breeding type and the quantity of animal product

    If an error occurs, we raise a ResourceNotFoundException to return a clean response to OFF

    Args:
        barcode: The product barcode
        locale: alpha2 locale (fr, en...)
    Returns:
        A ProductData containing the name, image_url, categories and labels tags
    Raises:
        ResourceNotFoundException: If the product cannot be found or data validation fails
    """
    url = "https://search.openfoodfacts.org/search"
    product_name_with_locale = f"product_name_{locale}"
    tags = [
        "categories_tags",
        "labels_tags",
        "image_url",
        "product_name",
        product_name_with_locale,
        "product_quantity_unit",
        "product_quantity",
        "quantity",
        "allergens_tags",
        "ingredients_tags",
        "ingredients",
        "countries",
        "countries_tags",
    ]
    params = {"q": f"code:{barcode}", "fields": ",".join(tags)}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()  # Raise exception for 4XX/5XX responses
            json_response = response.json()
    except Exception as e:
        logger.warning(f"Can't get product data from OFF search-a-licious API: {barcode}")
        raise ResourceNotFoundException(f"Can't get product data from OFF API: {barcode}") from e

    hits = json_response.get("hits")
    if hits and isinstance(hits, list) and product_name_with_locale in hits[0]:
        hits[0]["product_name"] = hits[0][product_name_with_locale]

    try:
        product_response = ProductResponseSearchALicious.model_validate(json_response)
    except ValidationError as e:
        logger.error(f"Failed to validate product data: {e}")
        raise ResourceNotFoundException(f"Failed to validate product data retrieved from OFF: {barcode}") from e

    if not product_response.hits:
        logger.warning(f"No hits found for params: {params}")
        raise ResourceNotFoundException(f"No hits returned by OFF API: {barcode}")

    product_data = product_response.hits[0]

    return product_data


async def get_pain_reports(barcode: str, locale: str) -> List[PainReport]:
    """
    Compute the pain reports list for a product based on its barcode

    Args:
        barcode: The product barcode
        locale: alpha2 locale (fr, en...)

    Returns:
        A list of PainReport objects
    """
    # Get the product data
    product_data = await get_data_from_off_v3(barcode, locale)

    try:
        # Create calculator with the retrieved data
        calculator = PainReportCalculator(product_data)

    except EggButNotFreshEgg as e:
        return [e.pain_report]
    # Generate and return the pain report
    # For no fresh chicken eggs return empty list to display a specific knowledge panel
    pain_reports = calculator.get_pain_reports()

    return pain_reports


def resolve_product_type(pain_reports: List[PainReport]) -> ProductType:
    """
    Determine the product type from pain reports.
    """
    if not pain_reports:
        raise ResourceNotFoundException("No pain reports")

    product_type = pain_reports[0].product_type

    return product_type


def get_generator(
    pain_reports: List[PainReport], product_type: ProductType, locale: str, translator: tuple[Callable, Callable]
):
    """
    Return the appropriate generator depending on product type.
    """

    if product_type.is_mixed is False and AnimalType.LAYING_HEN in product_type.animal_types:
        return EggKnowledgePanelGenerator(
            pain_reports=pain_reports,
            locale=locale,
            translator=translator,
        )

    raise ResourceNotFoundException(f"Unsupported product type: {product_type}")


def get_knowledge_panel_response(
    pain_reports: List[PainReport], translator: tuple[Callable, Callable], locale: str
) -> KnowledgePanelResponse:
    """
    Create a complete knowledge panel response with all panels related to suffering footprint.

    Args:
        pain_reports: A list of pain reports containing all animal data and pain durations
        translator: The translation function to use for i18n

    Returns:
        A complete KnowledgePanelResponse containing root panel, intensity definitions,
        physical pain data and psychological pain data
    """

    product_type = resolve_product_type(pain_reports)
    panel_generator = get_generator(pain_reports, product_type, locale, translator)

    return panel_generator.get_response()
