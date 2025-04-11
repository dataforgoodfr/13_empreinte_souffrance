from typing import Dict, List

from app.config.exceptions import ResourceNotFoundException
from app.enums.open_food_facts.enums import (
    TAGS_BY_ANIMAL_TYPE_AND_BREEDING_TYPE,
    TIME_IN_PAIN_FOR_100G_IN_SECONDS,
    AnimalType,
    PainIntensity,
    PainType,
)
from app.schemas.open_food_facts.external import ProductData
from app.schemas.open_food_facts.internal import AnimalPainReport, BreedingTypeAndWeight, PainLevelData, PainReport
from app.scripts.weight_calculator import calculate_egg_weight


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

    def _compute_breeding_types_with_weights(self) -> Dict[AnimalType, BreedingTypeAndWeight]:
        """
        Compute the breeding types and weights from product data.

        Returns:
            A dictionary mapping animal types to BreedingTypeAndWeight objects with detected breeding type and weight
        """

        # Get the breeding types
        breeding_types_by_animal = self._get_breeding_types()

        # Fill the weight for each breeding type and remove breeding types with weight <= 0
        breeding_types_with_weights = self._get_breeding_types_with_weights(breeding_types_by_animal)

        return breeding_types_with_weights

    def _get_breeding_types(self) -> Dict[AnimalType, BreedingTypeAndWeight]:
        """
        Compute the breeding types from product data.

        Returns:
            A dictionary mapping animal types to BreedingTypeAndWeight objects with detected breeding types
        """
        breeding_types_by_animal = {}
        for animal_type, tags_by_breeding_type in TAGS_BY_ANIMAL_TYPE_AND_BREEDING_TYPE.items():
            # Example of what we get from the for loop:
            # animal_type: AnimalType.LAYING_HEN
            # tags_by_breeding_type: LayingHenBreedingType.FURNISHED_CAGE: ["en:cage-chicken-eggs"]

            for breeding_type, tags in tags_by_breeding_type.items():
                if self.product_data.categories_tags and any(tag in self.product_data.categories_tags for tag in tags):
                    # Set the breeding type if any of the tags is present
                    breeding_types_by_animal[animal_type] = BreedingTypeAndWeight(breeding_type=breeding_type)
                    break

        return breeding_types_by_animal

    def _get_breeding_types_with_weights(
        self, breeding_types_by_animal: Dict[AnimalType, BreedingTypeAndWeight]
    ) -> Dict[AnimalType, BreedingTypeAndWeight]:
        """
        Compute the weight of animal product and fill the weight for each BreedingTypeAndWeight object.
        If the computed weight is <= 0, the animal type will be removed from the dictionary.

        Args:
            breeding_types_by_animal: Dictionary mapping animal types to BreedingTypeAndWeight objects

        Returns:
            A dictionary mapping animal types to BreedingTypeAndWeight objects with their weights, if the weight is > 0
        """
        breeding_types_with_weights = {}

        for animal_type, breeding_type in breeding_types_by_animal.items():
            weight_dict = calculate_egg_weight(breeding_types_by_animal, self.product_data)

            weight = weight_dict[AnimalType.LAYING_HEN].animal_product_weight

            # We only return breeding types (and their weights) if the weight of the animal-based product is > 0
            if weight > 0:
                breeding_type.animal_product_weight = weight
                breeding_types_with_weights[animal_type] = breeding_type

        return breeding_types_with_weights

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
