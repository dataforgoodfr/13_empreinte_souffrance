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
    quantity: str | None = None
    product_quantity_unit: str | None = None
    product_quantity: float | None = None
    allergens_tags: List[str] | None = None
    ingredients_tags: List[str] | None = None
    ingredients: List[dict] | None = None
    countries: str | None = None
    countries_tags: List[str] | None = None


class ProductResponse(BaseModel):
    """
    Response model for OFF V3 API request.
    """

    product: ProductData


# BaseModel when using v1 API
class ProductResponseSearchALicious(BaseModel):
    """
    Response model for OFF search-a-licious API request.
    """

    hits: List[ProductData]
