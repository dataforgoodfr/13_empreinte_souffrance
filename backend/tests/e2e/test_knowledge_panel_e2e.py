"""
End-to-end tests for the knowledge panel feature.

Unlike the rest of the test suites, these tests mock only the outermost network
boundary (`app.config.http_client.client.get`, i.e. the httpx transport). Everything
else runs for real: the locale middleware, routing, the retry/backoff logic, JSON
parsing and Pydantic validation, pain calculation, panel rendering, caching, and the
global exception handling. They exist to catch integration regressions that
layer-isolated unit tests, by construction, cannot - e.g. a field renamed in the
Pydantic schema but not in the calculator, or a middleware ordering change.

They are intentionally few and high-level; exhaustive edge cases belong in the
targeted unit test suites (calculators, service, routes, middlewares, cache,
http_client).
"""

from unittest.mock import AsyncMock, Mock, patch

import httpx
import pytest
from httpx import AsyncClient

from app.config.cache import knowledge_panel_cache


def _mock_off_response(json_data: dict, status_code: int = 200) -> Mock:
    """Build a fake httpx.Response-like object for the given JSON body and status code."""
    response = Mock()
    response.json = Mock(return_value=json_data)

    if status_code >= 400:
        request = httpx.Request("GET", "https://world.openfoodfacts.org")
        response.raise_for_status = Mock(
            side_effect=httpx.HTTPStatusError(
                "error", request=request, response=httpx.Response(status_code, request=request)
            )
        )
    else:
        response.raise_for_status = Mock(return_value=None)

    return response


@pytest.mark.asyncio
async def test_full_pipeline_for_a_caged_eggs_product(async_client: AsyncClient, off_v3_caged_eggs_payload: dict):
    """A realistic OFF v3 payload flows end-to-end through the whole stack into a full knowledge panel."""
    knowledge_panel_cache.clear()

    with patch("app.config.http_client.client.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = _mock_off_response(off_v3_caged_eggs_payload)
        response = await async_client.get("/off/v1/knowledge-panel/3256540011346", headers={"Accept-Language": "fr"})

    assert response.status_code == 200
    body = response.json()
    assert "root" in body["panels"]
    assert "project_panel" in body["panels"]
    assert body["product"]["name"] == "Oeufs de poules elevees en cage"


@pytest.mark.asyncio
async def test_locale_falls_back_to_generic_name_when_translation_missing(
    async_client: AsyncClient, off_v3_caged_eggs_payload: dict
):
    """When product_name_<locale> is absent from the payload, the generic product_name is used."""
    knowledge_panel_cache.clear()
    payload = off_v3_caged_eggs_payload
    del payload["product"]["product_name_fr"]

    with patch("app.config.http_client.client.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = _mock_off_response(payload)
        response = await async_client.get("/off/v1/knowledge-panel/3256540011346", headers={"Accept-Language": "fr"})

    assert response.status_code == 200
    assert response.json()["product"]["name"] == "Oeufs de poules elevees en cage"


@pytest.mark.asyncio
async def test_downstream_500_from_off_surfaces_as_a_clean_404(async_client: AsyncClient):
    """A 5xx from OFF must never leak upstream; the documented contract is a clean 404."""
    knowledge_panel_cache.clear()

    with (
        patch("app.config.http_client.client.get", new_callable=AsyncMock) as mock_get,
        patch("app.config.http_client.asyncio.sleep", new_callable=AsyncMock),  # skip real retry backoff delays
    ):
        mock_get.return_value = _mock_off_response({}, status_code=503)
        response = await async_client.get("/off/v1/knowledge-panel/0000000000000")

    assert response.status_code == 404
    assert response.json()["error"]["status"] == 404


@pytest.mark.asyncio
async def test_unknown_barcode_surfaces_as_404(async_client: AsyncClient, off_v3_not_found_payload: dict):
    """OFF replies 200 with status:0 and no 'product' key for an unknown barcode; we must still 404."""
    knowledge_panel_cache.clear()

    with patch("app.config.http_client.client.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = _mock_off_response(off_v3_not_found_payload)
        response = await async_client.get("/off/v1/knowledge-panel/0000000000000")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_batch_mixes_success_failure_and_cache_hit_end_to_end(
    async_client: AsyncClient, off_v3_caged_eggs_payload: dict, off_v3_not_found_payload: dict
):
    """One barcode is served from cache, one succeeds fresh, and one fails - all in a single batch call."""
    knowledge_panel_cache.clear()

    async def fake_get(url, **kwargs):
        if "111111111" in url or "222222222" in url:
            return _mock_off_response(off_v3_caged_eggs_payload)
        return _mock_off_response(off_v3_not_found_payload)

    with patch("app.config.http_client.client.get", new_callable=AsyncMock) as mock_get:
        mock_get.side_effect = fake_get

        # Warm the cache for barcode 111111111 with a preliminary single-product call.
        warm_up = await async_client.get("/off/v1/knowledge-panel/111111111")
        assert warm_up.status_code == 200
        calls_after_warmup = mock_get.call_count

        response = await async_client.get("/off/v1/knowledge-panel/?code=111111111,222222222,999999999")

    assert response.status_code == 200
    body = response.json()
    assert set(body["panels"].keys()) == {"111111111", "222222222"}
    assert "999999999" in body["errors"]
    # 111111111 came from cache: only 222222222 and 999999999 should have hit OFF for real
    assert mock_get.call_count == calls_after_warmup + 2


@pytest.mark.asyncio
async def test_head_request_returns_no_body_end_to_end(async_client: AsyncClient, off_v3_caged_eggs_payload: dict):
    knowledge_panel_cache.clear()

    with patch("app.config.http_client.client.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = _mock_off_response(off_v3_caged_eggs_payload)
        response = await async_client.head("/off/v1/knowledge-panel/3256540011346")

    assert response.status_code == 200
    assert response.content == b""


@pytest.mark.asyncio
async def test_unsupported_locale_falls_back_to_default_end_to_end(
    async_client: AsyncClient, off_v3_caged_eggs_payload: dict
):
    knowledge_panel_cache.clear()

    with patch("app.config.http_client.client.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = _mock_off_response(off_v3_caged_eggs_payload)
        response = await async_client.get("/off/v1/knowledge-panel/3256540011346", headers={"Accept-Language": "de-DE"})

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_transient_network_error_is_retried_then_succeeds_end_to_end(
    async_client: AsyncClient, off_v3_caged_eggs_payload: dict
):
    """A couple of transient read timeouts must be absorbed by the retry logic without surfacing to the client."""
    knowledge_panel_cache.clear()

    with (
        patch("app.config.http_client.client.get", new_callable=AsyncMock) as mock_get,
        patch("app.config.http_client.asyncio.sleep", new_callable=AsyncMock),  # skip real backoff delays
    ):
        mock_get.side_effect = [
            httpx.ReadTimeout("timeout"),
            httpx.ReadTimeout("timeout"),
            _mock_off_response(off_v3_caged_eggs_payload),
        ]
        response = await async_client.get("/off/v1/knowledge-panel/3256540011346")

    assert response.status_code == 200
    assert mock_get.call_count == 3
