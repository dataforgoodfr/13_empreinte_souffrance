import re
import unicodedata
from typing import Dict

from app.enums.open_food_facts.breeding_type_enums import (
    COUNTRIES_WHERE_CAGES_ARE_FURNISHED,
    get_barn_regex,
    get_cage_regex,
    get_free_range_regex,
)
from app.enums.open_food_facts.enums import AnimalType, BroilerChickenBreedingType, LayingHenBreedingType
from app.schemas.open_food_facts.external import ProductData
from app.schemas.open_food_facts.internal import BreedingTypeAndWeight

# Types
PatternType = set[str]
PatternMap = Dict[LayingHenBreedingType | BroilerChickenBreedingType, PatternType]
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

    def __init__(self, product_data: ProductData):
        """
        Initializes the calculator with the given product data.
        Args :  product_data (ProductData)
        """
        self.product_data = product_data
        self.patterns_repository = BreedingPatternsRepository()

    def get_breeding_types_by_animal(self) -> dict[AnimalType, BreedingTypeAndWeight]:
        """
        Get the breeding types for all animal types based on the product data.
        This method processes the product data for each animal type, determines if there is a
        unique match for the breeding type, and returns the result.
        Returns:
            dict[AnimalType, BreedingTypeAndWeight]: A dictionary mapping each animal type to its respective
            breeding type and weight = 0.
        """
        breeding_types_by_animal = {}

        for animal_type in self.patterns_repository.get_all_patterns():
            # Temporary fix to compute pain only for single-ingredient products
            # Skip if the animal type category is not in the product categories_tags
            if (
                not self.product_data.categories_tags
                or animal_type.categories_tags not in self.product_data.categories_tags
            ):
                break
            matched_breeding_types = self._get_breeding_types(animal_type)

            if len(matched_breeding_types) == 1:
                breeding_types_by_animal[animal_type] = BreedingTypeAndWeight(breeding_type=matched_breeding_types[0])

        return breeding_types_by_animal

    def _get_breeding_types(self, animal_type: AnimalType) -> list[LayingHenBreedingType | BroilerChickenBreedingType]:
        """
        Determines the breeding types for a specific animal based on an identification process.
        1st match exact categories_tag - stops if = 1 found  (> 1 => continue process)
        2nd match regex on names - stops if >= 1 found (> 1 =>  stop process - not found)
        3rd match regex on other tags including categories_tags  (> 1 => stop process - not found)
        Args:  animal_type (AnimalType): The type of animal to determine the breeding type for.
        Returns:  list[LayingHenBreedingType | BroilerChickenBreedingType]: A list of matched breeding types.
        """
        matched = self._match_from_exact_tags(tag="categories_tags", animal_type=animal_type)
        if len(matched) == 1:
            breeding_type = matched[0]
            breeding_type = self._refine_from_country(breeding_type)
            return [breeding_type]

        # Continue if no match or many matches on exact categories_tags
        for step in ["name", "tags"]:
            matched = self._match_from_regex(explored_tags=self._get_tags_to_explore(step), animal_type=animal_type)
            if matched:
                breeding_types = [self._refine_from_country(bt) for bt in matched]
                return breeding_types
        return []

    def _match_from_exact_tags(
        self, tag: str, animal_type: AnimalType
    ) -> list[LayingHenBreedingType | BroilerChickenBreedingType]:
        """
        Matches breeding types based on one exact tag from product data (only categories_tags possible here).
        Args:
            tag (str): The type of tag to use for matching (e.g., categories_tags).
            animal_type (AnimalType): The animal type to match against.
        Returns:
            list[LayingHenBreedingType | BroilerChickenBreedingType]: A list of matched breeding types.
        """
        explored_tags = getattr(self.product_data, tag, None)
        return [
            breeding_type
            for breeding_type, tags in self.patterns_repository.get_patterns(animal_type)[("exact", tag)].items()
            if explored_tags and any(t in explored_tags for t in tags)
        ]

    def _match_from_regex(
        self, explored_tags: list[str] | None, animal_type: AnimalType
    ) -> list[LayingHenBreedingType | BroilerChickenBreedingType]:
        """
        Matches breeding types using regex patterns applied to given tags
        Args:
            explored_tags (list[str]): The tags to explore using regex.
            animal_type (AnimalType): The animal type for which to perform regex matching.
        Returns:    list[LayingHenBreedingType | BroilerChickenBreedingType]: A list of matched breeding types.
        """
        matched: list[LayingHenBreedingType | BroilerChickenBreedingType] = []
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

    def _refine_from_country(
        self, breeding_type: LayingHenBreedingType | BroilerChickenBreedingType
    ) -> LayingHenBreedingType | BroilerChickenBreedingType:
        """
        Refines the breeding type based on country-specific regulations.
        Args:      breeding_type (LayingHenBreedingType | BroilerChickenBreedingType):
        Returns:   LayingHenBreedingType | BroilerChickenBreedingType:
        """
        if breeding_type == LayingHenBreedingType.CAGE:
            if self.product_data.countries_tags and any(
                country in COUNTRIES_WHERE_CAGES_ARE_FURNISHED for country in self.product_data.countries_tags
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
