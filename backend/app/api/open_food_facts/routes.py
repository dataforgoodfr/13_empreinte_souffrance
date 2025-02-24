from fastapi import APIRouter, HTTPException
from starlette.requests import Request

from app.api.open_food_facts.schemas import KnowledgePanelResponse
from app.business.open_food_facts.knowledge_panel import (
    ProductNotFoundException,
    get_properties_from_folksonomy,
)
from app.config.logging import setup_logging

router = APIRouter()
logger = setup_logging()


@router.get("/knowledge-panel/{product_id}", response_model=KnowledgePanelResponse)
async def knowledge_panel(
        request: Request,
        product_id: str,
):
    """
    API endpoint to return knowledge panel details.
    """
    logger.info("Getting knowledge panel for product %s", product_id)

    _ = request.state.translator

    # TODO: fix this. Fake translation with utf8 encoding to force utf8 encoding in the generated translations files
    _("ignøre this but keep it in the file")

    try:
        folksonomy_properties = get_properties_from_folksonomy(product_id)
    except ProductNotFoundException as e:
        raise HTTPException(status_code=404, detail=_("Product not found")) from e

    return KnowledgePanelResponse(
        title=_("Suffering Footprint"),
        description=_("The suffering footprint for this product is %s.") % folksonomy_properties["score"],
        logo_url="https://fakeimg.pl/350x100/?text=Empreinte%20Souffrance",
    )
