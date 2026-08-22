from unittest.mock import AsyncMock, patch

import httpx
import pytest

from app.config.http_client import get_with_retry


def _make_response(status_code: int = 200) -> httpx.Response:
    request = httpx.Request("GET", "https://example.com")
    return httpx.Response(status_code, request=request)


@pytest.mark.asyncio
async def test_succeeds_on_first_attempt_without_sleeping():
    response = _make_response()

    with (
        patch("app.config.http_client.client.get", new_callable=AsyncMock, return_value=response) as mock_get,
        patch("app.config.http_client.asyncio.sleep", new_callable=AsyncMock) as mock_sleep,
    ):
        result = await get_with_retry("https://example.com")

    assert result is response
    assert mock_get.call_count == 1
    mock_sleep.assert_not_called()


@pytest.mark.asyncio
async def test_retries_after_transient_errors_then_succeeds():
    response = _make_response()

    with (
        patch("app.config.http_client.client.get", new_callable=AsyncMock) as mock_get,
        patch("app.config.http_client.asyncio.sleep", new_callable=AsyncMock) as mock_sleep,
    ):
        mock_get.side_effect = [httpx.ReadTimeout("timeout"), httpx.ReadTimeout("timeout"), response]

        result = await get_with_retry("https://example.com", retries=3, base_delay=1.0)

    assert result is response
    assert mock_get.call_count == 3
    # Exponential backoff: base_delay * 2**attempt for each failed attempt
    assert [call.args[0] for call in mock_sleep.call_args_list] == [1.0, 2.0]


@pytest.mark.asyncio
async def test_raises_last_exception_after_exhausting_all_retries():
    with (
        patch("app.config.http_client.client.get", new_callable=AsyncMock) as mock_get,
        patch("app.config.http_client.asyncio.sleep", new_callable=AsyncMock),
    ):
        mock_get.side_effect = httpx.ReadTimeout("still timing out")

        with pytest.raises(httpx.ReadTimeout, match="still timing out"):
            await get_with_retry("https://example.com", retries=3, base_delay=0.01)

    assert mock_get.call_count == 3


@pytest.mark.asyncio
async def test_does_not_sleep_after_the_final_failed_attempt():
    """There is nothing to wait for once the last retry has failed."""
    with (
        patch("app.config.http_client.client.get", new_callable=AsyncMock) as mock_get,
        patch("app.config.http_client.asyncio.sleep", new_callable=AsyncMock) as mock_sleep,
    ):
        mock_get.side_effect = httpx.ReadTimeout("timeout")

        with pytest.raises(httpx.ReadTimeout):
            await get_with_retry("https://example.com", retries=2, base_delay=1.0)

    # Only one sleep, between attempt 1 and attempt 2 - none after the last attempt
    assert mock_sleep.call_count == 1


@pytest.mark.asyncio
async def test_http_status_error_is_retried_like_a_transient_error():
    """A raise_for_status() 5xx error must be retried the same way as a network timeout."""
    error_response = _make_response(status_code=503)
    ok_response = _make_response(status_code=200)

    with (
        patch("app.config.http_client.client.get", new_callable=AsyncMock) as mock_get,
        patch("app.config.http_client.asyncio.sleep", new_callable=AsyncMock),
    ):
        mock_get.side_effect = [error_response, ok_response]

        result = await get_with_retry("https://example.com", retries=3, base_delay=0.01)

    assert result is ok_response
    assert mock_get.call_count == 2


@pytest.mark.asyncio
async def test_concurrent_requests_are_capped_by_the_semaphore():
    """
    The shared semaphore limits in-flight requests to 3. This test issues 6 concurrent
    calls and checks that the observed number of simultaneously "in-progress" calls
    never exceeds that cap.
    """
    import asyncio

    in_flight = 0
    max_in_flight = 0
    lock = asyncio.Lock()

    async def fake_get(url, **kwargs):
        nonlocal in_flight, max_in_flight
        async with lock:
            in_flight += 1
            max_in_flight = max(max_in_flight, in_flight)
        await asyncio.sleep(0.01)
        async with lock:
            in_flight -= 1
        return _make_response()

    with patch("app.config.http_client.client.get", new_callable=AsyncMock, side_effect=fake_get):
        await asyncio.gather(*[get_with_retry("https://example.com") for _ in range(6)])

    assert max_in_flight <= 3
