import re
import unicodedata
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

    # Mapping of egg calibers to regex patterns for product names and quantities
    EGG_CALIBERS_BY_EXPRESSION = {
        # exclude " s' " and " 's " expressions
        EggCaliber.SMALL: {r"(?<!['’])\b(s|petits?|small)\b(?!['’])"},
        # exclude " m' " expressions
        EggCaliber.MEDIUM: {r"\b(m|medium|moyens?|medie)\b(?!['’])"},
        # exclude extra-large  and " l' " expressions
        EggCaliber.LARGE: {r"(?<!\bextra\s)(?<!\btres\s)\b(gros|large|l)\b(?!['’])"},
        EggCaliber.EXTRA_LARGE: {r"\b(xl|extra\slarge|tr[èe]s\sgros)\b"},
    }

    # Maximum count accepted as sole number
    MAX_EGG_COUNT = 250

    # Regex: matches a number alone (e.g. "6" or 12.5)
    REGEX_NUMBERS_ONLY = r"\s*\d+([.,]\d+)?\s*"

    COUNT_UNITS = {
        "pcs",
        "sans",
        "unite",
        "m",
        "moyen",
        "moyens",
        "gros",
        "xl",
        "large",
        "u",
        "un",
        "pk",
        "piece",
        "pieces",
    }

    # Checks for isolated numbers or specific units(e.g. "6" or "x6" but not "6C")
    REGEX_NUMBER_ISOLATED_OR_STUCK_UNIT = r"\b(?:x\s*(\d+)|(\d+)\s*(?:" + r"|".join(COUNT_UNITS) + r")?)\b"

    # Regex: matches number + unit (e.g. "6 eggs", "12 pcs", "3 gros", '1.5 dozen')
    REGEX_NUMERIC_UNIT = r"\s*(\d+(?:[.,]\d+)?)\s*((?:[a-zA-Zа-яА-ЯёЁ\u00C0-\u00FFœŒ]+\s*)+)\.?"

    # Regex: matches addition patterns like "10 + 2"
    REGEX_ADDITION = r"(\d+)\s*\+\s*(\d+)"

    # Regex: extracts any number ≤ 999 from a string (e.g. "boîte de 6 œufs")
    REGEX_EXTRACT_DIGITS = r"\b(\d{1,3})\b"

    # Regex for ingredients : '12 large eggs' or '6 oeufs'
    REGEX_INGREDIENTS = r"(\d+).*?(?:eggs?|oeufs?)"

    # Text expressions used to identify egg count like dozens
    DOZEN_EXPRESSIONS = {"dozen", "dozens", "dzn", "doz"}
    REGEX_DOZEN = r"(\d+)?\s*(?:" + r"|".join(DOZEN_EXPRESSIONS) + r")"

    # Conversion functions for various units to grams
    UNIT_CONVERSIONS = {
        # Metric weight units
        "g": lambda q: float(q),
        "gr": lambda q: float(q),
        "gram": lambda q: float(q),
        "grams": lambda q: float(q),
        "gramm": lambda q: float(q),
        "kg": lambda q: float(q) * 1000,
        # Imperial units
        "oz": lambda q: float(q) * 28.35,
        "lbs": lambda q: float(q) * 453.59,
        "lb": lambda q: float(q) * 453.59,
        # Volume units converted assuming egg density ~1.03g/ml
        "ml": lambda q: float(q) * 1.03,
        "l": lambda q: float(q) * 1030,
        "litres": lambda q: float(q) * 1030,
    }

    # Regex: matches number + weight unit (e.g. "6g", "12 litres", "8 oz")
    REGEX_WEIGHT_UNIT = r"(\d+(?:[.,]\d+)?)(?:\s*)(" + "|".join(UNIT_CONVERSIONS.keys()) + ")"

    @staticmethod
    def _normalize_common(s: str) -> str:
        """
        Common normalization:
        - Remove accents
        - Normalize unicode
        - Replace œ with oe
        - Replace multiple spaces with a single space
        - Strip leading and trailing spaces
        """
        s = "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
        s = unicodedata.normalize("NFKD", s)
        s = re.sub(r"œ", "oe", s)
        s = re.sub(r"\s+", " ", s)
        return s.strip()

    @staticmethod
    def prepare_string_to_parse_egg_count(s: str) -> str:
        """
        Normalizes a string for parsing egg count:
        - Remove numbers followed by '%'
        - Merge numbers separated by space in thousands (e.g., '1 200' -> '1200')
        - Keep only the upper bound in ranges (e.g., '53 - 63' -> '63')
        - Remove quantities with weight/volume units (g, kg, ml, oz, lbs, etc.)
        - Replace fractions '1/2' with '.5'
        - Replace 'one' with '1'
        - Remove 'omega 3'
        - Remove size mentions (e.g., 'size 4')
        - Normalize unicode, accents, and punctuation (keep + . ,)
        - Reduce multiple spaces to single space
        """
        if not s:
            return ""
        s = str(s).lower()
        s = re.sub(r"\d+\s*%", "", s)
        s = re.sub(r"\b(\d+)\s+(\d{3})\b", r"\1\2", s)
        s = re.sub(r"\b(\d+)\s*-\s*(\d+)", r"\2", s)
        s = re.sub(r"\b\d+(?:[.,]\d+)?\s*(?:g|gram[ms]?|oz|ml|lbs?|gr|litres|kg|l)\b", "", s)
        s = re.sub(r"\b1/2\b", ".5", s)
        s = PatternRepository._normalize_common(s)
        s = re.sub(r"[^\w\s+.,]", " ", s)
        s = re.sub(r"\bone\b", "1", s)
        s = re.sub(r"\bomega\s*3\b", "", s)
        s = re.sub(r"\bsize\s*\d+\b", "", s)
        s = re.sub(r"\s+", " ", s).strip()
        return s

    @staticmethod
    def prepare_string_to_parse_egg_caliber(s: str) -> str:
        """
        Normalizes a string for parsing egg caliber:
        - Remove digits
        - Remove accents
        - Normalize unicode
        - Replace œ with oe
        - Replace punctuation (except apostrophes) with space
        - Convert to lowercase
        - Reduce multiple spaces to single space
        """
        if not s:
            return ""
        s = str(s)
        s = PatternRepository._normalize_common(s)
        s = re.sub(r"[^\w\s'’]", " ", s)
        s = re.sub(r"\d+", " ", s)
        s = s.lower()
        s = re.sub(r"\s+", " ", s).strip()
        return s

    @staticmethod
    def prepare_string_to_parse_weight(s: str) -> str:
        """
        Normalizes a string for parsing weight:
        - Merge numbers separated by space in thousands (e.g., '1 200' -> '1200')
        - Remove accents
        - Normalize unicode
        - Replace œ with oe
        - Convert to lowercase
        - Reduce multiple spaces to single space
        """
        if not s:
            return ""
        s = str(s)
        s = re.sub(r"\b(\d+)\s+(\d{3})\b", r"\1\2", s)
        s = PatternRepository._normalize_common(s)
        s = s.lower()
        return s


