import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_off_knowledge_panel(async_client: AsyncClient):
    response = await async_client.get("/off/v1/knowledge-panel/1")
    assert response.status_code == 200
    assert response.json() == {
            "title": "Suffering Footprint",
            "description": "The suffering footprint for this product is 0.9.",
            "logo_url": "https://fakeimg.pl/350x100/?text=Empreinte%20Souffrance",
        }
