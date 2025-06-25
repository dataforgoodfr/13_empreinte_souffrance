from typing import List

from app.business.open_food_facts.breeding_type_calculator import BreedingTypeCalculator
from app.business.open_food_facts.egg_weight_calculator import calculate_egg_weight
from app.config.exceptions import ResourceNotFoundException
from app.enums.open_food_facts.enums import TIME_IN_PAIN_FOR_100G_IN_SECONDS, AnimalType, PainIntensity, PainType
from app.schemas.open_food_facts.external import ProductData
from app.schemas.open_food_facts.internal import (
    AnimalError,
    AnimalPainReport,
    BreedingType,
    BreedingTypeAndQuantity,
    PainLevelData,
    PainReport,
    ProductError,
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
        self.breeding_types = self._get_breeding_types()
        self.quantities = self._get_quantities()
        self.breeding_types_and_quantities = self._get_breeding_types_and_quantities()

    def _get_product_type(self) -> ProductType:
        animal_types = set()
        for animal_type in AnimalType:
            if (
                animal_type.is_computed
                and self.product_data.categories_tags
                and animal_type.categories_tags in self.product_data.categories_tags
            ):
                animal_types.add(animal_type)
        if len(animal_types) == 1:
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
        product_error: ProductError | None = ProductError.NO_HANDLED_ANIMAL

        # Process each animal type and its breeding type
        # If unable to compute animal pain report, add error message to animal report
        for animal_type, breeding_type_and_quantity in self.breeding_types_and_quantities.items():
            if isinstance(breeding_type_and_quantity, AnimalError):
                animal_report = AnimalPainReport(
                    animal_type=animal_type,
                    animal_error=breeding_type_and_quantity,
                    breeding_type=self.breeding_types.get(animal_type, None),
                    quantity=self.quantities.get(animal_type, None),
                )
                product_error = ProductError.NO_PAIN_LEVELS

            else:
                try:
                    animal_report = AnimalPainReport(
                        animal_type=animal_type,
                        pain_levels=self._generate_pain_levels_for_animal(animal_type, breeding_type_and_quantity),
                        breeding_type_and_quantity=breeding_type_and_quantity,
                    )
                    product_error = None
                except ResourceNotFoundException:
                    raise ResourceNotFoundException(f"Unable to generate pain levels for animal {animal_type}")

            animal_reports.append(animal_report)

        return PainReport(
            animals=animal_reports,
            product_name=self.product_data.product_name,
            product_image_url=self.product_data.image_url,
            product_error=product_error,
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

    def _get_breeding_types_and_quantities(self) -> dict[AnimalType, BreedingTypeAndQuantity | AnimalError]:
        """
        Gets the breeding types and quantity from separate methods.

        Returns:
            A dictionary mapping animal types to BreedingTypeAndQuantity
            objects  or an error containing
            the missing information for an animal type that was though identified.
        """

        breeding_types_by_animal = self.breeding_types
        quantity_by_animal = self.quantities

        breeding_types_and_quantities = dict[AnimalType, BreedingTypeAndQuantity | AnimalError]()

        for animal_type in self.product_type.animal_types:
            try:
                breeding_type = breeding_types_by_animal[animal_type]
                quantity = quantity_by_animal[animal_type]

                match (breeding_type, quantity):
                    case (None, None):
                        breeding_types_and_quantities[animal_type] = AnimalError.NO_BREEDING_TYPE_AND_NO_QUANTITY
                    case (None, _):
                        breeding_types_and_quantities[animal_type] = AnimalError.NO_BREEDING_TYPE
                    case (_, None):
                        breeding_types_and_quantities[animal_type] = AnimalError.NO_QUANTITY
                if breeding_type and quantity is not None:
                    breeding_types_and_quantities[animal_type] = BreedingTypeAndQuantity(
                        breeding_type=breeding_type, quantity=quantity
                    )
            except KeyError:
                raise ResourceNotFoundException(
                    "Missing breeding type or quantity key for animal type: {}".format(animal_type)
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

    def _get_quantities(self) -> dict[AnimalType, float | None]:
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
            # unable for now to compute mixed product
            return {animal_type: None for animal_type in self.product_type.animal_types}
        else:
            try:
                animal_type = list(self.product_type.animal_types)[0]
            except IndexError:
                return {}
            if animal_type == AnimalType.LAYING_HEN:
                quantity = calculate_egg_weight(self.product_data)
                return {animal_type: quantity}
            else:
                return {animal_type: None}

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

        # Get the time in pain per 100g for this combination of parameters
        # Default to 0 if any level in the hierarchy is missing
        try:
            breeding_type = breeding_type_and_quantity.breeding_type
            time_in_pain = TIME_IN_PAIN_FOR_100G_IN_SECONDS[animal_type][breeding_type][pain_type][pain_intensity]  # type: ignore[index]
        except (KeyError, TypeError):
            # This combination of animal, breeding type, pain type, and intensity is not defined
            return 0

        # Scale the time in pain based on the quantity of animal product
        return int(time_in_pain * breeding_type_and_quantity.quantity / 100)
