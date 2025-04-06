from pydantic import HttpUrl

from app.schemas.open_food_facts.external import ProductData

product_data = ProductData(
    categories_tags=["en:cage-chicken-eggs"],
    labels_tags=["organic"],
    product_name="Fake product name",
    image_url=HttpUrl("https://example.com/image.jpg"),
    product_quantity=200.0,
    product_quantity_unit="g",
    allergens_tags=[],
    ingredients_tags=[],
    ingredients=[],
    countries="fr",
    countries_tags=["en:france"],
)
