import re
from typing import List

from app.schemas.open_food_facts.external import ProductData

AVERAGE_EGG_WEIGHT = 50


UNIT_CONVERSIONS = {
    "pcs": lambda q: float(q) * AVERAGE_EGG_WEIGHT,
    "sans": lambda q: float(q) * AVERAGE_EGG_WEIGHT,
    "unite": lambda q: float(q) * AVERAGE_EGG_WEIGHT,
    "g": lambda q: float(q),
    "gr": lambda q: float(q),
    "gramm": lambda q: float(q),
    "oz": lambda q: float(q) * 28.35,
    "lbs": lambda q: float(q) * 453.59,
    "ml": lambda q: float(q) * 1.03,
    "l": lambda q: float(q) * 1030,
    "litres": lambda q: float(q) * 1030,
}

EGG_WEIGHTS_BY_TAG = {
    60: {"large-eggs", "gros-oeufs"},
    55: {"grade-a-eggs", "grade-aa-eggs"},
    50: {"medium-eggs"},
}


def get_egg_weight_by_tag(categories_tags: List[str]) -> int:
    """
    Returns the standard weight of one egg based on category tags.
    """
    for weight, tags in EGG_WEIGHTS_BY_TAG.items():
        if any(tag in categories_tags for tag in tags):
            return weight
    return 0


def get_number_of_eggs(categories_tags: List[str]) -> int:
    """
    Extracts the number of eggs from tags.
    TODO: Add support for other tags
    """
    for tag in categories_tags:
        match = re.search(r"pack-of-(\d+)", tag)
        if match:
            return int(match.group(1))
    return 0


def get_total_egg_weight_from_tags(categories_tags: List[str]) -> float:
    """
    Calculates total egg weight based on standard weights and pack size.
    """
    num_eggs = get_number_of_eggs(categories_tags)
    weight_per_egg = get_egg_weight_by_tag(categories_tags)
    return weight_per_egg * num_eggs


def get_egg_weight_from_quantity(quantity: float, unit: str) -> float:
    """
    Converts product quantity and unit into weight in grams.
    """
    unit_key = unit.lower()
    converter = UNIT_CONVERSIONS.get(unit_key)
    if converter:
        try:
            return converter(quantity)
        except (ValueError, TypeError):
            pass
    return 0


def calculate_egg_weight(product_data: ProductData) -> float:
    """
    Calculates the weight of eggs based on the product data.

    Returns:
        The egg weight if applicable.
    """
    quantity = product_data.product_quantity
    unit = product_data.product_quantity_unit
    categories_tags = product_data.categories_tags or []

    if quantity and unit:
        egg_weight = get_egg_weight_from_quantity(quantity, unit)
    else:
        egg_weight = get_total_egg_weight_from_tags(categories_tags)

    return egg_weight
