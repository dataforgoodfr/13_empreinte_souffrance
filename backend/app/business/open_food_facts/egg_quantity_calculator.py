import re
from dataclasses import dataclass
from typing import List, Optional

from app.enums.open_food_facts.enums import EggCaliber
from app.schemas.open_food_facts.external import ProductData


@dataclass
class EggQuantity:
    """
    Result of egg weight calculation containing all relevant information.

    Attributes:
        count: Number of eggs in the product
        caliber: Caliber of the eggs if known
        total_weight: Total weight of all eggs in grams
    """

    count: int
    total_weight: float
    caliber: EggCaliber | None = None

    @classmethod
    def from_count(cls, count: int, caliber: EggCaliber | None = None) -> Optional["EggQuantity"]:
        if count <= 0:
            return None
        egg_weight = caliber.weight if caliber else EggCaliber.AVERAGE.weight
        total_weight = count * egg_weight
        return cls(count=count, total_weight=total_weight, caliber=caliber)

    @classmethod
    def from_weight(cls, total_weight: float, caliber: EggCaliber | None = None) -> Optional["EggQuantity"]:
        if total_weight <= 0:
            return None
        egg_weight = caliber.weight if caliber else EggCaliber.AVERAGE.weight
        count = round(total_weight / egg_weight)
        return cls(count=count, total_weight=total_weight, caliber=caliber)


class PatternRepository:
    """
    Repository for constants and patterns used to estimate egg weight and convert units.

    Attributes:
        UNIT_CONVERSIONS (dict): Mapping of units to conversion lambdas returning weight in grams.
        EGG_CALIBERS_BY_TAG (dict): Mapping of egg caliber to known category tags.
        REGEX_* (str): Regex patterns used to extract numeric quantities from strings.
        *_EXPRESSIONS (list): Lists of keywords used to identify specific egg calibers or quantities.
    """

    # Conversion functions for various units to grams

    COUNT_UNITS = {"pcs", "sans", "unite"}

    UNIT_CONVERSIONS = {
        # Metric weight units
        "g": lambda q: float(q),
        "gr": lambda q: float(q),
        "gramm": lambda q: float(q),
        # Imperial units
        "oz": lambda q: float(q) * 28.35,
        "lbs": lambda q: float(q) * 453.59,
        # Volume units converted assuming egg density ~1.03g/ml
        "ml": lambda q: float(q) * 1.03,
        "l": lambda q: float(q) * 1030,
        "litres": lambda q: float(q) * 1030,
    }

    # Mapping known category tags to average egg weight in grams
    EGG_CALIBERS_BY_TAG = {
        EggCaliber.LARGE: {
            "en:large-eggs",
            "en:free-range-organic-large-chicken-eggs",
            "gros-oeufs",
            "en:free-range-large-eggs",
            "en:large-free-run-chicken-eggs",
        },
        EggCaliber.MEDIUM: {"en:medium-eggs-pack-of-10", "en:organic-chicken-eggs-medium-size"},
    }

    # Regex: matches a number alone (e.g. "6")
    REGEX_NUMBERS_ONLY = r"\s*\d+(\.\d+)?\s*"

    # Regex: matches number + unit (e.g. "6 eggs", "12 pcs", "3 gros")
    REGEX_NUMERIC_UNIT = r"\s*(\d+(?:\.\d+)?)\s*((?:[a-zA-Zа-яА-ЯёЁ\u00C0-\u00FFœŒ]+\s*)+)\.?"

    # Regex: matches formats like "x10", "X12"
    REGEX_X_NUM = r"[xX]\s*(\d+(?:\.\d+)?)"

    # Regex: matches addition patterns like "10 + 2"
    REGEX_ADDITION = r"(\d+)\s*\+\s*(\d+)"

    # Regex: extracts any number ≤ 999 from a string (e.g. "boîte de 6 œufs")
    REGEX_EXTRACT_DIGITS = r"\b(\d{1,3})\b"

    # Simple expressions used to identify egg calibers and count
    DOZEN_EXPRESSIONS = ["dozen", "dozens", "dzn", "doz"]
    MOYEN_EXPRESSIONS = ["m", "moyen", "moyens"]
    LARGE_EXPRESSIONS = ["gros", "l", "xl", "large"]


