import io
import re
from typing import Callable
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import httpx
import pytest

from app.business.open_food_facts.breeding_type_calculator import (
    BreedingTypeCalculator,
    get_barn_regex,
    get_cage_regex,
    get_free_range_regex,
)
from app.business.open_food_facts.egg_quantity_calculator import (
    EggCaliber,
    EggQuantityCalculator,
)
from app.business.open_food_facts.knowledge_panel import (
    KnowledgePanelGenerator,
    get_data_from_off_search_a_licious,
    get_data_from_off_v3,
    get_knowledge_panel_response,
)
from app.business.open_food_facts.pain_report_calculator import (
    MissingBreedingTypeOrQuantityError,
    PainReportCalculator,
)
from app.business.open_food_facts.unit_pain_loader import UnitPainLoader
from app.config.exceptions import ResourceNotFoundException
from app.config.i18n import I18N
from app.enums.open_food_facts.enums import AnimalType, EggQuantity, LayingHenBreedingType, PainIntensity, PainType
from app.schemas.open_food_facts.external import ProductData
from app.schemas.open_food_facts.internal import (
    BreedingTypeAndQuantity,
    KnowledgePanelResponse,
    PainReport,
)


@pytest.mark.asyncio
async def test_get_data_from_off_search_a_licious_success():
    """Test when the OFF API returns valid data"""
    barcode = "123456789"
    mock_response_data = {
        "hits": [
            {
                "categories_tags": ["en:cage-chicken-eggs", "other"],
                "labels_tags": ["organic"],
                "product_name": "Fake product name",
                "image_url": "https://example.com/image.jpg",
            }
        ]
    }

    mock_response = AsyncMock()
    mock_response.json = MagicMock(return_value=mock_response_data)
    mock_response.raise_for_status = Mock(return_value=None)

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        result = await get_data_from_off_search_a_licious(barcode, locale="en")

    assert result == ProductData.model_validate(mock_response_data["hits"][0])


@pytest.mark.asyncio
async def test_get_data_from_off_v3_success(sample_product_data: ProductData):
    """Test when the OFF API returns valid data"""
    barcode = "123456789"
    mock_response_data = {"product": sample_product_data}

    mock_response = AsyncMock()
    mock_response.json = MagicMock(return_value=mock_response_data)
    mock_response.raise_for_status = Mock(return_value=None)

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        result = await get_data_from_off_v3(barcode, locale="en")

    assert result == sample_product_data


@pytest.mark.asyncio
async def test_get_data_from_off_search_a_licious_no_hits():
    """Test when the OFF API returns no hits"""
    barcode = "000000000"
    mock_response_data = {"hits": []}

    mock_response = AsyncMock()
    mock_response.json = MagicMock(return_value=mock_response_data)
    mock_response.raise_for_status = Mock(return_value=None)

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        with pytest.raises(ResourceNotFoundException, match=f"No hits returned by OFF API: {barcode}"):
            await get_data_from_off_search_a_licious(barcode, locale="en")


@pytest.mark.asyncio
@pytest.mark.parametrize("get_data_from_off_function", [get_data_from_off_search_a_licious, get_data_from_off_v3])
async def test_get_data_from_off_validation_error(get_data_from_off_function: Callable):
    """Test when the OFF API returns invalid data"""
    barcode = "999999999"
    mock_response_data = {"product": "invalid_value"}

    mock_response = AsyncMock()
    mock_response.json = MagicMock(return_value=mock_response_data)
    mock_response.raise_for_status = Mock(return_value=None)

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        with pytest.raises(
            ResourceNotFoundException, match=f"Failed to validate product data retrieved from OFF: {barcode}"
        ):
            await get_data_from_off_function(barcode, locale="en")


@pytest.mark.asyncio
@pytest.mark.parametrize("get_data_from_off_function", [get_data_from_off_search_a_licious, get_data_from_off_v3])
async def test_get_data_from_off_http_call_exception(get_data_from_off_function: Callable):
    """Test when the OFF API returns an HTTP error"""
    barcode = "111111111"

    with patch("httpx.AsyncClient.__aenter__", side_effect=httpx.ReadTimeout("Network error")):
        with pytest.raises(ResourceNotFoundException, match=f"Can't get product data from OFF API: {barcode}"):
            await get_data_from_off_function(barcode, locale="en")


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
    assert isinstance(item, BreedingTypeAndQuantity)
    assert item.breeding_type == expected_breeding_types
    assert item.quantity == EggQuantity(count=4, total_weight=230)


def test_get_breeding_types(sample_product_data: ProductData):
    """Test getting breeding types from product data"""
    calculator = PainReportCalculator(sample_product_data)
    result = calculator._get_breeding_types()
    assert AnimalType.LAYING_HEN in result
    assert result[AnimalType.LAYING_HEN] == LayingHenBreedingType.FURNISHED_CAGE


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


