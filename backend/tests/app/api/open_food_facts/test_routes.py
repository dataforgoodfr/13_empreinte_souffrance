from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest
from httpx import AsyncClient

from app.schemas.open_food_facts.external import ProductData


@pytest.mark.asyncio
async def test_get_off_knowledge_panel(async_client: AsyncClient, sample_product_data: ProductData):
    """Test our knowledge panel endpoint"""
    mock_response_data = {"product": sample_product_data}

    mock_response = AsyncMock()
    mock_response.json = MagicMock(return_value=mock_response_data)
    mock_response.raise_for_status = Mock(return_value=None)

    with patch("app.business.open_food_facts.knowledge_panel.httpx.AsyncClient") as mock_http_client:
        # Get the instance returned by the async context
        instance = mock_http_client.return_value.__aenter__.return_value
        instance.get.return_value = mock_response
        response = await async_client.get("/off/v1/knowledge-panel/1")

    assert response.status_code == 200
    # Test response has the expected structure
    response_data = response.json()
    assert "panels" in response_data
    assert "main" in response_data["panels"]
    assert "physical_pain" in response_data["panels"]
    assert "psychological_pain" in response_data["panels"]
    assert "intensities_definitions" in response_data["panels"]

    # Check panels structure
    for panel in response_data["panels"].values():
        assert "elements" in panel
        assert "title_element" in panel

        # Check title element structure
        title_element = panel["title_element"]
        assert "title" in title_element
