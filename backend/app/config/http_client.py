import asyncio
import logging
from typing import Optional

import httpx

logger = logging.getLogger("app")

client = httpx.AsyncClient(
    headers={"User-Agent": "my-app/1.0"},
    follow_redirects=True,
    timeout=httpx.Timeout(connect=5.0, read=10.0, write=10.0, pool=5.0),
    limits=httpx.Limits(
        max_connections=20,
        max_keepalive_connections=10,
    ),
)

_semaphore = asyncio.Semaphore(3)


async def get(url: str, **kwargs) -> httpx.Response:
    async with _semaphore:
        response = await client.get(url, **kwargs)
        response.raise_for_status()
        return response


async def get_with_retry(
    url: str,
    retries: int = 3,
    base_delay: float = 1.0,
    **kwargs,
) -> httpx.Response:
    last_exception: Optional[Exception] = None

    for attempt in range(retries):
        try:
            return await get(url, **kwargs)

        except (httpx.HTTPError, httpx.TimeoutException) as e:
            last_exception = e
            logger.warning(f"HTTP error on attempt {attempt + 1}/{retries} for {url}: {type(e).__name__}")

            if attempt < retries - 1:
                await asyncio.sleep(base_delay * (2**attempt))

    if last_exception is not None:
        raise last_exception


async def close_http_client():
    await client.aclose()
