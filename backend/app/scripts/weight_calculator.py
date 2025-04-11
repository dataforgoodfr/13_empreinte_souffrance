import re
from typing import Dict, List

from app.enums.open_food_facts.enums import AnimalType
from app.schemas.open_food_facts.external import ProductData
from app.schemas.open_food_facts.internal import BreedingTypeAndWeight

# BreedingTypeAndWeightDict = Dict[str, Union[str, float]]

# ProductDataDict = Dict[str, Optional[Union[str, List[str], List[Dict[str, Optional[Union[str, float]]]]]]]


def get_standard_egg_weight_from_category(categories_tags: List[str]) -> float:
    """
    Retrieves the standard weight of an egg based on the category (to be implemented).
    """
    num_eggs = get_number_of_eggs_from_pack_tag(categories_tags)
    for tag in categories_tags:
        if "large-eggs" in tag:
            return 60.0 * num_eggs
        elif "grade-a-eggs" or "grade-aa-eggs" in tag:
            return 55.0 * num_eggs  # Example, weight may vary
        elif "medium-eggs" in tag:
            return 50.0 * num_eggs
        elif "gros-oeufs" in tag:
            return 60.0 * num_eggs
    return 0.0


def get_number_of_eggs_from_pack_tag(categories_tags: List[str]) -> int:
    """
    Extracts the number of eggs from the 'pack-of-' tag.
    """
    for tag in categories_tags:
        match = re.search(r"pack-of-(\d+)", tag)
        if match:
            return int(match.group(1))
    return 1


def get_average_egg_weight() -> float:
    """
    Returns the estimated average weight of an egg in grams.
    """
    return 50.0


def calculate_egg_weight(
    breeding_types_by_animal: Dict[AnimalType, BreedingTypeAndWeight], product_data: ProductData
) -> Dict[AnimalType, BreedingTypeAndWeight]:
    """
    Calculates the weight of eggs for LAYING_HEN in the breeding_types dictionary
    based on the provided schema logic and product data, completely without classes.

    Args:
        breeding_types_by_animal: Dictionary mapping animal types to dictionaries
                                   representing breeding type and weight.
        product_data: Dictionary containing product information.

    Returns:
        A dictionary mapping animal types to dictionaries with updated
        animal_product_weight for LAYING_HEN, or the original dictionary if not applicable.
    """
    updated_breeding_types = breeding_types_by_animal.copy()

    if AnimalType.LAYING_HEN in updated_breeding_types:
        quantity = product_data.product_quantity
        unit = product_data.product_quantity_unit
        categories_tags = product_data.categories_tags or []

        egg_weight = 0.0

        if not quantity:
            # quantity == Ø
            has_size_in_category = any(
                "large-eggs" in tag
                or "grade-a-eggs" in tag
                or "medium-eggs" in tag
                or "gros-oeufs" in tag
                or "pack-of-" in tag
                or "grade-aa-eggs"
                for tag in categories_tags
            )
            if has_size_in_category:
                egg_weight = get_standard_egg_weight_from_category(categories_tags)
        else:
            # quantity is not Ø
            if unit and unit.lower() in ["pcs", "sans", "unite"]:
                try:
                    num_eggs = float(quantity)
                    egg_weight = num_eggs * get_average_egg_weight()
                except (ValueError, TypeError):
                    pass
            elif unit and unit.lower() in ["g", "gr", "gramm"]:
                try:
                    egg_weight = float(quantity)
                except (ValueError, TypeError):
                    pass
            elif unit and unit.lower() in ["oz"]:
                try:
                    egg_weight = float(quantity) * 28.35
                except (ValueError, TypeError):
                    pass
            elif unit and unit.lower() in ["lbs"]:
                try:
                    egg_weight = float(quantity) * 453.59
                except (ValueError, TypeError):
                    pass
            elif unit and unit.lower() in ["ml"]:
                try:
                    egg_weight = float(quantity) * 1.03
                except (ValueError, TypeError):
                    pass
            elif unit and unit.lower() in ["l", "litres"]:
                try:
                    egg_weight = float(quantity) * 1030
                except (ValueError, TypeError):
                    pass

        if egg_weight > 0:
            updated_breeding_types[AnimalType.LAYING_HEN].animal_product_weight = egg_weight

    return updated_breeding_types
