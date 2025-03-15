from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from starlette.testclient import TestClient

from app.main import app
from app.schemas.open_food_facts.external import ProductData


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


@pytest.fixture
def product_data() -> ProductData:
    return ProductData(
        categories_tags=["cat1", "en:cage-chicken-eggs"],
        labels_tags=["label1", "label2"]
    )
