from typing import TypeAlias

from app.business.open_food_facts.egg_quantity_calculator import EggQuantityCalculator
from app.schemas.open_food_facts.external import ProductData
from app.schemas.open_food_facts.internal import AnimalType, ProductType

ProductQuantity: TypeAlias = float | None
# float to be changed to EggQuantity while letting PainReportCalculator and KnowledgePanel parse EggQuantity


class QuantityCalculator:
    """
    Calculates the quantity of product by animal type, based on the product's metadata
    and type. Supports specific logic for egg-based products (LAYING_HEN).
    """

    def __init__(self, product_data: ProductData, product_type: ProductType):
        """
        Initializes the calculator with product data and type.

        Args:
            product_data (ProductData): Structured product information including quantity, unit, and tags.
            product_type (ProductType): The type of product, including associated animal types.
        """

        self.product_data = product_data
        self.product_type = product_type

    def get_quantities_by_animal(self) -> dict[AnimalType, ProductQuantity]:
        """
        Returns a mapping of animal types to their associated quantity estimates.
        This method is a placeholder for mixed products; no actual computation is done.

        Returns:
            dict[AnimalType, ProductQuantity]: A dictionary where each animal type is mapped to None.
        """
        quantities_by_animal: dict[AnimalType, float | None] = {}

        for animal_type in self.product_type.animal_types:
            quantities_by_animal[animal_type] = None
        return quantities_by_animal

    def get_quantity(self, animal_type: AnimalType) -> ProductQuantity:
        """
        Computes the quantity of the product for a specific animal type.
        Uses the EggQuantityCalculator for LAYING_HEN and use output weight for now

        Args:
            AnimalType (AnimalType): The animal type to calculate quantity for.
        Returns:
            ProductQuantity : for now float or None, in grams.
        """
        if animal_type == AnimalType.LAYING_HEN:
            return EggQuantityCalculator().calculate_egg_quantity(self.product_data).total_weight
        else:
            return None