def test_generate_pain_levels_for_type_missing_quantity(sample_product_data: ProductData):
    """Test generating pain levels for a specific animal with breeding type and missing quantity"""

    sample_product_data.product_quantity = None

    calculator = PainReportCalculator(sample_product_data)

    breeding_type = BreedingTypeAndQuantity(breeding_type=LayingHenBreedingType.FURNISHED_CAGE, quantity=None)

    # Verify that the absence of quantity triggers an exception
    with pytest.raises(MissingBreedingTypeOrQuantityError):
        calculator._generate_pain_levels_for_pain_type(AnimalType.LAYING_HEN, breeding_type, PainType.PHYSICAL)


def test_get_pain_report(sample_product_data: ProductData):
    """Test generating pain report for sample product data"""

    calculator = PainReportCalculator(sample_product_data)
    pain_report = calculator.get_pain_report()

    # Verify that the pain report contains the expected animal type
    assert len(pain_report.animals) > 0
    assert (pain_report.animals[0]).animal_type == AnimalType.LAYING_HEN

    # Verify that pain levels are generated
    assert len((pain_report.animals[0]).pain_levels) > 0


def test_get_pain_report_missing_quantity(sample_product_data: ProductData):
    """Test generating pain report with missing quantity"""

    sample_product_data.product_quantity = None

    calculator = PainReportCalculator(sample_product_data)
    pain_report = calculator.get_pain_report()

    # Verify that the pain report contains the expected animal type
    assert len(pain_report.animals) > 0
    assert pain_report.animals[0].animal_type == AnimalType.LAYING_HEN

    # Verify that pain levels are empty when breeding type or quantity is missing
    assert len(pain_report.animals[0].pain_levels) == 0


# Test the display of knowledge panel with a product name or without it
@pytest.mark.parametrize(
    "product_name_for_test, expected_knowledge_panel_product_name",
    [
        ("Some product_name", "Some product_name"),
        (None, None),
    ],
)
# Test knowledge panel generation with a pain report with one animal and
# with a pain report with one animal with pain data and one animal without pain data
@pytest.mark.parametrize(
    "pain_report",
    ["pain_report", "pain_report_with_two_animals"],
    indirect=True,
)
def test_knowledge_panel_generator(
    pain_report: PainReport, product_name_for_test: str | None, expected_knowledge_panel_product_name: str | None
):
    """Test the KnowledgePanelGenerator with different pain_report fixtures and product names"""

    pain_report = pain_report.model_copy(update={"product_name": product_name_for_test})

    translator = I18N().get_translator(locale="en")

    # Create generator and test individual methods
    generator = KnowledgePanelGenerator(pain_report, translator)

    # Test main panel
    main_panel = generator._create_main_panel(["intensities_definitions", "physical_pain", "psychological_pain"])
    assert main_panel.level == "info"
    assert main_panel.title_element.title == "Welfare footprint"
    assert len(main_panel.elements) > 3
    assert not any(
        el.text_element is not None and "missing" in el.text_element.html.lower()
        for el in main_panel.elements
        if el.element_type == "text"
    )

    # Test intensities definitions panel
    intensities_panel = generator._create_intensities_definitions_panel()
    assert intensities_panel.title_element.title == "Intensity categories definitions"
    assert len(intensities_panel.elements) == 4  # One for each intensity

    # Test physical pain panel
    physical_panel = generator._create_physical_pain_panel()
    assert physical_panel.title_element.title == "Physical pain"
    assert len(physical_panel.elements) > 3  # Intro, description, animal pain data, and footer

    # Test psychological pain panel
    psychological_panel = generator._create_psychological_pain_panel()
    assert psychological_panel.title_element.title == "Psychological pain"
    assert len(psychological_panel.elements) > 3  # Intro, description, animal pain data, and footer

    # Test animal pain element generation
    animal_element = generator._get_animal_pain_for_panel(AnimalType.LAYING_HEN, PainType.PHYSICAL)
    assert animal_element is not None
    assert animal_element.text_element is not None
    assert animal_element.element_type == "text"
    assert "Laying hen" in animal_element.text_element.html

    # Test complete response
    response = generator.get_response()
    assert isinstance(response, KnowledgePanelResponse)
    assert len(response.panels) == 4

    # Verify that the product name in the response matches the expected value
    assert response.product.name == expected_knowledge_panel_product_name, (
        f"Product name in KnowledgePanelResponse should be \
            '{expected_knowledge_panel_product_name}' for input '{product_name_for_test}'"
    )


