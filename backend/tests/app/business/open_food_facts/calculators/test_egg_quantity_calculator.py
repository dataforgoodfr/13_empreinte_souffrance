import pytest

from app.business.open_food_facts.calculators.egg_quantity_calculator import EggCaliber, EggQuantityCalculator
from app.enums.open_food_facts.enums import EggQuantity


@pytest.mark.parametrize(
    "product_fixture, expected_quantity",
    [
        ("number_only_product", EggQuantity(count=6, total_weight=6 * EggCaliber.AVERAGE.weight)),
        (
            "numeric_unit_dozen_small",
            EggQuantity(count=12, total_weight=12 * EggCaliber.SMALL.weight, caliber=EggCaliber.SMALL),
        ),
        (
            "numeric_unit_moyen",
            EggQuantity(count=12, total_weight=12 * EggCaliber.MEDIUM.weight, caliber=EggCaliber.MEDIUM),
        ),
        (
            "numeric_unit_large",
            EggQuantity(count=12, total_weight=12 * EggCaliber.LARGE.weight, caliber=EggCaliber.LARGE),
        ),
        ("x_style_product", EggQuantity(count=10, total_weight=10 * EggCaliber.AVERAGE.weight)),
        ("addition_expression_product", EggQuantity(count=12, total_weight=12 * EggCaliber.AVERAGE.weight)),
        (
            "extract_digits_product_extra_large",
            EggQuantity(count=6, total_weight=6 * EggCaliber.EXTRA_LARGE.weight, caliber=EggCaliber.EXTRA_LARGE),
        ),
        (
            "tagged_large_egg_product",
            EggQuantity(count=6, total_weight=6 * EggCaliber.LARGE.weight, caliber=EggCaliber.LARGE),
        ),
        (
            "product_quantity_with_unit",
            EggQuantity(count=round(round(0.5 * 453.59) / EggCaliber.AVERAGE.weight), total_weight=round(0.5 * 453.59)),
        ),
        (
            "product_quantity_with_product_name_and_weight",
            EggQuantity(count=10, total_weight=10 * EggCaliber.AVERAGE.weight),
        ),
        ("unknown_quantity_product", None),
        ("no_data_product", None),
    ],
)
def test_calculate_egg_quantity(product_fixture, expected_quantity, request):
    product = request.getfixturevalue(product_fixture)
    assert EggQuantityCalculator().calculate_egg_quantity(product) == expected_quantity
