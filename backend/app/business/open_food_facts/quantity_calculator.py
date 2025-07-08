import re
from dataclasses import dataclass
from typing import List, TypeAlias

from app.enums.open_food_facts.enums import EggCaliber
from app.schemas.open_food_facts.external import ProductData
from app.schemas.open_food_facts.internal import AnimalType, ProductType


@dataclass
class EggQuantity:
    """
    Result of egg weight calculation containing all relevant information.

    Attributes:
        count: Number of eggs in the product
        caliber: Caliber of the eggs if known
        total_weight: Total weight of all eggs in grams
    """

    count: int | None = None
    caliber: EggCaliber | None = None
    total_weight: float | None = None
    is_complete: bool = False

    def fill_from_count(self, count: int, caliber: EggCaliber | None = None) -> None:
        self.count = count
        self.caliber = caliber
        self.total_weight = count * caliber.weight if caliber else count * EggCaliber.AVERAGE.weight
        self.is_complete = True

    def fill_from_weight(self, weight: float) -> None:
        self.total_weight = weight
        self.count = int(round(weight / EggCaliber.AVERAGE.weight))
        self.is_complete = True


ProductQuantity: TypeAlias = float | None
# float to be changed to EggQuantity while letting PainReportCalculator and KnowledgePanel parse EggQuantity


class PatternRepository:
    """
    Repository for constants and patterns used to estimate egg weight and convert units.

    Attributes:
        UNIT_CONVERSIONS (dict): Mapping of units to conversion lambdas returning weight in grams.
        EGG_WEIGHTS_BY_TAG (dict): Mapping of egg weight values to known category tags.
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
        self.quantity = EggQuantity()

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

    def get_egg_quantity_from_tags(self, categories_tags: List[str]) -> EggQuantity:
        """
        Calculates egg quantity based on standard weights and pack size.
        """
        num_eggs = self.get_number_of_eggs(categories_tags)
        weight_per_egg = self.get_egg_weight_by_tag(categories_tags)

        if num_eggs == 0:
            return self.quantity
        if weight_per_egg > 0:
            self.quantity.is_complete = True
            self.quantity.count = num_eggs
            self.quantity.total_weight = num_eggs * weight_per_egg
            return self.quantity
        self.quantity.fill_from_count(num_eggs)
        return self.quantity

    def get_egg_quantity_from_product_quantity(self, quantity: str) -> EggQuantity:
        """
        Parses string 'quantity' into egg quantity with count, caliber and weight.
        """
        if not quantity:
            return self.quantity

        # Case 1: Only numeric (≤30 eggs)

        if re.fullmatch(self.pattern_repository.REGEX_NUMBERS_ONLY, quantity):
            num = float(quantity)
            if num <= 30:
                self.quantity.is_complete = True
                self.quantity.count = int(round(num))
                self.quantity.total_weight = num * EggCaliber.AVERAGE.weight
                return self.quantity

        # Case 2: Numeric + unit (Latin, Cyrillic, accented, etc.)
        if not self.quantity.is_complete:
            match = re.match(self.pattern_repository.REGEX_NUMERIC_UNIT, quantity)
            if match:
                number = float(match.group(1))
                unit = match.group(2).lower().split()
                # e.g. '1 dozen'
                if any([u.lower() in self.pattern_repository.DOZEN_EXPRESSIONS for u in unit]):
                    self.quantity.fill_from_count(int(number * 12))
                # e.g. '12 M'
                elif any([u.lower() in self.pattern_repository.MOYEN_EXPRESSIONS for u in unit]):
                    self.quantity.fill_from_count(count=int(number), caliber=EggCaliber.MEDIUM)
                # e.g. '12 large'
                elif any([u.lower() in self.pattern_repository.LARGE_EXPRESSIONS for u in unit]):
                    self.quantity.fill_from_count(count=int(number), caliber=EggCaliber.LARGE)
                else:
                    # e.g. '12 unities'
                    self.quantity.fill_from_count(count=int(number))

        # Case 3: x10 / X10 style
        if not self.quantity.is_complete:
            match = re.match(self.pattern_repository.REGEX_X_NUM, quantity)
            if match:
                egg_number = float(match.group(1))
                self.quantity.fill_from_count(count=int(egg_number))

        # Case 4: Addition expressions: "10 + 2", "12 + 3 oeufs"
        if not self.quantity.is_complete:
            match = re.search(self.pattern_repository.REGEX_ADDITION, quantity)
            if match:
                egg_number = int(match.group(1)) + int(match.group(2))
                self.quantity.fill_from_count(count=int(egg_number))

        # Case 5: Single number (e.g. "Boîte de 6")
        if not self.quantity.is_complete:
            match = re.search(self.pattern_repository.REGEX_EXTRACT_DIGITS, quantity)
            if match:
                num = int(match.group(1))
                if num < 1000:
                    self.quantity.fill_from_count(count=int(num))

        if not self.quantity.is_complete:
            print(f"Could not parse quantity: {quantity}")
            return self.quantity

        return self.quantity

    def get_egg_quantity_from_product_quantity_and_unit(self, quantity: float, unit: str) -> EggQuantity:
        """
        Converts product quantity and unit (grams or units) into Egg Quantity : weight, count, and caliber.
        """
        unit_key = unit.lower()
        if unit in self.pattern_repository.COUNT_UNITS:
            self.quantity.fill_from_count(count=int(round(quantity)))
        else:
            converter = self.pattern_repository.UNIT_CONVERSIONS.get(unit_key)
            if converter:
                try:
                    weight = converter(quantity)
                    self.quantity.fill_from_weight(weight)
                except (ValueError, TypeError):
                    pass
        return self.quantity

    def calculate_egg_quantity(self, product_data: ProductData) -> EggQuantity:
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
            self.get_egg_quantity_from_product_quantity_and_unit(product_quantity, unit)
        elif quantity:
            self.get_egg_quantity_from_product_quantity(quantity)
        else:
            self.get_egg_quantity_from_tags(categories_tags)

        return self.quantity


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

    def get_quantity(self, AnimalType: AnimalType) -> ProductQuantity:
        """
        Computes the quantity of the product for a specific animal type.
        Uses the EggQuantityCalculator for LAYING_HEN and use output weight for now

        Args:
            AnimalType (AnimalType): The animal type to calculate quantity for.
        Returns:
            ProductQuantity : for now float or None, in grams.
        """
        if AnimalType == AnimalType.LAYING_HEN:
            return EggQuantityCalculator().calculate_egg_quantity(self.product_data).total_weight
        else:
            return None
