import pytest
from httpx import AsyncClient

from app.api.open_food_facts.schemas import PAIN_REPORT_EXAMPLE, KnowledgePanelResponse


@pytest.mark.asyncio
async def test_get_off_knowledge_panel(async_client: AsyncClient):
    response = await async_client.get("/off/v1/knowledge-panel/1")
    assert response.status_code == 200
    assert response.json() == KnowledgePanelResponse(
        logo_url="https://fakeimg.pl/350x100/?text=Empreinte%20Souffrance",
        global_score=8,
        pain_info=PAIN_REPORT_EXAMPLE,
    ).model_dump()
