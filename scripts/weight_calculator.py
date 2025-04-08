from typing import Dict, List, Optional, Union
import re
from enum import Enum
import json
import sys

class AnimalType(Enum):
    LAYING_HEN = "laying_hen"
    BROILER_CHICKEN = "broiler_chicken"
    COW = "cow"

class BreedingType(Enum):
    CAGE = "cage"
    BARN = "barn"
    FREE_RANGE = "free_range"
    ORGANIC = "organic"

# Type for representing BreedingTypeAndWeight without a class
BreedingTypeAndWeightDict = Dict[str, Union[str, float]]

# Type for representing ProductData without a class
ProductDataDict = Dict[str, Optional[Union[str, List[str], List[Dict[str, Optional[Union[str, float]]]]]]]

def extract_egg_percentage(ingredients: Optional[List[Dict[str, Optional[Union[str, float]]]]]) -> Optional[float]:
    """
    Extracts the percentage of eggs from the ingredients (dictionaries) with the updated structure.
    """
    if ingredients:
        for ingredient in ingredients:
            name_lower = ingredient.get("text", "").lower() if ingredient.get("text") else ""
            percent_estimate = ingredient.get("percent_estimate")
            percent_max = ingredient.get("percent_max")
            percent_min = ingredient.get("percent_min")

            if "oeuf" in name_lower or "egg" in name_lower:
                if isinstance(percent_estimate, (int, float)):
                    return float(percent_estimate)
                elif isinstance(percent_max, (int, float)) and isinstance(percent_min, (int, float)):
                    # If a range is available, return the average (or another desired logic)
                    return (float(percent_max) + float(percent_min)) / 2
    return None

def get_standard_egg_weight_from_category(categories_tags: List[str]) -> float:
    """
    Retrieves the standard weight of an egg based on the category (to be implemented).
    """
    num_eggs = get_number_of_eggs_from_pack_tag(categories_tags)
    for tag in categories_tags:
        if "large-eggs" in tag:
            return 60.0 * num_eggs
        elif "grade-a-eggs" in tag:
            return 55.0 * num_eggs # Example, weight may vary
        elif "medium-eggs" in tag:
            return 50.0 * num_eggs
        elif "gros-oeufs" in tag:
            return 60.0 * num_eggs
    return 0.0

def get_number_of_eggs_from_pack_tag(categories_tags: List[str]) -> int:
    """
    Extracts the number of eggs from the 'pack-of-' tag.
    """
    for tag in categories_tags:
        match = re.search(r"pack-of-(\d+)", tag)
        if match:
            return int(match.group(1))
    return 1 # If no 'pack-of-' tag, assume 1

def get_average_egg_weight() -> float:
    """
    Returns the estimated average weight of an egg in grams.
    """
    return 50.0 # Estimated average weight

def calculate_egg_weight(
    breeding_types_by_animal: Dict[AnimalType, BreedingTypeAndWeightDict],
    product_data: ProductDataDict
) -> Dict[AnimalType, BreedingTypeAndWeightDict]:
    """
    Calculates the weight of eggs for LAYING_HEN in the breeding_types dictionary
    based on the provided schema logic and product data, completely without classes.

    Args:
        breeding_types_by_animal: Dictionary mapping animal types to dictionaries
                                   representing breeding type and weight.
        product_data: Dictionary containing product information.

    Returns:
        A dictionary mapping animal types to dictionaries with updated
        animal_product_weight for LAYING_HEN, or the original dictionary if not applicable.
    """
    updated_breeding_types = breeding_types_by_animal.copy()

    if AnimalType.LAYING_HEN in updated_breeding_types:
        quantity = product_data.get("product_quantity")
        unit = product_data.get("product_quantity_unit")
        categories_tags = product_data.get("categories_tags") or []
        ingredients = product_data.get("ingredients")

        egg_weight = 0.0

        if not quantity:
            # quantity == Ø
            has_size_in_category = any(
                "large-eggs" in tag or "grade-a-eggs" in tag or "medium-eggs" in tag or "gros-oeufs" in tag or "pack-of-" in tag
                for tag in categories_tags
            )
            if has_size_in_category:
                egg_weight = get_standard_egg_weight_from_category(categories_tags)
        else:
            # quantity is not Ø
            if unit and unit.lower() in ["pcs", "sans", "unite"]:
                try:
                    num_eggs = float(quantity)
                    egg_weight = num_eggs * get_average_egg_weight()
                except (ValueError, TypeError):
                    pass
            elif unit and unit.lower() in ["g", "gr", "gramm"]:
                try:
                    egg_weight = float(quantity)
                except (ValueError, TypeError):
                    pass
            elif unit and unit.lower() in ["oz"]:
                try:
                    egg_weight = float(quantity) * 28.35
                except (ValueError, TypeError):
                    pass
            elif unit and unit.lower() in ["lbs"]:
                try:
                    egg_weight = float(quantity) * 453.59
                except (ValueError, TypeError):
                    pass
            elif unit and unit.lower() in ["ml"]:
                try:
                    egg_weight = float(quantity) * 1.03
                except (ValueError, TypeError):
                    pass
            elif unit and unit.lower() in ["l", "litres"]:
                try:
                    egg_weight = float(quantity) * 1030
                except (ValueError, TypeError):
                    pass

            # Check for egg products (if unit is in grams, look at the ingredients)
            if unit and unit.lower() == "g" and ingredients:
                total_weight_g = 0.0
                try:
                    total_weight_g = float(quantity)
                    egg_percentage = extract_egg_percentage(ingredients)
                    if egg_percentage is not None:
                        egg_weight = (egg_percentage / 100.0) * total_weight_g
                except (ValueError, TypeError):
                    pass

        if egg_weight > 0:
            updated_breeding_types[AnimalType.LAYING_HEN]["animal_product_weight"] = egg_weight

    return updated_breeding_types

