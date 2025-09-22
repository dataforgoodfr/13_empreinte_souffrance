import re

from app.config.exceptions import ResourceNotFoundException
from app.enums.open_food_facts.enums import AnimalType
from app.enums.open_food_facts.product_type_enums import ProductTypePatternRepository
from app.schemas.open_food_facts.external import ProductData
from app.schemas.open_food_facts.internal import ProductType


def get_product_type(product_data: ProductData) -> ProductType:
    """
    Determine the product type based on the product data.
    checks if the product is mixed or single animal type,
    and identifies the animal types present.
    Returns:
        ProductType instance indicating if the product is mixed and the set of animal types.
    """
    animal_types: set[AnimalType] = set()
    for animal_type in AnimalType:
        if (
            animal_type.is_computed
            and product_data.categories_tags
            and animal_type.categories_tags in product_data.categories_tags
        ):
            if animal_type == AnimalType.LAYING_HEN:
                if is_fresh_chicken_egg(product_data):
                    animal_types.add(animal_type)
            else:
                animal_types.add(animal_type)
    if not animal_types:
        raise ResourceNotFoundException("No animal types found in product data")
    elif len(animal_types) == 1:
        return ProductType(is_mixed=False, animal_types=animal_types)
    else:
        return ProductType(is_mixed=True, animal_types=animal_types)


def is_fresh_chicken_egg(product_data: ProductData) -> bool:
    """
    Determine if the product is a fresh chicken egg based on its categories tags.
    Checks :
        - if the product is a fresh chicken egg based on categories_tags -> True
        - if the product name contains chicken egg terms and fresh egg terms -> True
        - if the product name contains excluded category tags -> False
        - if the product name contains excluded patterns -> False
        - if none of the above conditions are met, it is considered a fresh chicken egg
    Args:
        product_data (ProductData): The product data containing categories_tags.
    Returns:
        bool: True if the product is a fresh chicken egg, False otherwise.
    """
    categories_tags = product_data.categories_tags or []

    if all(tag in ProductTypePatternRepository.FRESH_CHICKEN_EGG_TAGS for tag in categories_tags):
        return True

    names = {product_data.product_name, product_data.generic_name}
    names = {ProductTypePatternRepository.clean(name.lower()) for name in names if name}

    if (
        names
        and any(word in name for name in names if name for word in ProductTypePatternRepository.CHICKEN_EGG_TERMS)
        and any(word in name for name in names if name for word in ProductTypePatternRepository.FRESH_EGG_TERMS)
    ):
        return True

    if categories_tags and any(tag in ProductTypePatternRepository.EXCLUDED_CATEGORY_TAGS for tag in categories_tags):
        return False

    if names and any({re.search(ProductTypePatternRepository.EXCLUDED_PATTERNS, name) for name in names if name}):
        return False

    return True
