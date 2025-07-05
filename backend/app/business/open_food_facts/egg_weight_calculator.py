import re
from enum import StrEnum
from typing import List

from app.schemas.open_food_facts.external import ProductData


class EggSize(StrEnum):
    """Egg sizes with their corresponding weights in grams."""

    LARGE = "large"
    GRADE_A = "grade_a"
    MEDIUM = "medium"
    AVERAGE = "average"

    @property
    def weight(self) -> int:
        return {
            EggSize.LARGE: 60,
            EggSize.GRADE_A: 55,
            EggSize.MEDIUM: 50,
            EggSize.AVERAGE: 50,
        }[self]


class PatternRepository:
    """
    Repository for constants and patterns used to estimate egg weight and convert units.

    Attributes:
        UNIT_CONVERSIONS (dict): Mapping of units to conversion lambdas returning weight in grams.
        EGG_WEIGHTS_BY_TAG (dict): Mapping of egg weight values to known category tags.
        REGEX_* (str): Regex patterns used to extract numeric quantities from strings.
        *_EXPRESSIONS (list): Lists of keywords used to identify specific egg sizes or quantities.
    """

    # Conversion functions for various units to grams
    UNIT_CONVERSIONS = {
        # 1 piece or similar unit = average egg weight
        "pcs": lambda q: float(q) * EggSize.AVERAGE.weight,
        "sans": lambda q: float(q) * EggSize.AVERAGE.weight,
        "unite": lambda q: float(q) * EggSize.AVERAGE.weight,
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
    EGG_WEIGHTS_BY_TAG = {
        60: {
            "en:large-eggs",
            "en:free-range-organic-large-chicken-eggs",
            "gros-oeufs",
            "en:free-range-large-eggs",
            "en:large-free-run-chicken-eggs",
        },
        55: {"en:grade-a-eggs"},
        50: {"en:medium-eggs-pack-of-10", "en:organic-chicken-eggs-medium-size"},
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

    # Simple expressions used to identify egg sizes and count
    DOZEN_EXPRESSIONS = ["dozen", "dozens", "dzn", "doz"]
    MOYEN_EXPRESSIONS = ["m", "moyen", "moyens"]
    LARGE_EXPRESSIONS = ["gros", "l", "xl", "large"]


class EggWeightCalculator:
    """
    Utility for calculating the weight of eggs using various inputs:
    category tags, free-form quantities, unit-based measurements, or structured product data.

    """

    def __init__(self):
        self.pattern_repository = PatternRepository

    def get_egg_weight_by_tag(self, categories_tags: List[str]) -> int:
        """
        Returns the standard weight of one egg based on category tags.
        """
        for weight, tags in self.pattern_repository.EGG_WEIGHTS_BY_TAG.items():
            if any(tag in categories_tags for tag in tags):
                return weight
        return 0

    def get_number_of_eggs(self, categories_tags: List[str]) -> int:
        """
        Extracts the number of eggs from tags.
        TODO: Add support for other tags
        """
        for tag in categories_tags:
            match = re.search(r"pack-of-(\d+)", tag)
            if match:
                return int(match.group(1))
        return 0

    def get_total_egg_weight_from_tags(self, categories_tags: List[str]) -> float:
        """
        Calculates total egg weight based on standard weights and pack size.
        """
        num_eggs = self.get_number_of_eggs(categories_tags)
        weight_per_egg = self.get_egg_weight_by_tag(categories_tags)

        if num_eggs == 0:
            return 0
        if weight_per_egg > 0:
            return num_eggs * weight_per_egg
        return num_eggs * EggSize.AVERAGE.weight

    def get_egg_weight_from_quantity(self, quantity: str) -> float:
        """
        Parses quantity into weight in grams.
        """
        if not quantity:
            return 0

        # Case 1: Only numeric (≤30 eggs)
        parsed = False
        if re.fullmatch(self.pattern_repository.REGEX_NUMBERS_ONLY, quantity):
            num = float(quantity)
            if num <= 30:
                parsed = True
                return num * EggSize.AVERAGE.weight

        # Case 2: Numeric + unit (Latin, Cyrillic, accented, etc.)
        if not parsed:
            match = re.match(self.pattern_repository.REGEX_NUMERIC_UNIT, quantity)
            if match:
                number = float(match.group(1))
                unit = match.group(2).lower().split()
                # e.g. '1 dozen'
                if any([u.lower() in self.pattern_repository.DOZEN_EXPRESSIONS for u in unit]):
                    egg_weight = number * 12 * EggSize.AVERAGE.weight
                # e.g. '12 M'
                elif any([u.lower() in self.pattern_repository.MOYEN_EXPRESSIONS for u in unit]):
                    egg_weight = number * EggSize.AVERAGE.weight
                # e.g. '12 large'
                elif any([u.lower() in self.pattern_repository.LARGE_EXPRESSIONS for u in unit]):
                    egg_weight = number * EggSize.LARGE.weight
                else:
                    # e.g. '12 unities'
                    egg_weight = number * EggSize.AVERAGE.weight
                parsed = True
                return egg_weight

        # Case 3: x10 / X10 style
        if not parsed:
            match = re.match(self.pattern_repository.REGEX_X_NUM, quantity)
            if match:
                egg_number = float(match.group(1))
                parsed = True
                return egg_number * EggSize.AVERAGE.weight

        # Case 4: Addition expressions: "10 + 2", "12 + 3 oeufs"
        if not parsed:
            match = re.search(self.pattern_repository.REGEX_ADDITION, quantity)
            if match:
                egg_number = int(match.group(1)) + int(match.group(2))
                parsed = True
                return egg_number * EggSize.AVERAGE.weight

        # Case 5: Single number (e.g. "Boîte de 6")
        if not parsed:
            match = re.search(self.pattern_repository.REGEX_EXTRACT_DIGITS, quantity)
            if match:
                num = int(match.group(1))
                if num < 1000:
                    parsed = True
                    return num * EggSize.AVERAGE.weight

        if not parsed:
            print(f"Could not parse quantity: {quantity}")
            return 0

        return 0

    def get_egg_weight_from_product_quantity_and_unit(self, quantity: float, unit: str) -> float:
        """
        Converts product quantity and unit into weight in grams.
        """
        unit_key = unit.lower()
        converter = self.pattern_repository.UNIT_CONVERSIONS.get(unit_key)
        if converter:
            try:
                return converter(quantity)
            except (ValueError, TypeError):
                pass
        return 0

    def calculate_egg_weight(self, product_data: ProductData) -> float | None:
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
            egg_weight = self.get_egg_weight_from_product_quantity_and_unit(product_quantity, unit)
        elif quantity:
            egg_weight = self.get_egg_weight_from_quantity(quantity)
        else:
            egg_weight = self.get_total_egg_weight_from_tags(categories_tags)

        if egg_weight > 0:
            return egg_weight
        else:
            return None


def calculate_egg_weight(product_data: ProductData) -> float | None:
    """Convenience function to calculate egg weight using the EggWeightCalculator"""
    return EggWeightCalculator().calculate_egg_weight(product_data)
