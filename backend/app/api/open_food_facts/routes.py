from fastapi import APIRouter
from starlette.requests import Request

from app.business.open_food_facts.knowledge_panel import compute_suffering_footprint, get_knowledge_panel_response
from app.config.exceptions import ExternalServiceException, ResourceNotFoundException
from app.config.logging import setup_logging
from app.schemas.open_food_facts.internal import KnowledgePanelResponse

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
        pain_report = await compute_suffering_footprint(barcode=barcode)
    except (ResourceNotFoundException, ExternalServiceException):
        # Will be handled by the middleware, no need for additional processing here
        raise

    return get_knowledge_panel_response(pain_report=pain_report)
