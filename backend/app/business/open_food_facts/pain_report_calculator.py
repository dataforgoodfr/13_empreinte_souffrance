from random import randint
from typing import List

from app.config.exceptions import ResourceNotFoundException
from app.enums.open_food_facts.enums import (
    TAGS_BY_ANIMAL_TYPE_AND_BREEDING_TYPE,
    TIME_IN_PAIN_FOR_100G_IN_SECONDS,
    PainIntensity,
)
from app.schemas.open_food_facts.external import ProductData
from app.schemas.open_food_facts.internal import AnimalPainDuration, BreedingTypeAndWeight, PainCategory, PainReport


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
        self.breeding_types_with_weights = self._compute_breeding_types_with_weights()

    def _compute_breeding_types_with_weights(self) -> List[BreedingTypeAndWeight]:
        """
        Compute the breeding types and weights from product data.

        Returns:
            A list of BreedingTypeAndWeight objects (one by type of animal) with detected breeding types and weights
        """

        # Get the breeding types
        breeding_types = self._get_breeding_types()

        # Fill the weight for each breeding type and remove breeding types with weight <= 0
        breeding_types_with_weights = self._get_breeding_types_with_weights(breeding_types)

        return breeding_types_with_weights

    def _get_breeding_types(self) -> List[BreedingTypeAndWeight]:
        """
        Compute the breeding types from product data.

        Returns:
            A list of BreedingTypeAndWeight objects (one by type of animal) with detected breeding types
        """
        breeding_types = []
        for animal_type, tags_by_breeding_type in TAGS_BY_ANIMAL_TYPE_AND_BREEDING_TYPE.items():
            # Example of what we get from the for loop:
            # animal_type: AnimalType.LAYING_HEN
            # tags_by_breeding_type: LayingHenBreedingType.FURNISHED_CAGE: ["en:cage-chicken-eggs"]

            for breeding_type, tags in tags_by_breeding_type.items():
                if any(tag in self.product_data.categories_tags for tag in tags):
                    # set the breeding type if any of the tags is present
                    breeding_types.append(BreedingTypeAndWeight(animal_type=animal_type, breeding_type=breeding_type))
                    break

        return breeding_types

    def _get_breeding_types_with_weights(self, breeding_types: List[BreedingTypeAndWeight]) -> List[BreedingTypeAndWeight]:
        """
        Compute the weight of animal product and fill the weight for each BreedingTypeAndWeight objects.
        If the computed weight is <= 0, the BreedingTypeAndWeight object will not be returned.

        Returns:
            A list of BreedingTypeAndWeight objects (one by type of animal) with detected weights, if the weight is > 0
        """
        breeding_types_and_weights = []
        for breeding_type in breeding_types:
            # TODO: Implement actual weight calculation based on product data
            #  This is currently a placeholder
            weight = randint(0, 1000)

            # We only return breeding types (and their weights) if the weight of the animal-based product is > 0
            if weight > 0:
                breeding_type.animal_product_weight = weight
                breeding_types_and_weights.append(breeding_type)

        return breeding_types_and_weights

    def get_pain_report(self) -> PainReport:
        """
        Generate a pain report based on breeding types and weights.

        Returns:
            A complete pain report
        """
        if not self.breeding_types_with_weights:
            raise ResourceNotFoundException("Can't find valid breeding type or animal product weight for this product")

        return PainReport(
            breeding_types_with_weights=self.breeding_types_with_weights,
            pain_categories=[
                PainCategory(
                    pain_intensity=pain_intensity,
                    animals=[
                        AnimalPainDuration(
                            animal_type=breeding_type_with_weight.animal_type,
                            seconds_in_pain=self._calculate_time_in_pain(breeding_type_with_weight, pain_intensity)
                        )
                        for breeding_type_with_weight in self.breeding_types_with_weights
                    ]
                )
                for pain_intensity in PainIntensity
            ],
        )

    def _calculate_time_in_pain(
            self,
            breeding_type_with_weight: BreedingTypeAndWeight,
            pain_intensity: PainIntensity
    ) -> int:
        """
        Calculates time in pain for a given combination.

        Args:
            breeding_type_with_weight: A BreedingTypeAndWeight object
            pain_intensity: Pain intensity (from PainIntensity enum)

        Returns:
            Duration of pain in seconds
        """
        if breeding_type_with_weight.animal_product_weight <= 0:
            return 0

        time_in_pain = (
            TIME_IN_PAIN_FOR_100G_IN_SECONDS.get(breeding_type_with_weight.animal_type, {})
            .get(breeding_type_with_weight.breeding_type, {})
            .get(pain_intensity, 0)
        )

        return int(time_in_pain * breeding_type_with_weight.animal_product_weight / 100)
