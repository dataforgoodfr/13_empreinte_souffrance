from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_off_knowledge_panel(async_client: AsyncClient):
    """Test our knowledge panel endpoint"""
    mock_response_data = {
        "hits": [{"categories_tags": ["en:cage-chicken-eggs", "other"], "labels_tags": ["organic"]}]
    }

    mock_response = AsyncMock()
    mock_response.json = MagicMock(return_value=mock_response_data)
    mock_response.raise_for_status = AsyncMock(return_value=None)

    with patch("app.business.open_food_facts.knowledge_panel.randint", return_value=200):
        with patch("app.business.open_food_facts.knowledge_panel.httpx.AsyncClient") as mock_http_client:
            # Get the instance returned by the async context
            instance = mock_http_client.return_value.__aenter__.return_value
            instance.get.return_value = mock_response
            response = await async_client.get("/off/v1/knowledge-panel/1")

    assert response.status_code == 200
    assert response.json() == {
    "pain_report": {
        "pain_categories": [
            {
                "animals": [{"animal_type": "laying_hen", "seconds_in_pain": 200}],
                "pain_type": "excruciating",
            },
            {
                "animals": [{"animal_type": "laying_hen", "seconds_in_pain": 4000}],
                "pain_type": "disabling",
            },
            {
                "animals": [{"animal_type": "laying_hen", "seconds_in_pain": 6000}],
                "pain_type": "hurtful",
            },
            {
                "animals": [{"animal_type": "laying_hen", "seconds_in_pain": 8000}],
                "pain_type": "annoying",
            },
        ],
        "breeding_types_with_weights": [
            {
                "animal_type": "laying_hen",
                "breeding_type": "furnished_cage",
                "animal_product_weight": 200,
            }
        ]
    },
}
