import logging

import httpx
from httpx import RequestError
from pydantic import ValidationError

from app.config.exceptions import ResourceNotFoundException
from app.enums.open_food_facts.enums import (
    TAGS_BY_ANIMAL_TYPE_AND_BREEDING_TYPE,
    TIME_IN_PAIN_FOR_100G_IN_SECONDS,
    AnimalType,
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
    If an error occurs, we raise a ResourceNotFoundException to return a clean response to OFF

    Args:
        barcode: The product barcode
    Returns:
        A ProductData containing the categories and labels tags
    Raises:
        ResourceNotFoundException: If the product cannot be found or data validation fails
    """
    url = "https://search.openfoodfacts.org/search"
    tags = ["categories_tags", "labels_tags"]
    params = {"q": f"code:{barcode}", "fields": ",".join(tags)}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()  # Raise exception for 4XX/5XX responses
    except RequestError as e:
        logger.warning(f"Product not found: {barcode}")
        raise ResourceNotFoundException(f"Product not found: {barcode}") from e

    try:
        product_response = ProductResponse.model_validate(response.json())
    except ValidationError as e:
        logger.error(f"Failed to validate product data: {e}")
        raise ResourceNotFoundException(f"Product not found: {barcode}") from e

    if not product_response.hits:
        logger.warning(f"No hits found for params: {params}")
        raise ResourceNotFoundException(f"Product not found: {barcode}")

    product_data = product_response.hits[0]
    return product_data


class PainReportCalculator:
    """
    Class to calculate the pain report for an animal product.
    """

    def __init__(self, product_data: ProductData):
        """
        Initialize the calculator with product data.

        Args:
            product_data: ProductData instance containing categories_tags and labels_tags.
        """
        self.product_data = product_data
        self.breeding_types = self.compute_breeding_types()
        self.weights = self.compute_weights()

    def compute_breeding_types(self) -> AnimalBreedingType:
        """
        Compute the breeding types from product data.

        Returns:
            AnimalBreedingType object with detected breeding types
        """
        breeding_types = AnimalBreedingType()

        # Laying hens
        laying_hen_tags = TAGS_BY_ANIMAL_TYPE_AND_BREEDING_TYPE[AnimalType.LAYING_HEN]
        for breeding_type, tags in laying_hen_tags.items():
            if any(tag in self.product_data.categories_tags for tag in tags):
                # set the breeding type if any of the tags is present
                breeding_types.laying_hen_breeding_type = breeding_type
                break

        # Broiler chickens
        broiler_chicken_tags = TAGS_BY_ANIMAL_TYPE_AND_BREEDING_TYPE[AnimalType.BROILER_CHICKEN]
        for breeding_type, tags in broiler_chicken_tags.items():
            if any(tag in self.product_data.categories_tags for tag in tags):
                # set the breeding type if any of the tags is present
                breeding_types.broiler_chicken_breeding_type = breeding_type
                break

        return breeding_types

    def compute_weights(self) -> AnimalProductWeight:
        """
        Compute the weight of animal products in the product.

        Returns:
            AnimalProductWeight object with detected weights
        """
        # TODO: Implement actual weight calculation based on product data
        # This is currently a placeholder
        return AnimalProductWeight(
            egg_weight=200,
            chicken_weight=None,
        )

    @property
    def have_data_to_be_computed(self) -> bool:
        """
        Check if we have enough data to generate a report.

        Returns:
            True if at least one breeding type and product weight is set, False otherwise
        """
        return bool(self.has_breeding_type and self.has_weight)

    @property
    def has_breeding_type(self) -> bool:
        """
        Check if any breeding type is set.

        Returns:
            True if any breeding type is set, False otherwise
        """
        return bool(self.breeding_types.laying_hen_breeding_type or self.breeding_types.broiler_chicken_breeding_type)

    @property
    def has_weight(self) -> bool:
        """
        Check if any weight is set.

        Returns:
            True if any weight is set, False otherwise
        """
        return bool(self.weights.egg_weight or self.weights.chicken_weight)

    def get_pain_report(self) -> PainReport:
        """
        Generate a pain report based on breeding types and weights.

        Returns:
            A complete pain report
        """
        if not self.have_data_to_be_computed:
            raise ResourceNotFoundException("Product not found")

        animal_breeding_pairs = []

        # For laying hens
        if self.breeding_types.laying_hen_breeding_type:
            animal_breeding_pairs.append((
                AnimalType.LAYING_HEN,
                self.breeding_types.laying_hen_breeding_type,
                self.weights.egg_weight or 0
            ))

        # For broiler chickens
        if self.breeding_types.broiler_chicken_breeding_type:
            animal_breeding_pairs.append((
                AnimalType.BROILER_CHICKEN,
                self.breeding_types.broiler_chicken_breeding_type,
                self.weights.chicken_weight or 0
            ))

        return PainReport(
            pain_categories=[
                PainCategory(
                    pain_type=pain_type,
                    animals=[
                        AnimalPainDuration(
                            animal_type=animal_type,
                            seconds_in_pain=self._calculate_time_in_pain(
                                animal_type, breeding_type_value, pain_type, animal_weight
                            )
                        )
                        for animal_type, breeding_type_value, animal_weight in animal_breeding_pairs
                        if animal_weight > 0
                    ]
                )
                for pain_type in PainType
            ],
        )

    def _calculate_time_in_pain(self, animal_type, breeding_type_value, pain_type, weight_value):
        """
        Calculates time in pain for a given combination.

        Args:
            animal_type: Type of animal (from AnimalType enum)
            breeding_type_value: Type of breeding for this animal
            pain_type: Type of pain (from PainType enum)
            weight_value: Weight of the animal product in grams

        Returns:
            Duration of pain in seconds
        """
        if weight_value <= 0:
            return 0

        time_in_pain = (
            TIME_IN_PAIN_FOR_100G_IN_SECONDS.get(animal_type, {})
            .get(breeding_type_value, {})
            .get(pain_type, 0)
        )

        return time_in_pain * weight_value / 100


async def compute_suffering_footprint(barcode: str) -> PainReport | None:
    """
    Compute the suffering footprint for a product based on its barcode.

    Args:
        barcode: The product barcode

    Returns:
        PainReport if applicable, None otherwise
    """
    # Get the product data
    product_data = await get_data_from_off(barcode)

    # Create calculator with the retrieved data
    calculator = PainReportCalculator(product_data)

    # Check if we have enough data to generate a report
    if not calculator.have_data_to_be_computed:
        raise ResourceNotFoundException(f"Product not found: {barcode}")

    # Generate and return the pain report
    return calculator.get_pain_report()
