from typing import List

from pydantic import BaseModel, HttpUrl


class ProductData(BaseModel):
    """
    Product data model for search-a-licious request.
    """

    categories_tags: List[str] | None = None
    labels_tags: List[str] | None = None
    image_url: HttpUrl | None = None
    product_name: str
    product_quantity_unit: str | None = None
    product_quantity: float | None = None
    allergens_tags: List[str] | None = None
    ingredients_tags: List[str] | None = None
    ingredients: List[dict] | None = None
    countries: str | None = None
    countries_tags: List[str] | None = None


class ProductResponse(BaseModel):
    """
    Response model for search-a-licious request.
    """

    product: ProductData


# BaseModel when using v1 API
class ProductResponseV1(BaseModel):
    """
    Response model for search-a-licious request.
    """

    hits: List[ProductData]
