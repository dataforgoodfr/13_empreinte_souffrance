from typing import Dict, List

from app.business.open_food_facts.breeding_type_calculator import BreedingTypeCalculator
from app.business.open_food_facts.egg_weight_calculator import calculate_egg_weight
from app.config.exceptions import ResourceNotFoundException
from app.enums.open_food_facts.enums import TIME_IN_PAIN_FOR_100G_IN_SECONDS, AnimalType, PainIntensity, PainType
from app.schemas.open_food_facts.external import ProductData
from app.schemas.open_food_facts.internal import (
    AnimalPainReport,
    BreedingType,
    BreedingTypeAndWeight,
    PainLevelData,
    PainReport,
    ProductType,
)


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
        self.product_type = self._get_product_type()
        self.breeding_types_with_weights = self._get_breeding_types_with_weights()

    def _get_product_type(self) -> ProductType:
        animal_types = set()
        for animal_type in AnimalType:
            if self.product_data.categories_tags and animal_type.categories_tags in self.product_data.categories_tags:
                animal_types.add(animal_type)
        if len(animal_types) == 1:
            return ProductType(is_mixed=False, animal_types=animal_types)
        else:
            return ProductType(is_mixed=True, animal_types=animal_types)

    def get_pain_report(self) -> PainReport:
        """
        Generate a pain report based on breeding types and weights.

        The report is organized by animal type, with each animal having
        a list of pain levels categorized by pain type (physical/psychological)
        and breeding type information.

        Returns:
            A complete pain report
        """
        if not self.breeding_types_with_weights:
            raise ResourceNotFoundException("Can't find valid breeding type or animal product weight for this product")

        animal_reports = []

        # Process each animal type and its breeding type
        for animal_type, breeding_type in self.breeding_types_with_weights.items():
            # Generate all pain levels for this animal
            pain_levels = self._generate_pain_levels_for_animal(animal_type, breeding_type)

            # Add animal report to the list
            animal_reports.append(
                AnimalPainReport(
                    animal_type=animal_type, pain_levels=pain_levels, breeding_type_with_weight=breeding_type
                )
            )

        return PainReport(
            animals=animal_reports,
            product_name=self.product_data.product_name,
            product_image_url=self.product_data.image_url,
        )

    def _generate_pain_levels_for_animal(
        self, animal_type: AnimalType, breeding_type: BreedingTypeAndWeight
    ) -> List[PainLevelData]:
        """
        Generate pain levels for a specific animal type and breeding type.

        Args:
            animal_type: The type of animal
            breeding_type: The breeding type with weight information

        Returns:
            List of PainLevelData objects for all pain types and intensities
        """
        pain_levels = []

        # Process each pain type
        for pain_type in PainType:
            pain_levels.extend(self._generate_pain_levels_for_type(animal_type, breeding_type, pain_type))

        return pain_levels

    def _generate_pain_levels_for_type(
        self, animal_type: AnimalType, breeding_type: BreedingTypeAndWeight, pain_type: PainType
    ) -> List[PainLevelData]:
        """
        Generate pain levels for a specific animal, breeding type, and pain type.

        Args:
            animal_type: The type of animal
            breeding_type: The breeding type with weight information
            pain_type: The type of pain (physical or psychological)

        Returns:
            List of PainLevelData objects for all pain intensities of the given type
        """
        pain_levels = []

        # Process each pain intensity for this pain type
        for pain_intensity in PainIntensity:
            # Calculate seconds in pain for this animal, pain type, and intensity
            seconds_in_pain = self._calculate_time_in_pain_for_animal_with_type(
                animal_type, breeding_type, pain_type, pain_intensity
            )

            # Add pain level entry
            pain_levels.append(
                PainLevelData(pain_intensity=pain_intensity, pain_type=pain_type, seconds_in_pain=seconds_in_pain)
            )

        return pain_levels

    def _get_breeding_types_with_weights(self) -> Dict[AnimalType, BreedingTypeAndWeight]:
        """
        Gets the breeding types and weights from separate methods.

        Returns:
            A dictionary mapping animal types to BreedingTypeAndWeight
            objects with detected breeding type and weight
        """

        # Get the breeding types
        breeding_types_by_animal = self._get_breeding_types()
        weight_by_animal = self._get_weights()

        breeding_types_with_weights = {
            animal_type: BreedingTypeAndWeight(
                breeding_type=breeding_types_by_animal[animal_type], animal_product_weight=weight_by_animal[animal_type]
            )
            for animal_type in self.product_type.animal_types
        }

        return breeding_types_with_weights

    def _get_breeding_types(self) -> Dict[AnimalType, BreedingType]:
        """
        Compute the breeding types from product data.
        Returns:
            A dictionary mapping animal types to BreedingTypeAndWeight
              objects with detected breeding types
        """
        if self.product_type.is_mixed:
            return BreedingTypeCalculator(self.product_data, self.product_type).get_breeding_types_by_animal()

        else:
            animal_type = list(self.product_type.animal_types)[0]
            breeding_type = BreedingTypeCalculator(self.product_data, self.product_type).get_breeding_type(
                animal_type=animal_type
            )
            return {animal_type: breeding_type}

    def _get_weights(self) -> dict[AnimalType, float]:
        """
        Calculates and returns the weights associated with each animal type
        present in the product.
        If product mixed or broiler chicken, weight cannot be computed for now
        For laying hens  uses a dedicated egg weight calculator.

        Returns:
            dict[AnimalType, float]: A dictionary where keys are `AnimalType`
            instances and values are their associated weights (in grams).
        """
        if self.product_type.is_mixed:
            return {animal_type: 0 for animal_type in self.product_type.animal_types}
        else:
            animal_type = list(self.product_type.animal_types)[0]
            if animal_type == AnimalType.LAYING_HEN:
                weight = calculate_egg_weight(self.product_data)
                return {animal_type: weight}
            else:
                return {animal_type: 0}

    def _calculate_time_in_pain_for_animal_with_type(
        self,
        animal_type: AnimalType,
        breeding_type_with_weight: BreedingTypeAndWeight,
        pain_type: PainType,
        pain_intensity: PainIntensity,
    ) -> int:
        """
        Calculates time in pain for a given animal type, breeding type, pain type, and pain intensity.

        Args:
            animal_type: The type of animal
            breeding_type_with_weight: A BreedingTypeAndWeight object
            pain_type: The type of pain (physical or psychological)
            pain_intensity: Pain intensity (from PainIntensity enum)

        Returns:
            Duration of pain in seconds
        """
        if breeding_type_with_weight.animal_product_weight <= 0:
            return 0

        # Get the time in pain per 100g for this combination of parameters
        # Default to 0 if any level in the hierarchy is missing
        try:
            breeding_type = breeding_type_with_weight.breeding_type
            time_in_pain = TIME_IN_PAIN_FOR_100G_IN_SECONDS[animal_type][breeding_type][pain_type][pain_intensity]  # type: ignore[index]
        except (KeyError, TypeError):
            # This combination of animal, breeding type, pain type, and intensity is not defined
            return 0

        # Scale the time in pain based on the weight of animal product
        return int(time_in_pain * breeding_type_with_weight.animal_product_weight / 100)
