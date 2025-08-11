from typing import AsyncGenerator, List

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from pydantic import HttpUrl
from starlette.testclient import TestClient

from app.enums.open_food_facts.enums import (
    AnimalType,
    BroilerChickenBreedingType,
    LayingHenBreedingType,
    PainIntensity,
    PainType,
)
from app.main import app
from app.schemas.open_food_facts.external import ProductData
from app.schemas.open_food_facts.internal import AnimalPainReport, BreedingTypeAndQuantity, PainLevelData, PainReport


@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture that provides an async HTTP client configured for testing.
    Use with async FastAPI routes.
    """
    async with AsyncClient(base_url="http://test", transport=ASGITransport(app=app)) as client:
        yield client


@pytest.fixture
def client() -> TestClient:
    """
    Fixture that provides a sync HTTP client for testing.
    """
    return TestClient(app)


@pytest.fixture
def sample_product_data() -> ProductData:
    """
    Fixture that provides sample product data for testing.
    Contains cage chicken eggs category...
    """
    return ProductData(
        categories_tags=["en:eggs", "en:chicken-eggs", "cat1", "en:cage-chicken-eggs"],
        labels_tags=["label1", "label2"],
        product_name="Fake product name",
        image_url=HttpUrl("https://example.com/image.jpg"),
        quantity=None,
        product_quantity=200,
        product_quantity_unit="g",
        allergens_tags=[],
        ingredients_tags=[],
        ingredients=[],
        countries="fr",
        countries_tags=["en:france"],
    )


@pytest.fixture
def weight_product_quantity_and_unit() -> ProductData:
    """
    Fixture that provides sample product data for testing.
    Contains data from product with code 9338295000049
    """
    return ProductData(
        categories_tags=["en:farming-productsen:eggsen:chicken-eggs", "en:free-range-chicken-eggs"],
        labels_tags=[],
        product_name="Eggs",
        image_url=HttpUrl("https://example.com/image.jpg"),
        quantity="800 g",
        product_quantity=800,
        product_quantity_unit="g",
        allergens_tags=[],
        ingredients_tags=[],
        ingredients=[],
        countries="au",
        countries_tags=["en:australia"],
    )


@pytest.fixture
def weight_quantity_only_digits() -> ProductData:
    """
    Fixture that provides sample product data for testing.
    Contains data from product with code 3770007836007
    """
    return ProductData(
        categories_tags=["en:farming-productsen:eggsen:chicken-eggs", "en:free-range-chicken-eggs"],
        labels_tags=[],
        product_name="6 oeufs frais plein air de poules Marans",
        image_url=HttpUrl("https://example.com/image.jpg"),
        quantity="6",
        product_quantity=None,
        product_quantity_unit=None,
        allergens_tags=[],
        ingredients_tags=[],
        ingredients=[],
        countries="fr",
        countries_tags=["en:france"],
    )


@pytest.fixture
def laying_hen_breeding_type() -> BreedingTypeAndQuantity:
    """
    Fixture that provides a sample BreedingTypeAndQuantity for laying hens.
    """
    return BreedingTypeAndQuantity(
        breeding_type=LayingHenBreedingType.FURNISHED_CAGE,
        quantity=200
    )

@pytest.fixture
def pain_levels() -> List[PainLevelData]:
    """
    Fixture that provides a list of PainLevelData objects for all pain types and intensities.
    """
    pain_levels = []

    # Add physical pain levels
    for intensity in PainIntensity:
        pain_levels.append(PainLevelData(pain_intensity=intensity, pain_type=PainType.PHYSICAL, seconds_in_pain=100))

    # Add psychological pain levels
    for intensity in PainIntensity:
        pain_levels.append(
            PainLevelData(pain_intensity=intensity, pain_type=PainType.PSYCHOLOGICAL, seconds_in_pain=200)
        )

    return pain_levels


@pytest.fixture
def animal_pain_report(laying_hen_breeding_type, pain_levels) -> AnimalPainReport:
    """
    Fixture that provides a sample AnimalPainReport for a laying hen.
    """
    return AnimalPainReport(
        animal_type=AnimalType.LAYING_HEN, pain_levels=pain_levels, breeding_type_and_quantity=laying_hen_breeding_type
    )


@pytest.fixture
def animal_pain_report_missing_quantity() -> AnimalPainReport:
    """
    Fixture that provides a sample AnimalPainReport for a laying hen with missing quantity.
    """
    return AnimalPainReport(
        animal_type=AnimalType.BROILER_CHICKEN,
        pain_levels=[],
        breeding_type_and_quantity=BreedingTypeAndQuantity(
            breeding_type=BroilerChickenBreedingType.FREE_RANGE,
            quantity=None,
        ),
    )


@pytest.fixture
def pain_report(animal_pain_report) -> PainReport:
    """
    Fixture that provides a sample PainReport that is returned for one animal
    with complete information.
    """
    return PainReport(
        animals=[animal_pain_report],
        product_name="Fake product name",
        product_image_url=HttpUrl("https://example.com/image.jpg"),
    )


@pytest.fixture
def pain_report_missing_quantity(animal_pain_report_missing_quantity) -> PainReport:
    """Fixture that provides a sample PainReport that is returned for one animal with missing quantity."""
    return PainReport(
        animals=[animal_pain_report_missing_quantity],
        product_name="Fake product name",
        product_image_url=HttpUrl("https://example.com/image.jpg"),
    )


@pytest.fixture
def pain_report_with_two_animals(animal_pain_report, animal_pain_report_missing_quantity) -> PainReport:
    """
    Fixture that provides a sample PainReport that is returned for one animal with complete information
    and one animal with missing quantity.
    """
    return PainReport(
        animals=[animal_pain_report, animal_pain_report_missing_quantity],
        product_name="Fake product name",
        product_image_url=HttpUrl("https://example.com/image.jpg"),
    )


# Weight testing fixtures
@pytest.fixture
def number_only_product():
    return ProductData(product_name="Fake product name", quantity="6")


@pytest.fixture
def numeric_unit_dozen():
    return ProductData(product_name="Fake product name", quantity="1 dozen")


@pytest.fixture
def numeric_unit_moyen():
    return ProductData(product_name="Fake product name", quantity="12 moyens")


@pytest.fixture
def numeric_unit_large():
    return ProductData(product_name="Fake product name", quantity="12 large")


@pytest.fixture
def x_style_product():
    return ProductData(product_name="Fake product name", quantity="x10")


@pytest.fixture
def addition_expression_product():
    return ProductData(product_name="Fake product name", quantity="10 + 2")


@pytest.fixture
def extract_digits_product():
    return ProductData(product_name="Fake product name", quantity="Boîte de 6")


@pytest.fixture
def tagged_large_egg_product():
    return ProductData(product_name="Fake product name", categories_tags=["en:large-eggs", "pack-of-6"])


@pytest.fixture
def product_quantity_with_unit():
    return ProductData(product_name="Fake product name", product_quantity=0.5, product_quantity_unit="lbs")


@pytest.fixture
def unknown_quantity_product():
    return ProductData(product_name="Fake product name", quantity="some weird string")


@pytest.fixture
def no_data_product():
    return ProductData(
        product_name="Fake product name",
    )
