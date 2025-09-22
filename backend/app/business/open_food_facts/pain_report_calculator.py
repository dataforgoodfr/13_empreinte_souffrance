from typing import List

from app.business.open_food_facts.breeding_type_calculator import BreedingTypeCalculator
from app.business.open_food_facts.product_type_calculator import get_product_type
from app.business.open_food_facts.quantity_calculator import QuantityCalculator
from app.business.open_food_facts.unit_pain_loader import PAIN_PER_EGG_IN_SECONDS
from app.config.exceptions import MissingBreedingTypeOrQuantityError, ResourceNotFoundException
from app.enums.open_food_facts.enums import (
    AnimalType,
    EggCaliber,
    PainIntensity,
    PainType,
    ProductQuantity,
)
from app.schemas.open_food_facts.external import ProductData
from app.schemas.open_food_facts.internal import (
    AnimalPainReport,
    BreedingType,
    BreedingTypeAndQuantity,
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
        self.product_type = get_product_type(self.product_data)
        self.breeding_types = self._get_breeding_types()
        self.quantities = self._get_quantities()
        self.breeding_types_and_quantities = self._get_breeding_types_and_quantities()

    def _get_product_type(self) -> ProductType:
        """
        Determine the product type based on the product data.
        checks if the product is mixed or single animal type,
        and identifies the animal types present.
        Returns:
            ProductType instance indicating if the product is mixed and the set of animal types.
        """
        animal_types = set()
        for animal_type in AnimalType:
            if (
                animal_type.is_computed
                and self.product_data.categories_tags
                and animal_type.categories_tags in self.product_data.categories_tags
            ):
                animal_types.add(animal_type)
        if not animal_types:
            raise ResourceNotFoundException("No animal types found in product data")
        elif len(animal_types) == 1:
            return ProductType(is_mixed=False, animal_types=animal_types)
        else:
            return ProductType(is_mixed=True, animal_types=animal_types)

    def get_pain_report(self) -> PainReport:
        """
        Generate a pain report based on breeding types and quantities.

        The report is organized by animal type, with each animal having
        a list of pain levels categorized by pain type (physical/psychological)
        and breeding type information.

        Returns:
            A complete pain report, with error messages for animals as an option
        """
        animal_reports = []

        # Process each animal type and its breeding type
        # If unable to compute animal pain report, add error message to animal report
        for animal_type, breeding_type_and_quantity in self.breeding_types_and_quantities.items():
            try:
                pain_levels = self._generate_pain_levels_for_animal(animal_type, breeding_type_and_quantity)
            except MissingBreedingTypeOrQuantityError:
                pain_levels = []

            animal_report = AnimalPainReport(
                animal_type=animal_type,
                pain_levels=pain_levels,
                breeding_type_and_quantity=breeding_type_and_quantity,
            )

            animal_reports.append(animal_report)

        return PainReport(
            animals=animal_reports,
            product_name=self.product_data.product_name,
            product_image_url=self.product_data.image_url,
        )

    def _generate_pain_levels_for_animal(
        self, animal_type: AnimalType, breeding_type: BreedingTypeAndQuantity
    ) -> List[PainLevelData]:
        """
        Generate pain levels for a specific animal type and breeding type.

        Args:
            animal_type: The type of animal
            breeding_type: The breeding type with quantity information

        Returns:
            List of PainLevelData objects for all pain types and intensities
        """
        pain_levels = []

        # Process each pain type
        for pain_type in PainType:
            pain_levels.extend(self._generate_pain_levels_for_pain_type(animal_type, breeding_type, pain_type))

        return pain_levels

    def _generate_pain_levels_for_pain_type(
        self, animal_type: AnimalType, breeding_type_and_quantity: BreedingTypeAndQuantity, pain_type: PainType
    ) -> List[PainLevelData]:
        """
        Generate pain levels for a specific animal, breeding type, and pain type.

        Args:
            animal_type: The type of animal
            breeding_type: The breeding type with quantity information
            pain_type: The type of pain (physical or psychological)

        Returns:
            List of PainLevelData objects for all pain intensities of the given type
        """
        pain_levels = []

        # Process each pain intensity for this pain type
        for pain_intensity in PainIntensity:
            # Calculate seconds in pain for this animal, pain type, and intensity
            seconds_in_pain = self._calculate_time_in_pain_for_animal_with_type(
                animal_type, breeding_type_and_quantity, pain_type, pain_intensity
            )

            # Add pain level entry
            pain_levels.append(
                PainLevelData(pain_intensity=pain_intensity, pain_type=pain_type, seconds_in_pain=seconds_in_pain)
            )

        return pain_levels

    def _get_breeding_types_and_quantities(self) -> dict[AnimalType, BreedingTypeAndQuantity]:
        """
        Gets the breeding types and quantity from separate methods.

        Returns:
            A dictionary mapping animal types to BreedingTypeAndQuantity
            objects  or an error containing
            the missing information for an animal type that was though identified.
        """

        breeding_types_by_animal = self.breeding_types
        quantity_by_animal = self.quantities

        breeding_types_and_quantities = dict[AnimalType, BreedingTypeAndQuantity]()

        for animal_type in self.product_type.animal_types:
            breeding_type = breeding_types_by_animal[animal_type]
            quantity = quantity_by_animal[animal_type]
            breeding_types_and_quantities[animal_type] = BreedingTypeAndQuantity(
                breeding_type=breeding_type, quantity=quantity
            )

        return breeding_types_and_quantities

    def _get_breeding_types(self) -> dict[AnimalType, BreedingType | None]:
        """
        Compute the breeding types from product data.
        Returns:
            A dictionary mapping animal types to BreedingType | None
              objects with detected breeding types
        """
        if self.product_type.is_mixed:
            return BreedingTypeCalculator(self.product_data, self.product_type).get_breeding_types_by_animal()

        else:
            try:
                animal_type = list(self.product_type.animal_types)[0]
            except IndexError:
                raise IndexError("Issue with product type : no animal types found but not mixed")
            breeding_type = BreedingTypeCalculator(self.product_data, self.product_type).get_breeding_type(
                animal_type=animal_type
            )
            return {animal_type: breeding_type}

    def _get_quantities(self) -> dict[AnimalType, ProductQuantity | None]:
        """
        Calculates and returns the quantities associated with each animal type
        present in the product.
        Mixed product and broiler chicken quantity cannot be computed for now
        For laying hens we use a dedicated egg weight calculator.

        Returns:
            dict[AnimalType, float]: A dictionary where keys are `AnimalType`
            instances and values are their associated quantities (in grams).
        """
        if self.product_type.is_mixed:
            return QuantityCalculator(self.product_data, self.product_type).get_quantities_by_animal()
        else:
            try:
                animal_type = list(self.product_type.animal_types)[0]
            except IndexError:
                return {}
            quantity = QuantityCalculator(self.product_data, self.product_type).get_quantity(animal_type)
            return {animal_type: quantity}

    def _calculate_time_in_pain_for_animal_with_type(
        self,
        animal_type: AnimalType,
        breeding_type_and_quantity: BreedingTypeAndQuantity,
        pain_type: PainType,
        pain_intensity: PainIntensity,
    ) -> int:
        """
        Calculates time in pain for a given animal type, breeding type, pain type, and pain intensity.

        Args:
            animal_type: The type of animal
            breeding_type_and_quantity: A BreedingTypeAndQuantity object
            pain_type: The type of pain (physical or psychological)
            pain_intensity: Pain intensity (from PainIntensity enum)

        Returns:
            Duration of pain in seconds
        """
        breeding_type = breeding_type_and_quantity.breeding_type
        quantity = breeding_type_and_quantity.quantity

        if breeding_type is None or quantity is None:
            raise MissingBreedingTypeOrQuantityError()

        if animal_type == AnimalType.LAYING_HEN:
            try:
                caliber = quantity.caliber or EggCaliber.AVERAGE
                count = quantity.count

                # Get the time in pain per egg for this combination of parameters
                # Default to 0 if any level in the hierarchy is missing
                time_in_pain = PAIN_PER_EGG_IN_SECONDS[animal_type][breeding_type][pain_type][pain_intensity][caliber]
            except (KeyError, TypeError):
                # This combination of animal, breeding type, pain type, and intensity is not defined
                return 0

            # Scale the time in pain based on the number of eggs
            return int(time_in_pain * count)

        # Pain can only be computed for laying hens
        else:
            return 0