if __name__ == "__main__":
    # --- Input Data (Directly in the script) ---
    breeding_types_data = {
        AnimalType.LAYING_HEN: {"breeding_type": BreedingType.FREE_RANGE.value, "animal_product_weight": 0.0}
    }

    product_data_list = [
        {
            "product_name": "Fresh Eggs",
            "product_quantity": "300",
            "product_quantity_unit": "g"
        },
        {
            "product_name": "Fresh Eggs",
            "product_quantity": "6",
            "product_quantity_unit": "pcs"
        },
        {
            "product_name": "Eggs",
            "categories_tags": ["en:eggs", "en:large-eggs", "pack-of-12"]
        },
        {
            "product_name": "Mayonnaise",
            "product_quantity": "250",
            "product_quantity_unit": "g",
            "ingredients": [
                {"id": "en:e385", "is_in_taxonomy": 1, "percent_estimate": 0.12, "percent_max": 1.18, "percent_min": 0, "text": "calcium disodium edta", "vegan": "yes", "vegetarian": "yes"},
                {"id": "en:flavouring", "is_in_taxonomy": 1, "percent_estimate": 0.06, "percent_max": 1.18, "percent_min": 0, "text": "flavourings", "vegan": "maybe", "vegetarian": "maybe"},
                {"id": "en:e160c", "is_in_taxonomy": 1, "percent_estimate": 0.03, "percent_max": 1.18, "percent_min": 0, "text": "paprika extract", "vegan": "yes", "vegetarian": "yes"},
                {"id": "en:ces-a-good-source-of-omega-3", "is_in_taxonomy": 0, "percent_estimate": 0.03, "percent_max": 1.18, "percent_min": 0, "text": "ces a good source of omega 3"},
                {"id": "en:egg", "is_in_taxonomy": 1, "percent_estimate": 20.0, "percent_max": None, "percent_min": None, "text": "egg", "vegan": "no", "vegetarian": "yes"}
            ]
        },
        {
            "product_name": "Pasta",
            "product_quantity": "500",
            "product_quantity_unit": "g",
            "ingredients": [
                {"id": "en:wheat-flour", "text": "durum wheat semolina", "percent_estimate": 100.0}
            ]
        }
    ]

    print("\n--- Running Egg Weight Calculator ---")

    for i, product_data in enumerate(product_data_list):
        print(f"\n--- Processing Product {i+1} ---")
        print(f"Input Breeding Types: {breeding_types_data}")
        print(f"Input Product Data: {product_data}")

        updated_breeding_types = calculate_egg_weight(breeding_types_data, product_data)

        print("\n--- Output Report ---")
        print("Updated Breeding Types with Egg Weight:")
        # Convert AnimalType keys to strings for JSON serialization
        serializable_breeding_types = {animal.value: data for animal, data in updated_breeding_types.items()}
        print(json.dumps(serializable_breeding_types, indent=4))
