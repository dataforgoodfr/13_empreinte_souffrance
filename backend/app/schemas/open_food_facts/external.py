from typing import List

from pydantic import BaseModel


class ProductData(BaseModel):
    """
    Product data model for search-a-licious request.
    """
    categories_tags: List[str] | None = None
    labels_tags: List[str] | None = None


class ProductResponse(BaseModel):
    """
    Response model for search-a-licious request.
    """
    hits: List[ProductData]
