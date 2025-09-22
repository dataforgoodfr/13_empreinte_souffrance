import re
import unicodedata
from typing import Dict

from app.enums.open_food_facts.breeding_type_enums import (
    BreedingTypesPatternRepository,
    get_barn_regex,
    get_cage_regex,
    get_free_range_regex,
)
from app.enums.open_food_facts.enums import AnimalType, BreedingType, LayingHenBreedingType
from app.schemas.open_food_facts.external import ProductData
from app.schemas.open_food_facts.internal import ProductType

# Types
PatternType = set[str]
PatternMap = Dict[BreedingType, PatternType]
AnimalPatternMap = Dict[tuple[str, str], PatternMap]


class BreedingPatternsRepository:
    """
    This class stores the patterns for exact category tag matches and regex patterns
    to help classify the breeding type of products based on animal types.
    """

    def __init__(self) -> None:
        """
        Initializes the repository by loading the breeding patterns from a predefined source.
        """
        self._patterns: dict[AnimalType, AnimalPatternMap] = self._load_patterns()

    def get_patterns(self, animal_type: AnimalType) -> AnimalPatternMap:
        """
        Retrieve the patterns for a specific animal type.
        Args:
            animal_type (AnimalType)
        Returns:
            AnimalPatternMap: A dictionary containing both exact category tags and regex patterns
            for the given animal type.
        """
        if animal_type not in self._patterns.keys():
            return {("exact", "categories_tags"): {}, ("regex", "all"): {}}
        return self._patterns.get(animal_type, {})

    def get_all_patterns(self) -> dict[AnimalType, AnimalPatternMap]:
        return self._patterns.copy()

    @staticmethod
    def _load_patterns() -> dict[AnimalType, AnimalPatternMap]:
        """
        Loads the breeding patterns from a predefined set of data.
        Returns:
            dict[AnimalType, AnimalPatternMap]: A dictionary mapping animal types to breeding patterns.
        """
        return {
            AnimalType.LAYING_HEN: {
                ("exact", "categories_tags"): {
                    LayingHenBreedingType.FREE_RANGE: {"en:free-range-chicken-eggs", "en:organic-eggs"},
                    LayingHenBreedingType.BARN: {"en:barn-chicken-eggs"},
                    LayingHenBreedingType.CAGE: {"en:cage-chicken-eggs"},
                },
                ("regex", "all"): {
                    LayingHenBreedingType.FREE_RANGE: {get_free_range_regex()},
                    LayingHenBreedingType.BARN: {get_barn_regex()},
                    LayingHenBreedingType.CAGE: {get_cage_regex()},
                },
            },
        }


