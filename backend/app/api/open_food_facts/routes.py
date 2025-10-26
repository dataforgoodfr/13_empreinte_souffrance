from fastapi import APIRouter
from starlette.requests import Request

from app.business.open_food_facts.knowledge_panel import get_knowledge_panel_response, get_pain_report
from app.config.cache import knowledge_panel_cache
from app.config.exceptions import ExternalServiceException, ResourceNotFoundException
from app.config.logging import setup_logging
from app.schemas.open_food_facts.internal import KnowledgePanelResponse

router = APIRouter()
logger = setup_logging()


@router.get("/knowledge-panel/{barcode}", response_model=KnowledgePanelResponse, response_model_exclude_none=True)
async def knowledge_panel(request: Request, barcode: str):
    """
    API endpoint to return knowledge panel details.

    Args:
        request (Request): The request object.
        barcode (str): The product barcode number.

    Returns:
        KnowledgePanelResponse: The knowledge panel response.
    """
    locale = request.state.locale
    cache_key = f"knowledge_panel:{barcode}:{locale}"

    # Try to get from cache first
    cached_response = None
    if cached_response is not None:
        logger.info(f"Returning cached knowledge panel for product {barcode} (locale: {locale})")
        return cached_response

    logger.info(f"Getting knowledge panel for product {barcode} (locale: {locale})")

    try:
        pain_report = await get_pain_report(barcode=barcode, locale=locale)
    except (ResourceNotFoundException, ExternalServiceException):
        # Will be handled by the middleware, no need for additional processing here
        raise

    response = get_knowledge_panel_response(pain_report=pain_report, translator=request.state.translator)

    # Cache the response for 1 day (86400 seconds)
    knowledge_panel_cache.set(cache_key, response, ttl_seconds=86400)

    return response