def test_knowledge_panel_generator_missing_quantity(pain_report_missing_quantity: PainReport):
    """Test the KnowledgePanelGenerator class with a pain report missing quantity"""
    translator = I18N().get_translator(locale="en")

    # Create generator and test individual methods
    generator = KnowledgePanelGenerator(pain_report_missing_quantity, translator)

    # Test main panel
    main_panel = generator._create_main_panel([])
    assert main_panel.level == "info"
    assert main_panel.title_element.title == "Welfare footprint"

    # Test main panel elements as intro, uniqueness and missing data
    assert len(main_panel.elements) > 3
    assert any(
        el.text_element is not None and "missing" in el.text_element.html.lower()
        for el in main_panel.elements
        if el.element_type == "text"
    )

    # Test complete response
    response = generator.get_response()
    assert list(response.panels.keys()) == ["main"]


@pytest.mark.parametrize(
    "pain_report",
    ["pain_report", "pain_report_with_two_animals"],
    indirect=True,
)
def test_get_knowledge_panel_response(pain_report):
    """Test the get_knowledge_panel_response function"""
    translator = I18N().get_translator(locale="en")

    # Generate knowledge panel response using the function
    response = get_knowledge_panel_response(pain_report, translator)

    # Verify response structure
    assert "main" in response.panels
    assert "physical_pain" in response.panels
    assert "psychological_pain" in response.panels
    assert "intensities_definitions" in response.panels

    # Verify each panel has the required fields
    for panel in response.panels.values():
        assert hasattr(panel, "elements")
        assert hasattr(panel, "title_element")


def test_get_knowledge_panel_response_missing_quantity(pain_report_missing_quantity: PainReport):
    """Test that only main panel is generated when quantity is missing"""
    translator = I18N().get_translator(locale="en")

    response = get_knowledge_panel_response(pain_report_missing_quantity, translator)

    # On attend uniquement "main" dans les panels
    assert list(response.panels.keys()) == ["main"]
    assert hasattr(response.panels["main"], "elements")
    assert hasattr(response.panels["main"], "title_element")


@pytest.mark.parametrize(
    "tag,should_match",
    [
        ("œufs-plein-air-non-bios", True),
        ("en:free-range-chicken-eggs", True),
        ("chicken-eggs-not-free-range", False),
        ("Ariaperta uova fresche da galline allevate all'aperto", True),
    ],
)
def test_free_range_regex(tag, should_match):
    pattern = get_free_range_regex()
    assert bool(re.search(pattern, BreedingTypeCalculator._clean(tag))) == should_match


@pytest.mark.parametrize(
    "tag,should_match",
    [
        ("œufs élevés AU SOL*", True),
        ("barn-chicken-eggs-not-organic", True),
        ("produit bio", False),
        ("oeufs solidaires", False),
    ],
)
def test_barn_regex(tag, should_match):
    pattern = get_barn_regex()
    assert bool(re.search(pattern, BreedingTypeCalculator._clean(tag))) == should_match


@pytest.mark.parametrize(
    "tag,should_match",
    [
        ("eggs-from-caged-hens", True),
        ("Produit hors Cage", False),
        ("abcagedd", False),
        ("cage-free-chicken-eggs", False),
        ("ces oeufs ne proviennent pas de poules éléveées en CAGE", False),
    ],
)
def test_cage_regex(tag, should_match):
    pattern = get_cage_regex()
    assert bool(re.search(pattern, BreedingTypeCalculator._clean(tag))) == should_match


# Test egg quantity calculator


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
        ("unknown_quantity_product", None),
        ("no_data_product", None),
    ],
)
def test_calculate_egg_quantity(product_fixture, expected_quantity, request):
    product = request.getfixturevalue(product_fixture)
    assert EggQuantityCalculator().calculate_egg_quantity(product) == expected_quantity


def test_load_minimal_csv():
    csv_content = """animal_type;breeding_type;pain_type;pain_intensity;caliber;pain_per_egg_in_seconds
laying_hen;barn;physical;hurtful;small;12.5
"""
    file_like = io.StringIO(csv_content)

    loader = UnitPainLoader(file_like)
    data = loader.load()

    assert isinstance(data, dict)
    assert AnimalType.LAYING_HEN in data
    assert LayingHenBreedingType.BARN in data[AnimalType.LAYING_HEN]
    assert PainType.PHYSICAL in data[AnimalType.LAYING_HEN][LayingHenBreedingType.BARN]
    assert PainIntensity.HURTFUL in data[AnimalType.LAYING_HEN][LayingHenBreedingType.BARN][PainType.PHYSICAL]
    assert (
        EggCaliber.SMALL
        in data[AnimalType.LAYING_HEN][LayingHenBreedingType.BARN][PainType.PHYSICAL][PainIntensity.HURTFUL]
    )
    assert (
        data[AnimalType.LAYING_HEN][LayingHenBreedingType.BARN][PainType.PHYSICAL][PainIntensity.HURTFUL][
            EggCaliber.SMALL
        ]
        == 12.5
    )
