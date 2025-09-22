import re
from typing import List

from app.enums.open_food_facts.egg_quantity_enums import EggQuantityPatternRepository
from app.enums.open_food_facts.enums import EggCaliber, EggQuantity
from app.schemas.open_food_facts.external import ProductData


class EggQuantityCalculator:
    """
    Utility for calculating the weight of eggs using various inputs:
    category tags, free-form quantities, unit-based measurements, or structured product data.
    """

    def __init__(self):
        self.pattern_repository = EggQuantityPatternRepository

    def _get_egg_caliber_from_tags(self, categories_tags: List[str]) -> EggCaliber | None:
        """
        Returns the egg caliber based on category tags
        Parses small, medium, large, and then extra-large egg calibers, returns the smallest
        matching caliber

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
        Returns the egg caliber based on a fields, product name or quantity
        Parses small, medium, large, and then extra-large egg calibers, returns the smallest
        matching caliber

        Args:
            field (str): A data field containing product information
        Returns:
            EggCaliber: The caliber of one egg if a matching tag is found, otherwise None.
        """
        for caliber, expressions in self.pattern_repository.EGG_CALIBERS_BY_EXPRESSION.items():
            if any(
                re.search(str, EggQuantityPatternRepository.prepare_string_to_parse_egg_caliber(field))
                for str in expressions
            ):
                return caliber
        return None

    def _get_egg_quantity_from_ingredients(
        self, ingredients_tags: List[str], caliber: EggCaliber | None
    ) -> EggQuantity | None:
        """
        Calculates egg quantity based on information found in categories tags.
        Only 12 egg(s) or 12 oeufs patterns are supported.
        Args:
            categories_tags (List[str]): List of category tags from the product data.
        Returns:
            EggQuantity: The calculated egg quantity with count, total weight, and optional caliber,
            or None if no quantity could be found.
        """
        if not ingredients_tags:
            return None

        for ingredient in ingredients_tags:
            ingredient = EggQuantityPatternRepository._normalize_common(ingredient)
            match = re.search(EggQuantityPatternRepository.REGEX_INGREDIENTS, ingredient)
            if match:
                return EggQuantity.from_count(count=int(match.group(1)), caliber=caliber)

        return None

    def _get_egg_quantity_from_name(self, name: str, caliber: EggCaliber | None) -> EggQuantity | None:
        """
        Calculates egg quantity based on information found in the product name.

        Args:
            product_name (str): The product name from the product data.
        """
        name = EggQuantityPatternRepository.prepare_string_to_parse_egg_count(name)

        # Case : 'One dozen' or '5 dozen'
        match = re.search(EggQuantityPatternRepository.REGEX_DOZEN, name)
        if match:
            number = int(match.group(1)) if match.group(1) else 1
            egg_number = number * 12
            return EggQuantity.from_count(count=egg_number, caliber=caliber)

        # Case : '10+2 eggs'
        match = re.search(EggQuantityPatternRepository.REGEX_ADDITION, name)
        if match:
            egg_number = int(match.group(1)) + int(match.group(2))
            return EggQuantity.from_count(count=int(egg_number), caliber=caliber)

        # Case : ' 10 [...] eggs' or 'X10' or '10' or '10u
        matches = re.findall(EggQuantityPatternRepository.REGEX_NUMBER_ISOLATED_OR_STUCK_UNIT, name)
        if matches:
            match = matches[0]  # Take the first match
            egg_number = int(match[0] or match[1])
            if egg_number <= self.pattern_repository.MAX_EGG_COUNT:
                return EggQuantity.from_count(count=egg_number, caliber=caliber)

        return None

    def _get_egg_quantity_from_quantity_as_count(self, quantity: str, caliber: EggCaliber | None) -> EggQuantity | None:
        """
        Parses string 'quantity' into egg quantity with count, caliber and weight.

        Args:
            quantity (str): The quantity string to parse, e.g. "6", "1 dozen", "12 large", "x10" etc
        Returns:
            EggQuantity: The calculated egg quantity with count, total weight, and optional caliber,
            or None if no quantity could be found.
        """

        if not quantity or quantity == "":
            return None

        quantity = EggQuantityPatternRepository.prepare_string_to_parse_egg_count(quantity)

        # Case : Only numeric (≤30 eggs)
        if re.fullmatch(self.pattern_repository.REGEX_NUMBERS_ONLY, quantity):
            num = float(quantity)
            if num <= self.pattern_repository.MAX_EGG_COUNT:
                return EggQuantity.from_count(count=int(num), caliber=caliber)

        # Case : Numeric + unit (Latin, Cyrillic, accented, etc.)
        match = re.match(self.pattern_repository.REGEX_NUMERIC_UNIT, quantity)
        if match:
            number = float(match.group(1))
            unit = match.group(2).lower().split()
            # e.g. '1 dozen'
            if any([u.lower() in self.pattern_repository.DOZEN_EXPRESSIONS for u in unit]):
                egg_number = int(number * 12)
                return EggQuantity.from_count(count=egg_number, caliber=caliber)
            else:
                # e.g. '12 unities' or '12 large'
                egg_number = int(number)
                if egg_number <= self.pattern_repository.MAX_EGG_COUNT:
                    return EggQuantity.from_count(count=egg_number, caliber=caliber)

        # Case : Addition expressions: "10 + 2", "12 + 3 oeufs"
        match = re.search(self.pattern_repository.REGEX_ADDITION, quantity)
        if match:
            egg_number = int(match.group(1)) + int(match.group(2))
            return EggQuantity.from_count(count=int(egg_number), caliber=caliber)

        # Case : x10 / X10 style ou 10u
        matches = re.findall(EggQuantityPatternRepository.REGEX_NUMBER_ISOLATED_OR_STUCK_UNIT, quantity)
        if matches:
            match = matches[0]  # Take the first match
            if match:
                egg_number = int(match[0] or match[1])
                if egg_number <= self.pattern_repository.MAX_EGG_COUNT:
                    return EggQuantity.from_count(count=egg_number, caliber=caliber)

        # Case : Single number (e.g. "Boîte de 6")
        match = re.search(self.pattern_repository.REGEX_EXTRACT_DIGITS, quantity)
        if match:
            num = int(match.group(1))
            if num < self.pattern_repository.MAX_EGG_COUNT:
                return EggQuantity.from_count(count=int(num), caliber=caliber)

        # If no patterns matched, return None
        return None

    def _get_egg_quantity_from_quantity_as_weight(
        self, quantity: str, caliber: EggCaliber | None
    ) -> EggQuantity | None:
        """
        Parses string 'quantity' into egg weight if no count was found

        Args:
            quantity (str): The quantity string to parse, e.g. "500 g", "1.5 lbs", "0.5 kg" etc
        Returns:
            EggQuantity: The calculated egg quantity with count, total weight, and optional caliber,
            or None if no quantity could be found.
        """

        if not quantity or quantity == "":
            return None

        quantity = EggQuantityPatternRepository.prepare_string_to_parse_weight(quantity)

        # Find 100 g or 10 oz
        match = re.findall(self.pattern_repository.REGEX_WEIGHT_UNIT, quantity)
        if match:
            match = match[0]  # Take the first match
            number = float(match[0])
            unit = match[1].lower().strip()
            converter = self.pattern_repository.UNIT_CONVERSIONS.get(unit)
            if converter:
                try:
                    weight = round(converter(number))
                    return EggQuantity.from_weight(total_weight=weight, caliber=caliber)
                except (ValueError, TypeError):
                    pass

        # If no patterns matched, return None
        print(f"Could not parse quantity as weight: {quantity}")
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
        First parses categories tags, product name, generic name and quantity to determine the egg caliber.
        Then, to get quantity, parses :
        - quantity as count (e.g. "6", "1 dozen", "12 large", "x10" etc)
        - product name (e.g. "box of 6 eggs", "12 + 3 eggs", "x10 eggs" etc)
        - generic name (e.g. "box of 6 eggs", "12 + 3 eggs", "x10 eggs" etc)
        - ingredients tags (e.g. "6-eggs", "en:12-large-eggs" etc)
        - product quantity and unit, only weight (e.g. 500 g, 1.5 lbs, 0.5 kg, 6 pcs, 12 unities etc)
        - quantity as weight (e.g. "500 g", "1.5 lbs", "0.5 kg" etc)
        in this order, returning the first valid egg quantity found.

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
        generic_name = product_data.generic_name or ""
        ingredients_tags = product_data.ingredients_tags or []

        caliber = self._get_egg_caliber_from_tags(categories_tags)
        if not caliber:
            caliber = self._get_egg_caliber_from_field(product_name)
        if not caliber:
            caliber = self._get_egg_caliber_from_field(generic_name)
        if not caliber:
            caliber = self._get_egg_caliber_from_field(quantity)

        egg_quantity = None

        if quantity:
            egg_quantity = self._get_egg_quantity_from_quantity_as_count(quantity, caliber)
        if not egg_quantity:
            egg_quantity = self._get_egg_quantity_from_name(product_name, caliber)
        if not egg_quantity:
            egg_quantity = self._get_egg_quantity_from_name(generic_name, caliber)
        if not egg_quantity:
            egg_quantity = self._get_egg_quantity_from_ingredients(ingredients_tags, caliber)
        if (product_quantity and unit) and (not egg_quantity):
            egg_quantity = self._get_egg_quantity_from_product_quantity_and_unit(product_quantity, unit, caliber)
        if quantity and (not egg_quantity):
            egg_quantity = self._get_egg_quantity_from_quantity_as_weight(quantity, caliber)

        return egg_quantity
