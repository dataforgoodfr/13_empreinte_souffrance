import re
import unicodedata

from app.enums.open_food_facts.enums import EggCaliber


class EggQuantityPatternRepository:
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
        s = EggQuantityPatternRepository._normalize_common(s)
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
        s = EggQuantityPatternRepository._normalize_common(s)
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
        s = EggQuantityPatternRepository._normalize_common(s)
        s = s.lower()
        return s
