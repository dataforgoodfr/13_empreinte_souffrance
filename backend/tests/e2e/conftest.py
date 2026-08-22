import pytest


@pytest.fixture
def off_v3_caged_eggs_payload() -> dict:
    """
    A representative payload as actually returned by the OFF v3 API: raw JSON, as it comes
    over the wire, not the already-parsed internal ProductData model used by the other
    test suites. Used to exercise the real JSON -> Pydantic parsing path end-to-end.
    """
    return {
        "status": 1,
        "product": {
            "code": "3256540011346",
            "product_name": "Oeufs de poules elevees en cage",
            "product_name_fr": "Oeufs de poules elevees en cage",
            "product_name_en": "Caged hen eggs",
            "categories_tags": ["en:eggs", "en:chicken-eggs", "en:cage-chicken-eggs"],
            "labels_tags": [],
            "image_url": "https://images.openfoodfacts.org/images/products/325/654/001/1346/front.jpg",
            "quantity": "6 oeufs",
            "product_quantity": 360,
            "product_quantity_unit": "g",
            "allergens_tags": ["en:eggs"],
            "ingredients_tags": [],
            "ingredients": [],
            "countries": "France",
            "countries_tags": ["en:france"],
        },
    }


@pytest.fixture
def off_v3_not_found_payload() -> dict:
    """The payload OFF v3 returns (with a 200 status) for a barcode it doesn't know."""
    return {"status": 0, "status_verbose": "product not found", "code": "0000000000000"}
