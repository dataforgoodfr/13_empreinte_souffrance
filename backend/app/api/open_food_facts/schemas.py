from pydantic import BaseModel


class KnowledgePanelResponse(BaseModel):
    """
    Response model for knowledge panel endpoint.
    Based on this structure: (TODO)
    https://fr.openfoodfacts.org/api/v2/product/3683080567969/?fields=knowledge_panels
    """
    title: str
    description: str
    logo_url: str | None = None