class EggQuantityCalculator:
    """
    Utility for calculating the weight of eggs using various inputs:
    category tags, free-form quantities, unit-based measurements, or structured product data.

    """

    def __init__(self):
        self.pattern_repository = PatternRepository

    def get_egg_caliber_by_tag(self, categories_tags: List[str]) -> EggCaliber | None:
        """
        Returns the egg caliber based on category tags.

        Args:
            categories_tags (List[str]): List of category tags from the product data.
        Returns:
            EggCaliber: The caliber of one egg if a matching tag is found, otherwise None.
        """
        for caliber, tags in self.pattern_repository.EGG_CALIBERS_BY_TAG.items():
            if any(tag in categories_tags for tag in tags):
                return caliber
        return None

    def get_number_of_eggs(self, categories_tags: List[str]) -> int:
        """
        Extracts the number of eggs from categories tags, for now pack size.
        TODO: Add support for other tags

        Args:
            categories_tags (List[str]): List of category tags from the product data.
        Returns:
            int: The number of eggs if a number is found, otherwise 0.
        """
        for tag in categories_tags:
            match = re.search(r"pack-of-(\d+)", tag)
            if match:
                return int(match.group(1))
        return 0

    def get_egg_quantity_from_tags(self, categories_tags: List[str]) -> EggQuantity | None:
        """
        Calculates egg quantity based on information found in categories tags.

        Args:
            categories_tags (List[str]): List of category tags from the product data.
        Returns:
            EggQuantity: The calculated egg quantity with count, total weight, and caliber.
        """
        num_eggs = self.get_number_of_eggs(categories_tags)
        egg_caliber = self.get_egg_caliber_by_tag(categories_tags)

        if num_eggs == 0:
            return None

        return EggQuantity.from_count(count=num_eggs, caliber=egg_caliber)

    def get_egg_quantity_from_product_quantity(self, quantity: str) -> EggQuantity | None:
        """
        Parses string 'quantity' into egg quantity with count, caliber and weight.

        Args:
            quantity (str): The quantity string to parse, e.g. "6", "1 dozen", "12 large", "x10" etc
        Returns:
            EggQuantity: The calculated egg quantity with count, total weight, and caliber.
        """

        if not quantity:
            return None

        # Case 1: Only numeric (≤30 eggs)
        if re.fullmatch(self.pattern_repository.REGEX_NUMBERS_ONLY, quantity):
            num = float(quantity)
            if num <= 30:
                return EggQuantity.from_count(count=int(num))

        # Case 2: Numeric + unit (Latin, Cyrillic, accented, etc.)
        match = re.match(self.pattern_repository.REGEX_NUMERIC_UNIT, quantity)
        if match:
            number = float(match.group(1))
            unit = match.group(2).lower().split()
            # e.g. '1 dozen'
            if any([u.lower() in self.pattern_repository.DOZEN_EXPRESSIONS for u in unit]):
                return EggQuantity.from_count(count=int(number * 12))
            # e.g. '12 M'
            elif any([u.lower() in self.pattern_repository.MOYEN_EXPRESSIONS for u in unit]):
                return EggQuantity.from_count(count=int(number), caliber=EggCaliber.MEDIUM)
            # e.g. '12 large'
            elif any([u.lower() in self.pattern_repository.LARGE_EXPRESSIONS for u in unit]):
                return EggQuantity.from_count(count=int(number), caliber=EggCaliber.LARGE)
            else:
                # e.g. '12 unities'
                return EggQuantity.from_count(count=int(number))

        # Case 3: x10 / X10 style
        match = re.match(self.pattern_repository.REGEX_X_NUM, quantity)
        if match:
            egg_number = float(match.group(1))
            return EggQuantity.from_count(count=int(egg_number))

        # Case 4: Addition expressions: "10 + 2", "12 + 3 oeufs"
        match = re.search(self.pattern_repository.REGEX_ADDITION, quantity)
        if match:
            egg_number = int(match.group(1)) + int(match.group(2))
            return EggQuantity.from_count(count=int(egg_number))

        # Case 5: Single number (e.g. "Boîte de 6")
        match = re.search(self.pattern_repository.REGEX_EXTRACT_DIGITS, quantity)
        if match:
            num = int(match.group(1))
            if num < 1000:
                return EggQuantity.from_count(count=int(num))

        # If no patterns matched, return None
        print(f"Could not parse quantity: {quantity}")
        return None

    def get_egg_quantity_from_product_quantity_and_unit(self, quantity: float, unit: str) -> EggQuantity | None:
        """
        Converts product quantity and unit (grams or units) into Egg Quantity : weight, count, and caliber.
        If unit is in COUNT_UNITS, quantity is considered as count of eggs.
        If unit is in the keys of UNIT_CONVERSIONS, use this converter to get the weight.

        Args:
            quantity (float): The quantity of eggs or weight.
            unit (str): The unit of the quantity (e.g. "pcs", "unite", "g", "oz", "lbs", "ml", "l", "litres").

        Returns:
            EggQuantity: The calculated egg quantity with count, total weight, and caliber.
        """
        unit_key = unit.lower()
        if unit in self.pattern_repository.COUNT_UNITS:
            return EggQuantity.from_count(count=int(round(quantity)))
        else:
            converter = self.pattern_repository.UNIT_CONVERSIONS.get(unit_key)
            if converter:
                try:
                    weight = converter(quantity)
                    return EggQuantity.from_weight(total_weight=weight)
                except (ValueError, TypeError):
                    pass

        print(f"Could not parse quantity and unit: {quantity} {unit}")
        return None

    def calculate_egg_quantity(self, product_data: ProductData) -> EggQuantity | None:
        """
        Calculates egg quantity based on the product data.

        Args:
            product_data (ProductData): The product data containing quantity, unit, and categories tags.
        Returns:
            EggQuantity: The calculated egg quantity with count, total weight, and caliber.
        """
        product_quantity = product_data.product_quantity
        unit = product_data.product_quantity_unit
        quantity = product_data.quantity
        categories_tags = product_data.categories_tags or []

        if product_quantity and unit:
            return self.get_egg_quantity_from_product_quantity_and_unit(product_quantity, unit)
        elif quantity:
            return self.get_egg_quantity_from_product_quantity(quantity)
        else:
            return self.get_egg_quantity_from_tags(categories_tags)