class EggQuantityCalculator:
    """
    Utility for calculating the weight of eggs using various inputs:
    category tags, free-form quantities, unit-based measurements, or structured product data.
    """

    def __init__(self):
        self.pattern_repository = PatternRepository

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
            if any(re.search(str, PatternRepository.prepare_string_to_parse_egg_caliber(field)) for str in expressions):
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
            ingredient = PatternRepository._normalize_common(ingredient)
            match = re.search(PatternRepository.REGEX_INGREDIENTS, ingredient)
            if match:
                print(f"Extracted count from ingredients_tags: {match.group(1)[:10]}")
                return EggQuantity.from_count(count=int(match.group(1)), caliber=caliber)

        return None

    def _get_egg_quantity_from_name(self, name: str, caliber: EggCaliber | None) -> EggQuantity | None:
        """
        Calculates egg quantity based on information found in the product name.

        Args:
            product_name (str): The product name from the product data.
        """
        name = PatternRepository.prepare_string_to_parse_egg_count(name)

        # Case : 'One dozen' or '5 dozen'
        match = re.search(PatternRepository.REGEX_DOZEN, name)
        if match:
            number = int(match.group(1)) if match.group(1) else 1
            egg_number = number * 12
            return EggQuantity.from_count(count=egg_number, caliber=caliber)

        # Case : '10+2 eggs'
        match = re.search(PatternRepository.REGEX_ADDITION, name)
        if match:
            egg_number = int(match.group(1)) + int(match.group(2))
            return EggQuantity.from_count(count=int(egg_number), caliber=caliber)

        # Case : ' 10 [...] eggs' or 'X10' or '10' or '10u
        matches = re.findall(PatternRepository.REGEX_NUMBER_ISOLATED_OR_STUCK_UNIT, name)
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

        quantity = PatternRepository.prepare_string_to_parse_egg_count(quantity)

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
        matches = re.findall(PatternRepository.REGEX_NUMBER_ISOLATED_OR_STUCK_UNIT, quantity)
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
        # print(f"Could not parse quantity as egg count: {quantity}")
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

        quantity = PatternRepository.prepare_string_to_parse_weight(quantity)

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
