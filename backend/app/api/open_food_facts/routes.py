from fastapi import APIRouter
from starlette.requests import Request

from app.api.open_food_facts.schemas import KnowledgePanelResponse
from app.business.open_food_facts.knowledge_panel import (
    get_properties_from_folksonomy,
)
from app.config.exceptions import ExternalServiceException, ResourceNotFoundException
from app.config.logging import setup_logging

router = APIRouter()
logger = setup_logging()


@router.get("/knowledge-panel/{barcode}", response_model=KnowledgePanelResponse)
async def knowledge_panel(request: Request, barcode: str):
    """
    API endpoint to return knowledge panel details.

    Args:
        request (Request): The request object.
        barcode (str): The product barcode number.

    Returns:
        KnowledgePanelResponse: The knowledge panel response.
    """
    logger.info(f"Getting knowledge panel for product {barcode}")

    try:
        pain_report = get_properties_from_folksonomy(barcode=barcode)
    except (ResourceNotFoundException, ExternalServiceException):
        # Will be handled by the middleware, no need for additional processing here
        raise

    return KnowledgePanelResponse(
        logo_url="https://fakeimg.pl/350x100/?text=Empreinte%20Souffrance",
        global_score=8,
        pain_info=pain_report,
    )
