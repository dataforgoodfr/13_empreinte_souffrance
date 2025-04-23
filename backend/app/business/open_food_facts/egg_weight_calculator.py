import re
from typing import List

from app.schemas.open_food_facts.external import ProductData

AVERAGE_EGG_WEIGHT = 50
LARGE_EGG_WEIGHT = 60


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
    60: {
        "en:large-eggs",
        "en:free-range-organic-large-chicken-eggs",
        "gros-oeufs",
        "en:free-range-large-eggs",
        "en:large-free-run-chicken-eggs",
    },
    55: {"en:grade-a-eggs", "en:grade-a-eggs"},
    50: {"en:medium-eggs-pack-of-10", "en:organic-chicken-eggs-medium-size"},
}

REGEX_NUMBERS_ONLY = r"\s*\d+(\.\d+)?\s*"
REGEX_NUMERIC_UNIT = r"\s*(\d+(?:\.\d+)?)\s*((?:[a-zA-Zа-яА-ЯёЁ\u00C0-\u00FFœŒ]+\s*)+)\.?"
REGEX_X_NUM = r"[xX]\s*(\d+(?:\.\d+)?)"
REGEX_ADDITION = r"(\d+)\s*\+\s*(\d+)"
REGEX_EXTRACT_DIGITS = r"\b(\d{1,3})\b"

DOZEN_EXPRESSIONS = ["dozen", "dozens", "dzn", "doz"]
MOYEN_EXPRESSIONS = ["m", "moyen", "M", "Moyens", "moyens"]
LARGE_EXPRESSIONS = ["gros", "l", "xl", "large", "Large", "L", "XL", "Gros"]


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
    if num_eggs > 0 and weight_per_egg == 0:
        return num_eggs * AVERAGE_EGG_WEIGHT
    return weight_per_egg * num_eggs


def get_egg_weight_from_quantity(quantity: str) -> float:
    """
    Parses quantity into weight in grams.
    """
    # Case 1: Only numeric (≤30 eggs)
    parsed = False
    if re.fullmatch(REGEX_NUMBERS_ONLY, quantity):
        num = float(quantity)
        if num <= 30:
            parsed = True
            return num * AVERAGE_EGG_WEIGHT

    # Case 2: Numeric + unit (Latin, Cyrillic, accented, etc.)
    if not parsed:
        match = re.match(REGEX_NUMERIC_UNIT, quantity)
        if match:
            number = float(match.group(1))
            unit = match.group(2).lower().split()
            # e.g. '1 dozen'
            if any([u in DOZEN_EXPRESSIONS for u in unit]):
                egg_weight = number * 12 * AVERAGE_EGG_WEIGHT
            # e.g. '12 M'
            elif any([u in MOYEN_EXPRESSIONS for u in unit]):
                egg_weight = number * AVERAGE_EGG_WEIGHT
            # e.g. '12 large'
            elif any([u in LARGE_EXPRESSIONS for u in unit]):
                egg_weight = number * LARGE_EGG_WEIGHT
            else:
                # e.g. '12 unities'
                egg_weight = number * AVERAGE_EGG_WEIGHT
            parsed = True
            return egg_weight

    # Case 3: x10 / X10 style
    if not parsed:
        match = re.match(REGEX_X_NUM, quantity)
        if match:
            egg_number = float(match.group(1))
            parsed = True
            return egg_number * AVERAGE_EGG_WEIGHT

    # Case 4: Addition expressions: "10 + 2", "12 + 3 oeufs"
    if not parsed:
        match = re.search(REGEX_ADDITION, quantity)
        if match:
            egg_number = int(match.group(1)) + int(match.group(2))
            parsed = True
            return egg_number * AVERAGE_EGG_WEIGHT

    # Case 5: Single number (e.g. "Boîte de 6")
    if not parsed:
        match = re.search(REGEX_EXTRACT_DIGITS, quantity)
        if match:
            num = int(match.group(1))
            if num < 1000:
                parsed = True
                return num * AVERAGE_EGG_WEIGHT

    if not parsed:
        return 0

    return 0


def get_egg_weight_from_product_quantity_and_unit(quantity: float, unit: str) -> float:
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
    product_quantity = product_data.product_quantity
    unit = product_data.product_quantity_unit
    quantity = product_data.quantity
    categories_tags = product_data.categories_tags or []

    if product_quantity and unit:
        egg_weight = get_egg_weight_from_product_quantity_and_unit(product_quantity, unit)
    elif quantity:
        egg_weight = get_egg_weight_from_quantity(quantity)
    else:
        egg_weight = get_total_egg_weight_from_tags(categories_tags)

    return egg_weight