class BreedingTypeCalculator:
    """
    A calculator that determines the breeding type of a product based on its data.

    This class analyzes a product data to determine the correct breeding type of
    all animals types registered in BreedingPatternsRepository
    """

    def __init__(self, product_data: ProductData, product_type: ProductType):
        """
        Initializes the calculator with the given product data
        and product type computed by the pain report calculator
        Args :  product_data (ProductData), product_type (ProductType)
        """
        self.product_data = product_data
        self.patterns_repository = BreedingPatternsRepository()
        self.product_type = product_type

    def get_breeding_types_by_animal(self) -> dict[AnimalType, BreedingType | None]:
        """
        Get the breeding types for all animal types known in product_type based on the product data.
        This method processes the product data for each animal type, determines if there is a
        unique match for the breeding type, and returns the result.
        Returns:
            dict[AnimalType, BreedingType | None]: A dictionary mapping each animal type to its respective
            breeding type
        """
        breeding_types_by_animal: dict[AnimalType, BreedingType | None] = {}

        # Method dedicated to mixed products so calculator cannot handle them for now
        for animal_type in self.product_type.animal_types:
            breeding_types_by_animal[animal_type] = None

        return breeding_types_by_animal

    def get_breeding_type(self, animal_type: AnimalType) -> BreedingType | None:
        """
        Determines the breeding types for a specific animal based on an identification process.
        1st match exact categories_tag - stops if = 1 found  (> 1 => continue process)
        2nd match regex on names - stops if >= 1 found (> 1 =>  stop process - not found)
        3rd match regex on other tags including categories_tags  (> 1 => stop process - not found)
        Args:  animal_type (AnimalType): The type of animal to determine the breeding type for.
        Returns:  BreedingType | None: The determined breeding type for the animal, or None if not found
        or too many matches
        """
        matched = self._match_from_exact_tags(tag="categories_tags", animal_type=animal_type)
        if len(matched) == 1:
            breeding_type = self._refine_from_country(matched[0])
            return breeding_type

        # Continue if no match or many matches on exact categories_tags
        # If nothing found or too many return None
        for step in ["name", "tags"]:
            matched = self._match_from_regex(explored_tags=self._get_tags_to_explore(step), animal_type=animal_type)
            if len(matched) == 1:
                breeding_type = self._refine_from_country(matched[0])
                return breeding_type
            elif len(matched) > 1:
                return None
        return None

    def _match_from_exact_tags(self, tag: str, animal_type: AnimalType) -> list[BreedingType]:
        """
        Matches breeding types based on one exact tag from product data (only categories_tags possible here).
        Args:
            tag (str): The type of tag to use for matching (e.g., categories_tags).
            animal_type (AnimalType): The animal type to match against.
        Returns:
            list[BreedingType]: A list of matched breeding types.
        """
        explored_tags = getattr(self.product_data, tag, None)
        return [
            breeding_type
            for breeding_type, tags in self.patterns_repository.get_patterns(animal_type)[("exact", tag)].items()
            if explored_tags and any(t in explored_tags for t in tags)
        ]

    def _match_from_regex(self, explored_tags: list[str] | None, animal_type: AnimalType) -> list[BreedingType]:
        """
        Matches breeding types using regex patterns applied to given tags
        Args:
            explored_tags (list[str]): The tags to explore using regex.
            animal_type (AnimalType): The animal type for which to perform regex matching.
        Returns:    list[LayingHenBreedingType | BroilerChickenBreedingType]: A list of matched breeding types.
        """
        matched: list[BreedingType] = []
        if not explored_tags:
            return matched
        for breeding_type, pattern_set in self.patterns_repository.get_patterns(animal_type)[("regex", "all")].items():
            pattern = next(iter(pattern_set))
            for tag in explored_tags:
                if re.search(pattern, self._clean(tag)):
                    matched.append(breeding_type)
                    break
        return matched

    def _get_tags_to_explore(self, step: str) -> list[str]:
        """
        Retrieves the tags to search based on the given research step (name or tags).
        Args:  step (str): The step indicating which set of tags to explore ("name" or "tags").
        Returns:  list[str]: A list of tags to explore.
        """
        if step == "name":
            return [tag for tag in [self.product_data.product_name, self.product_data.generic_name] if tag]
        elif step == "tags":
            tag_groups = [
                self.product_data.categories_tags or [],
                self.product_data.labels_tags or [],
                self.product_data.ingredients_tags or [],
            ]
            return [tag for group in tag_groups for tag in group if tag]
        else:
            raise ValueError("Invalid step. Use 'name' or 'tags'.")

    def _refine_from_country(self, breeding_type: BreedingType) -> BreedingType:
        """
        Refines the breeding type based on country-specific regulations.
        Args:      breeding_type (LayingHenBreedingType | BroilerChickenBreedingType):
        Returns:   LayingHenBreedingType | BroilerChickenBreedingType:
        """
        if breeding_type == LayingHenBreedingType.CAGE:
            if self.product_data.countries_tags and any(
                country in BreedingTypesPatternRepository.COUNTRIES_WHERE_CAGES_ARE_FURNISHED
                for country in self.product_data.countries_tags
            ):
                return LayingHenBreedingType.FURNISHED_CAGE
            else:
                return LayingHenBreedingType.CONVENTIONAL_CAGE
        return breeding_type

    @staticmethod
    def _clean(s: str | None) -> str:
        """
        Cleans a string by removing accents, replacing punctuation and digits,
        converting to lowercase, and replacing 'œ' with 'oe' before regex matching.
        Args:     s (str | None): The string to clean.

        Returns:  str: The cleaned string.
        """
        if not s:
            return ""
        s = s.lower().replace("œ", "oe")
        s = unicodedata.normalize("NFD", s)
        s = "".join(c for c in s if unicodedata.category(c) != "Mn")
        s = re.sub(r"[^\w\s]|\d+", " ", s)
        return s
