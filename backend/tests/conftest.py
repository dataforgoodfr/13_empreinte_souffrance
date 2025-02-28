from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from starlette.testclient import TestClient

from app.main import app


@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture that provides an async HTTP client configured for testing.
    Use with async FastAPI routes.
    """
    async with AsyncClient(
        base_url="http://test", transport=ASGITransport(app=app)
    ) as client:
        yield client


@pytest.fixture
def client() -> TestClient:
    """
    Fixture that provides a sync HTTP client for testing.
    """
    return TestClient(app)
