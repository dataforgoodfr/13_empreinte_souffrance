import pytest

from app.business.open_food_facts.calculators.pain_report_calculator import PainReportCalculator
from app.config.exceptions import MissingBreedingType
from app.enums.open_food_facts.enums import AnimalType, EggQuantity, LayingHenBreedingType, PainIntensity, PainType
from app.schemas.open_food_facts.external import ProductData
from app.schemas.open_food_facts.internal import BreedingTypeAndQuantity


@pytest.mark.parametrize(
    "countries, expected_breeding_types",
    [
        (["en:france"], LayingHenBreedingType.FURNISHED_CAGE),
        (["en:united-states"], LayingHenBreedingType.CONVENTIONAL_CAGE),
    ],
)
def test_get_breeding_types_and_quantities(
    sample_product_data: ProductData,
    countries,
    expected_breeding_types,
):
    """Test computing breeding types with quantities"""
    sample_product_data.countries_tags = countries
    calculator = PainReportCalculator(sample_product_data)

    result = calculator._get_breeding_types_and_quantities()

    # product_data fixture contains the `en:cage-chicken-eggs` tag
    assert AnimalType.LAYING_HEN in result
    item = result[AnimalType.LAYING_HEN]
    assert isinstance(item[0], BreedingTypeAndQuantity)
    assert item[0].breeding_type == expected_breeding_types
    assert item[0].quantity == EggQuantity(count=4, total_weight=230)


def test_get_breeding_types(sample_product_data: ProductData):
    """Test getting breeding types from product data"""
    calculator = PainReportCalculator(sample_product_data)
    result = calculator._get_breeding_types()
    assert AnimalType.LAYING_HEN in result
    assert result[AnimalType.LAYING_HEN] == [LayingHenBreedingType.FURNISHED_CAGE]


def test_generate_pain_levels_for_type(sample_product_data: ProductData):
    """Test generating pain levels for a specific animal, breeding type, and pain type"""

    calculator = PainReportCalculator(sample_product_data)

    quantity = EggQuantity(count=4, total_weight=230)

    breeding_type = BreedingTypeAndQuantity(breeding_type=LayingHenBreedingType.FURNISHED_CAGE, quantity=quantity)

    # Test generating physical pain levels
    physical_pain_levels = calculator._generate_pain_levels_for_pain_type(
        AnimalType.LAYING_HEN, breeding_type, PainType.PHYSICAL
    )

    assert len(physical_pain_levels) == 4  # One for each intensity
    for level in physical_pain_levels:
        assert level.pain_type == PainType.PHYSICAL
        assert isinstance(level.pain_intensity, PainIntensity)
        assert isinstance(level.seconds_in_pain, int)

    # Test generating psychological pain levels
    psychological_pain_levels = calculator._generate_pain_levels_for_pain_type(
        AnimalType.LAYING_HEN, breeding_type, PainType.PSYCHOLOGICAL
    )

    assert len(psychological_pain_levels) == 4  # One for each intensity
    for level in psychological_pain_levels:
        assert level.pain_type == PainType.PSYCHOLOGICAL
        assert isinstance(level.pain_intensity, PainIntensity)
        assert isinstance(level.seconds_in_pain, int)


def test_generate_pain_levels_for_type_missing_quantity(
    sample_product_data: ProductData, missing_breeding_type: BreedingTypeAndQuantity
):
    """Test generating pain levels for a specific animal with breeding type and missing quantity"""

    sample_product_data.product_quantity = None

    calculator = PainReportCalculator(sample_product_data)

    # Verify that the absence of quantity triggers an exception
    with pytest.raises(MissingBreedingType):
        calculator._generate_pain_levels_for_pain_type(AnimalType.LAYING_HEN, missing_breeding_type, PainType.PHYSICAL)


def test_get_pain_reports(sample_product_data: ProductData):
    """Test generating a pain report for sample product data"""

    calculator = PainReportCalculator(sample_product_data)
    pain_report = calculator.get_pain_reports()
    assert len(pain_report.scenarios) > 0
    scenario = pain_report.scenarios[0]

    # Verify that the scenario contains the expected animal type
    assert len(scenario.animal_pain_reports) > 0
    assert (scenario.animal_pain_reports[0]).animal_type == AnimalType.LAYING_HEN

    # Verify that pain levels are generated
    assert len((scenario.animal_pain_reports[0]).pain_levels) > 0


def test_get_pain_report_missing_quantity(sample_product_data: ProductData):
    """Test generating pain report with missing quantity"""

    sample_product_data.product_quantity = None

    calculator = PainReportCalculator(sample_product_data)
    pain_report = calculator.get_pain_reports()
    assert len(pain_report.scenarios) > 0
    scenario = pain_report.scenarios[0]

    # Verify that the scenario contains the expected animal type
    assert len(scenario.animal_pain_reports) > 0
    assert scenario.animal_pain_reports[0].animal_type == AnimalType.LAYING_HEN

    # Verify that pain levels are still given (for one egg)
    assert len(scenario.animal_pain_reports[0].pain_levels) == 8
