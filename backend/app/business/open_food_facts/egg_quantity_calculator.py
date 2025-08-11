import re
from typing import List

from app.enums.open_food_facts.enums import EggCaliber, EggQuantity
from app.schemas.open_food_facts.external import ProductData


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

    # Mapping of egg calibers to known category tags
    EGG_CALIBERS_BY_TAG = {
        EggCaliber.SMALL: {"en:small-eggs"},
        EggCaliber.MEDIUM: {"en:medium-eggs-pack-of-10", "en:organic-chicken-eggs-medium-size"},
        EggCaliber.LARGE: {
            "en:large-eggs",
            "en:free-range-organic-large-chicken-eggs",
            "gros-oeufs",
            "en:free-range-large-eggs",
            "en:large-free-run-chicken-eggs",
        },
        EggCaliber.EXTRA_LARGE: {
            "en:extra-large-eggs",
        },
    }

    # Mapping of egg calibers to regex patterns for product names
    # TODO : enhance patterns
    EGG_CALIBERS_BY_EXPRESSION = {
        EggCaliber.SMALL: {r"\b(s|petits?|small)\b"},
        EggCaliber.MEDIUM: {r"\b(m|medium|moyens?)\b"},
        EggCaliber.LARGE: {r"\b(gros|l|xl|large)\b"},
        EggCaliber.EXTRA_LARGE: {r"\b(xl|extra|extra[ -]large|tr[èe]s gros)\b"},
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

    def _get_egg_caliber_from_tags(self, categories_tags: List[str]) -> EggCaliber | None:
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

    def _get_egg_caliber_from_field(self, field: str) -> EggCaliber | None:
        """
        Returns the egg caliber based on the product name.

        Args:
            field (str): A data field containing product information, like product name
            or quantity.
        Returns:
            EggCaliber: The caliber of one egg if a matching tag is found, otherwise None.
        """
        for caliber, expressions in self.pattern_repository.EGG_CALIBERS_BY_EXPRESSION.items():
            if any(re.search(str, field, re.IGNORECASE) for str in expressions):
                return caliber
        return None

    def _get_egg_quantity_from_tags(self, categories_tags: List[str], caliber: EggCaliber | None) -> EggQuantity | None:
        """
        Calculates egg quantity based on information found in categories tags.

        Args:
            categories_tags (List[str]): List of category tags from the product data.
        Returns:
            EggQuantity: The calculated egg quantity with count, total weight, and optional caliber,
            or None if no quantity could be found.
        """

        for tag in categories_tags:
            match = re.search(r"pack-of-(\d+)", tag)
            if match:
                return EggQuantity.from_count(count=int(match.group(1)), caliber=caliber)

        return None

    def _get_egg_quantity_from_product_quantity(self, quantity: str, caliber: EggCaliber | None) -> EggQuantity | None:
        """
        Parses string 'quantity' into egg quantity with count, caliber and weight.

        Args:
            quantity (str): The quantity string to parse, e.g. "6", "1 dozen", "12 large", "x10" etc
        Returns:
            EggQuantity: The calculated egg quantity with count, total weight, and optional caliber,
            or None if no quantity could be found.
        """

        if not quantity:
            return None

        # Case 1: Only numeric (≤30 eggs)
        if re.fullmatch(self.pattern_repository.REGEX_NUMBERS_ONLY, quantity):
            num = float(quantity)
            if num <= 30:
                return EggQuantity.from_count(count=int(num), caliber=caliber)

        # Case 2: Numeric + unit (Latin, Cyrillic, accented, etc.)
        match = re.match(self.pattern_repository.REGEX_NUMERIC_UNIT, quantity)
        if match:
            number = float(match.group(1))
            unit = match.group(2).lower().split()
            # e.g. '1 dozen'
            if any([u.lower() in self.pattern_repository.DOZEN_EXPRESSIONS for u in unit]):
                return EggQuantity.from_count(count=int(number * 12), caliber=caliber)
            # e.g. '12 M'
            elif any([u.lower() in self.pattern_repository.MOYEN_EXPRESSIONS for u in unit]):
                if not caliber:
                    caliber = EggCaliber.MEDIUM
                return EggQuantity.from_count(count=int(number), caliber=caliber)
            # e.g. '12 large'
            elif any([u.lower() in self.pattern_repository.LARGE_EXPRESSIONS for u in unit]):
                if not caliber:
                    caliber = EggCaliber.LARGE
                return EggQuantity.from_count(count=int(number), caliber=caliber)
            else:
                # e.g. '12 unities'
                return EggQuantity.from_count(count=int(number), caliber=caliber)

        # Case 3: x10 / X10 style
        match = re.match(self.pattern_repository.REGEX_X_NUM, quantity)
        if match:
            egg_number = float(match.group(1))
            return EggQuantity.from_count(count=int(egg_number), caliber=caliber)

        # Case 4: Addition expressions: "10 + 2", "12 + 3 oeufs"
        match = re.search(self.pattern_repository.REGEX_ADDITION, quantity)
        if match:
            egg_number = int(match.group(1)) + int(match.group(2))
            return EggQuantity.from_count(count=int(egg_number), caliber=caliber)

        # Case 5: Single number (e.g. "Boîte de 6")
        match = re.search(self.pattern_repository.REGEX_EXTRACT_DIGITS, quantity)
        if match:
            num = int(match.group(1))
            if num < 1000:
                return EggQuantity.from_count(count=int(num), caliber=caliber)

        # If no patterns matched, return None
        print(f"Could not parse quantity: {quantity}")
        return None

    def _get_egg_quantity_from_product_quantity_and_unit(
        self, quantity: float, unit: str, caliber: EggCaliber | None
    ) -> EggQuantity | None:
        """
        Converts product quantity and unit (grams or units) into Egg Quantity : weight, count, and caliber.
        If unit is in COUNT_UNITS, quantity is considered as count of eggs.
        If unit is in the keys of UNIT_CONVERSIONS, use this converter to get the weight.

        Args:
            quantity (float): The quantity of eggs or weight.
            unit (str): The unit of the quantity (e.g. "pcs", "unite", "g", "oz", "lbs", "ml", "l", "litres").

        Returns:
            EggQuantity: The calculated egg quantity with count, total weight, and optional caliber,
            or None if no quantity could be found.
        """
        unit_key = unit.lower()
        if unit in self.pattern_repository.COUNT_UNITS:
            return EggQuantity.from_count(count=int(quantity), caliber=caliber)
        else:
            converter = self.pattern_repository.UNIT_CONVERSIONS.get(unit_key)
            if converter:
                try:
                    weight = round(converter(quantity))
                    return EggQuantity.from_weight(total_weight=weight, caliber=caliber)
                except (ValueError, TypeError):
                    pass

        print(f"Could not parse quantity and unit: {quantity} {unit}")
        return None

    def calculate_egg_quantity(self, product_data: ProductData) -> EggQuantity | None:
        """
        Calculates egg quantity based on the product data.
        First parses categories tags and product name to determine the egg caliber.
        Then parses quantity and unit, quantity alone and finally categories tags to get the egg count

        Args:
            product_data (ProductData): The product data containing quantity, unit, and categories tags.
        Returns:
            EggQuantity: The calculated egg quantity with count, total weight, and optional caliber,
            or None if no quantity could be found.
        """
        product_quantity = product_data.product_quantity
        unit = product_data.product_quantity_unit
        quantity = product_data.quantity or ""
        categories_tags = product_data.categories_tags or []
        product_name = product_data.product_name or ""

        caliber = self._get_egg_caliber_from_tags(categories_tags)

        if not caliber:
            caliber = self._get_egg_caliber_from_field(product_name)

        if not caliber:
            caliber = self._get_egg_caliber_from_field(quantity)

        if product_quantity and unit:
            return self._get_egg_quantity_from_product_quantity_and_unit(product_quantity, unit, caliber)
        elif quantity:
            return self._get_egg_quantity_from_product_quantity(quantity, caliber)
        else:
            return self._get_egg_quantity_from_tags(categories_tags, caliber)
