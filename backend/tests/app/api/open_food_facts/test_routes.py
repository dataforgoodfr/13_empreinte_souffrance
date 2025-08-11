from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest
from httpx import AsyncClient

from app.config.cache import knowledge_panel_cache
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


@pytest.mark.asyncio
async def test_knowledge_panel_cache_miss_then_hit(async_client: AsyncClient, sample_product_data: ProductData):
    """Test that the cache works correctly: first request is a cache miss, second is a cache hit"""
    # Clear the cache before testing
    knowledge_panel_cache.clear()

    mock_response_data = {"product": sample_product_data}
    mock_response = AsyncMock()
    mock_response.json = MagicMock(return_value=mock_response_data)
    mock_response.raise_for_status = AsyncMock(return_value=None)

    with patch("app.business.open_food_facts.knowledge_panel.httpx.AsyncClient") as mock_http_client:
        # Get the instance returned by the async context
        instance = mock_http_client.return_value.__aenter__.return_value
        instance.get.return_value = mock_response

        # First request - should be a cache miss
        response1 = await async_client.get("/off/v1/knowledge-panel/123456789")
        assert response1.status_code == 200

        # Verify the external API was called (cache miss)
        assert instance.get.called
        call_count_after_first_request = instance.get.call_count

        # Second request with same barcode - should be a cache hit
        response2 = await async_client.get("/off/v1/knowledge-panel/123456789")
        assert response2.status_code == 200

        # Verify the external API was NOT called again (cache hit)
        assert instance.get.call_count == call_count_after_first_request

        # Verify responses are identical
        assert response1.json() == response2.json()


@pytest.mark.asyncio
async def test_knowledge_panel_cache_different_locales(async_client: AsyncClient, sample_product_data: ProductData):
    """Test that cache correctly separates responses by locale"""
    # Clear the cache before testing
    knowledge_panel_cache.clear()

    mock_response_data = {"product": sample_product_data}
    mock_response = AsyncMock()
    mock_response.json = MagicMock(return_value=mock_response_data)
    mock_response.raise_for_status = AsyncMock(return_value=None)

    with patch("app.business.open_food_facts.knowledge_panel.httpx.AsyncClient") as mock_http_client:
        instance = mock_http_client.return_value.__aenter__.return_value
        instance.get.return_value = mock_response

        # Request with English locale
        response_en = await async_client.get("/off/v1/knowledge-panel/123456789", headers={"Accept-Language": "en"})
        assert response_en.status_code == 200
        calls_after_en = instance.get.call_count

        # Request with French locale (same barcode) - should trigger new API call
        response_fr = await async_client.get("/off/v1/knowledge-panel/123456789", headers={"Accept-Language": "fr"})
        assert response_fr.status_code == 200
        calls_after_fr = instance.get.call_count

        # Verify both requests triggered API calls (different cache entries)
        assert calls_after_fr > calls_after_en

        # Third request with English locale - should be cache hit
        response_en_cached = await async_client.get(
            "/off/v1/knowledge-panel/123456789", headers={"Accept-Language": "en"}
        )
        assert response_en_cached.status_code == 200

        # Verify no additional API call was made (cache hit)
        assert instance.get.call_count == calls_after_fr


@pytest.mark.asyncio
async def test_knowledge_panel_cache_different_barcodes(async_client: AsyncClient, sample_product_data: ProductData):
    """Test that cache correctly separates responses by barcode"""
    # Clear the cache before testing
    knowledge_panel_cache.clear()

    mock_response_data = {"product": sample_product_data}
    mock_response = AsyncMock()
    mock_response.json = MagicMock(return_value=mock_response_data)
    mock_response.raise_for_status = AsyncMock(return_value=None)

    with patch("app.business.open_food_facts.knowledge_panel.httpx.AsyncClient") as mock_http_client:
        instance = mock_http_client.return_value.__aenter__.return_value
        instance.get.return_value = mock_response

        # First barcode
        response1 = await async_client.get("/off/v1/knowledge-panel/111111111")
        assert response1.status_code == 200
        calls_after_first = instance.get.call_count

        # Different barcode - should trigger new API call
        response2 = await async_client.get("/off/v1/knowledge-panel/222222222")
        assert response2.status_code == 200
        calls_after_second = instance.get.call_count

        # Verify both requests triggered API calls (different cache entries)
        assert calls_after_second > calls_after_first

        # Same barcode as first request - should be cache hit
        response1_cached = await async_client.get("/off/v1/knowledge-panel/111111111")
        assert response1_cached.status_code == 200

        # Verify no additional API call was made (cache hit)
        assert instance.get.call_count == calls_after_second
