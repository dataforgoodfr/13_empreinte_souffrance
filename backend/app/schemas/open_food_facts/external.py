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


class ProductResponse(BaseModel):
    """
    Response model for search-a-licious request.
    """

    hits: List[ProductData]
