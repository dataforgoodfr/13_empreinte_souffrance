import pytest

from app.business.open_food_facts.calculators.product_type_calculator import get_product_type
from app.config.exceptions import EggButNotFreshEgg
from app.enums.open_food_facts.enums import AnimalType
from app.schemas.open_food_facts.external import ProductData
from app.schemas.open_food_facts.internal import ProductType


@pytest.mark.parametrize(
    "product_fixture",
    [
        ("fresh_chicken_eggs_product"),
        ("label_rouge_eggs"),
    ],
)
def test_get_product_type_fresh_chicken_egg(product_fixture: ProductData, request):
    """Test that a fresh chicken egg is correctly identified as a laying hen product"""
    product = request.getfixturevalue(product_fixture)
    product_type = get_product_type(product)
    assert product_type == ProductType(is_mixed=False, animal_types={AnimalType.LAYING_HEN})


def test_get_product_type_liquid_eggs(liquid_eggs_product: ProductData):
    """Test that a liquid egg raises ResourceNotFoundException since not handled by the calculator"""
    with pytest.raises(EggButNotFreshEgg):
        get_product_type(liquid_eggs_product)
