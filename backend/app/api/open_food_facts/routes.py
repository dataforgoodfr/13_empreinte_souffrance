from fastapi import APIRouter, Query, Response
from starlette.requests import Request

from app.business.open_food_facts.knowledge_panel import get_knowledge_panel_response, get_pain_report, get_pain_reports
from app.config.cache import knowledge_panel_cache
from app.config.exceptions import ExternalServiceException, ResourceNotFoundException
from app.config.logging import setup_logging
from app.schemas.open_food_facts.internal import KnowledgePanelBatchResponse, KnowledgePanelResponse

router = APIRouter()
logger = setup_logging()


@router.api_route(
    "/knowledge-panel/{barcode}",
    methods=["GET", "HEAD"],
    response_model=KnowledgePanelResponse,
    response_model_exclude_none=True,
)
async def knowledge_panel(request: Request, barcode: str):
    """
    API endpoint to return knowledge panel details for a single product.
    Handles both GET and HEAD methods.

    Args:
        request (Request): The request object.
        barcode (str): The product barcode number.

    Returns:
        KnowledgePanelResponse: The knowledge panel response.
    """
    locale = request.state.locale
    cache_key = f"knowledge_panel:{barcode}:{locale}"

    # Try to get from cache first
    cached_response = knowledge_panel_cache.get(cache_key)
    if cached_response is not None:
        logger.info(f"Returning cached knowledge panel for product {barcode} (locale: {locale})")

        if request.method == "HEAD":
            return Response(status_code=200)

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

    if request.method == "HEAD":
        return Response(status_code=200)

    return response


@router.get(
    "/knowledge-panel/",
    response_model=KnowledgePanelBatchResponse,
    response_model_exclude_none=True,
)
async def knowledge_panels_batch(
    request: Request,
    code: str = Query(..., description="Comma-separated list of product barcodes"),
):
    """
    API endpoint to return knowledge panels for one or several products in a single call.
    Processes all barcodes in parallel. Failures on individual barcodes are reported
    in the 'errors' field without affecting the other results.

    Args:
        request: The request object.
        code: Comma-separated barcodes, e.g. "3017620422003" or "3017620422003,3228857000166"

    Returns:
        KnowledgePanelBatchResponse with 'panels' (successes) and 'errors' (failures)
    """
    locale = request.state.locale
    barcode_list = [b.strip() for b in code.split(",") if b.strip()]

    logger.info(f"Getting knowledge panels for {len(barcode_list)} products (locale: {locale})")

    panels: dict = {}
    errors: dict = {}
    barcodes_to_fetch = []

    for barcode in barcode_list:
        cache_key = f"knowledge_panel:{barcode}:{locale}"
        cached = knowledge_panel_cache.get(cache_key)
        if cached is not None:
            logger.info(f"Returning cached knowledge panel for product {barcode} (locale: {locale})")
            panels[barcode] = cached
        else:
            barcodes_to_fetch.append(barcode)

    if barcodes_to_fetch:
        pain_reports = await get_pain_reports(barcodes=barcodes_to_fetch, locale=locale)

        for barcode, result in pain_reports.items():
            if isinstance(result, BaseException):
                logger.warning(f"Failed to get pain report for product {barcode}: {result}")
                errors[barcode] = str(result)
            else:
                response = get_knowledge_panel_response(pain_report=result, translator=request.state.translator)
                cache_key = f"knowledge_panel:{barcode}:{locale}"
                knowledge_panel_cache.set(cache_key, response, ttl_seconds=86400)
                panels[barcode] = response

    return KnowledgePanelBatchResponse(panels=panels, errors=errors)
