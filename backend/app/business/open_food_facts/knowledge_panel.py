import logging
from http.client import HTTPException

import httpx
from pydantic import ValidationError

from app.config.exceptions import ResourceNotFoundException
from app.enums.open_food_facts.enums import (
    LAYING_HEN_FURNISHED_CAGE_TAGS,
    LAYING_HEN_PAIN_FOR_100G,
    AnimalType,
    LayingHenBreedingType,
    PainType,
)
from app.schemas.open_food_facts.external import ProductData, ProductResponse
from app.schemas.open_food_facts.internal import (
    AnimalBreedingType,
    AnimalPainDuration,
    AnimalProductWeight,
    PainCategory,
    PainReport,
)

logger = logging.getLogger("app")


async def get_data_from_off(barcode: str) -> ProductData:
    """
    Retrieve useful product data from OFF to compute the breeding type and the weight of animal product

    We actually use the OFF Search-a-licious API.

    :param barcode: The product barcode
    :return: A ProductResponse containing the product data
    """
    url = "https://search.openfoodfacts.org/search"
    tags = ["categories_tags", "labels_tags"]
    params = {"q": f"code:{barcode}", "fields": ",".join(tags)}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
        except HTTPException as e:
            logger.warning(f"Product not found: {barcode}")
            raise ResourceNotFoundException(f"Product not found: {barcode}") from e

    try:
        product_response = ProductResponse.model_validate(response.json())
    except ValidationError as e:
        logger.error(f"Failed to validate product data: {e}")
        # We want to return a clean response to OFF
        raise ResourceNotFoundException(f"Product not found: {barcode}") from e

    if not product_response.hits:
        logger.warning(f"No hits found for params: {params}")
        raise ResourceNotFoundException(f"Product not found: {barcode}")

    product_data = product_response.hits[0]
    logger.warning(f"Product data: {product_data}")
    return product_data


async def compute_breeding_type(product_data: ProductData) -> AnimalBreedingType:
    breading_types = AnimalBreedingType()

    if any(tag in product_data.categories_tags for tag in LAYING_HEN_FURNISHED_CAGE_TAGS):
        breading_types.laying_hen_breeding_type = LayingHenBreedingType.FURNISHED_CAGE

    return breading_types


async def compute_weight(product_data: ProductData) -> AnimalProductWeight:
    # TODO
    return AnimalProductWeight(
        egg_weight=200,
    )


def have_breading_type(breading_type: AnimalBreedingType) -> bool:
    return breading_type.laying_hen_breeding_type or breading_type.broiler_chicken_breeding_type


def have_weight(weight: AnimalProductWeight) -> bool:
    return weight.egg_weight or weight.chicken_weight


def get_pain_report_from_breading_type_and_weight(
        breeding_type: AnimalBreedingType,
        weight: AnimalProductWeight
) -> PainReport:

    laying_hen_pain_data = None
    if breeding_type.laying_hen_breeding_type:
        laying_hen_pain_data = LAYING_HEN_PAIN_FOR_100G[breeding_type.laying_hen_breeding_type]

    return PainReport(
        pain_categories=[
            PainCategory(
                pain_type=pain_type,
                animals=[
                    AnimalPainDuration(
                        animal_type=AnimalType.LAYING_HEN,
                        seconds_in_pain=laying_hen_pain_data[pain_type] * weight.egg_weight
                    )
                ]
            )
            for pain_type in PainType
        ]
    )


async def compute_suffering_footprint(barcode: str) -> PainReport | None:
    product_data = await get_data_from_off(barcode)

    breeding_type = await compute_breeding_type(product_data)
    weight = await compute_weight(product_data)

    if not have_breading_type(breeding_type) or not have_weight(weight):
        return None

    return get_pain_report_from_breading_type_and_weight(breeding_type, weight)
