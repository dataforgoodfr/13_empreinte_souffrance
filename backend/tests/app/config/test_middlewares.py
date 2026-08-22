import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette.requests import Request

from app.config.exceptions import BaseAppException, ResourceNotFoundException
from app.config.middlewares import GlobalExceptionMiddleware, add_locale_translator

# --- GlobalExceptionMiddleware ---


def _build_exception_test_app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(GlobalExceptionMiddleware)

    @app.get("/boom-known")
    async def boom_known():
        raise ResourceNotFoundException("product missing")

    @app.get("/boom-custom-status")
    async def boom_custom_status():
        raise BaseAppException("custom failure", status_code=418)

    @app.get("/boom-unknown")
    async def boom_unknown():
        raise ValueError("something exploded")

    @app.get("/ok")
    async def ok():
        return {"status": "ok"}

    return app


@pytest.fixture
def exception_client() -> TestClient:
    return TestClient(_build_exception_test_app())


def test_known_app_exception_returns_its_own_status_and_message(exception_client: TestClient):
    response = exception_client.get("/boom-known")

    assert response.status_code == 404
    body = response.json()
    assert body["error"]["status"] == 404
    assert body["error"]["message"] == "product missing"


def test_custom_status_code_below_500_is_not_masked(exception_client: TestClient):
    response = exception_client.get("/boom-custom-status")

    assert response.status_code == 418
    assert response.json()["error"]["message"] == "custom failure"


def test_unknown_exception_is_masked_as_generic_server_error(exception_client: TestClient):
    """A raw, unexpected exception must never leak its message to the client."""
    response = exception_client.get("/boom-unknown")

    assert response.status_code == 500
    body = response.json()
    assert body["error"]["status"] == 500
    assert body["error"]["message"] == "An unexpected server error occurred"
    assert "exploded" not in body["error"]["message"]


def test_happy_path_is_unaffected_by_the_middleware(exception_client: TestClient):
    response = exception_client.get("/ok")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# --- add_locale_translator ---


def _build_locale_test_app() -> FastAPI:
    app = FastAPI()
    app.middleware("http")(add_locale_translator)

    @app.get("/locale")
    async def get_locale(request: Request):
        return {"locale": request.state.locale}

    return app


@pytest.fixture
def locale_client() -> TestClient:
    return TestClient(_build_locale_test_app())


@pytest.mark.parametrize(
    "headers,expected_locale",
    [
        ({}, "en"),  # no header at all -> default locale
        ({"Accept-Language": "fr"}, "fr"),
        ({"Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8"}, "fr"),  # full BCP-47 tag with quality values
        ({"Accept-Language": "de"}, "en"),  # unsupported locale -> falls back to default
        ({"Accept-Language": "de,fr;q=0.8"}, "fr"),  # first supported locale in the preference list wins
    ],
)
def test_locale_resolved_from_accept_language_header(locale_client: TestClient, headers: dict, expected_locale: str):
    response = locale_client.get("/locale", headers=headers)

    assert response.json()["locale"] == expected_locale


def test_url_lang_param_takes_priority_over_accept_language_header(locale_client: TestClient):
    response = locale_client.get("/locale?lang=fr", headers={"Accept-Language": "en"})

    assert response.json()["locale"] == "fr"


def test_unsupported_url_lang_param_falls_back_to_header(locale_client: TestClient):
    response = locale_client.get("/locale?lang=de", headers={"Accept-Language": "fr"})

    assert response.json()["locale"] == "fr"


def test_url_lang_param_is_case_insensitive(locale_client: TestClient):
    response = locale_client.get("/locale?lang=FR")

    assert response.json()["locale"] == "fr"
