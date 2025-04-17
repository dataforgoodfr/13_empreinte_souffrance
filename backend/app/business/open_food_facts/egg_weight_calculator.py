import re
from typing import List, Optional

from app.schemas.open_food_facts.external import ProductData

AVERAGE_EGG_WEIGHT = 50
LARGE_EGG_WEIGHT = 60
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

# "6"
REGEX_NUMBERS_ONLY = r"\s*\d+(\.\d+)?\s*"
# "6 eggs"
REGEX_NUMERIC_UNIT = r"\s*(\d+(?:\.\d+)?)\s*((?:[a-zA-Zа-яА-ЯёЁ\u00C0-\u00FFœŒ]+\s*)+)\.?"
# "x10"
REGEX_X_NUM = r"[xX]\s*(\d+(?:\.\d+)?)"
# "10+2 eggs"
REGEX_ADDITION = r"(\d+)\s*\+\s*(\d+)"
# "a big box of 10 eggs"
REGEX_EXTRACT_DIGITS = r"\b(\d{1,3})\b"

DOZEN_EXPRESSIONS = ["dozen", "dozens", "dzn", "doz"]
MOYEN_EXPRESSIONS = ["m", "moyen", "moyens"]
LARGE_EXPRESSIONS = ["gros", "l", "xl", "large"]


DOZEN_UNIT = ["dzn", "dozen", "doz"]
WEIGHT_UNIT = ["lb", "kg", "oz", "à", "gram", "g", "gr"]
PIECE_UNIT = [
    "frische",
    "unknown",
    "pieze",
    "entre",
    "entre",
    "mixed",
    "pack",
    "portion",
    "p",
    "pk",
    "gro",
    "ud",
    "uova",
    "pz",
    "x",
    "moyen",
    "stuk",
    "st",
    "stück",
    "pc",
    "eier",
    "kpl",
    "n",
    "komada",
    "gal",
    "label",
    "szt",
    "stck",
    "egg",
    "unidade",
    "eieren",
    "unité",
    "stk",
    "oeuf",
    "u",
    "xl",
    "l",
    "m",
    "huevo",
    "lg",
    "large",
    "ovo",
    "kla",
    "unit",
    "pièce",
]


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

    if num_eggs == 0:
        return 0
    if weight_per_egg > 0:
        return num_eggs * weight_per_egg
    return num_eggs * AVERAGE_EGG_WEIGHT


def get_egg_weight_from_quantity(quantity: str) -> float:
    """
    Parses quantity into weight in grams.
    """
    if not quantity:
        return 0

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
            if any([u.lower() in DOZEN_EXPRESSIONS for u in unit]):
                egg_weight = number * 12 * AVERAGE_EGG_WEIGHT
            # e.g. '12 M'
            elif any([u.lower() in MOYEN_EXPRESSIONS for u in unit]):
                egg_weight = number * AVERAGE_EGG_WEIGHT
            # e.g. '12 large'
            elif any([u.lower() in LARGE_EXPRESSIONS for u in unit]):
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
        print(f"Could not parse quantity: {quantity}")
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
    product_quantity = product_data.product_quantity
    unit = product_data.product_quantity_unit
    quantity = product_data.quantity
    quantity = product_data.quantity
    categories_tags = product_data.categories_tags or []

    if product_quantity and unit:
        egg_weight = get_egg_weight_from_product_quantity_and_unit(product_quantity, unit)
    elif quantity:
        egg_weight = get_egg_weight_from_quantity(quantity)
    if product_quantity and unit:
        egg_weight = get_egg_weight_from_product_quantity_and_unit(product_quantity, unit)
    elif quantity:
        egg_weight = get_egg_weight_from_quantity(quantity)
    else:
        egg_weight = get_total_egg_weight_from_tags(categories_tags)

    return egg_weight


def calculate_egg_weight(product_data: ProductData) -> float:
    """
    Calculates the weight of eggs based on the product data.

    Returns:
        The egg weight if applicable.
    """

    return calculate_egg_weight_and_reason(product_data)[0]


def extract_quantity_and_unit(text):
    """
    Extracts the first integer and optionally the first word
    (of several letters) from a string.

    Args:
        text: The input string.

    Returns:
        A tuple containing the extracted integer (as an integer) and
        the extracted word (as a string, or None if no word is found),
        or (None, None) if no integer is found.
    """
    if text is None:
        return None, None

    # match_with_text = re.search(r'(\d+)\s*([a-zA-ZœŒçàéèêëîïôöûüÿÀÉÈÊËÎÏÔÖÛÜŸ]+)', text.lower())
    # match_with_text = re.search(r'(\d+)\s*([a-z]+)s?\b', text)
    match_with_text = re.search(r"(\d+,?\.?\d?)\s*([a-zçàéèêëîïôöûüÿ]+)s?\b", text.lower().replace("œ", "oe"))
    if match_with_text:
        quantity = float(match_with_text.group(1).replace(",", "."))
        unit = match_with_text.group(2).rstrip("s")
        return quantity, unit
    else:
        match_only_quantity = re.search(r"(\d+)", text)
        if match_only_quantity:
            quantity = int(match_only_quantity.group(1))
            return quantity, None
        else:
            return None, None


def get_egg_number(product_data: ProductData) -> Optional[int]:
    """
    Extracts a whole number of eggs from the quantity field

    Args:
        product_data: ProductData: The product_data (duh...)

    Returns:
        An integer containing the extracted integer if successful, None otherwise
    """

    if product_data.categories_tags is not None and "en:chicken-eggs" in product_data.categories_tags:  # oeuf
        extracted_quantity, extracted_unit = extract_quantity_and_unit(product_data.quantity)
        if extracted_quantity is None:
            return None
        elif extracted_unit is None:
            return extracted_quantity
        elif extracted_unit in DOZEN_UNIT:
            return 12 * extracted_quantity
        elif extracted_unit in PIECE_UNIT:
            return extracted_quantity
        elif (
            extracted_unit in WEIGHT_UNIT
            and product_data.product_quantity_unit == "g"
            and product_data.product_quantity is not None
        ):
            return int(product_data.product_quantity // AVERAGE_EGG_WEIGHT)
        else:
            return None
    else:  # ovoproduit
        return None
