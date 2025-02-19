import logging
import uuid
from contextvars import ContextVar
from urllib.parse import parse_qs

from fastapi import Request

from app.config.i18n import get_i18n

request_id_ctx = ContextVar("request_id", default=None)


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request_id_ctx.get()
        return True


async def request_id_middleware(request: Request, call_next):
    """
    Middleware that generates and tracks a unique identifier (UUID) for each HTTP request.
    This allows for request tracing and debugging across the application.

    - Generates a unique UUID for each incoming request
    - Adds the ID to response headers as 'X-Request-ID'
    - Makes the ID available to the logging system via RequestIdFilter
    """
    request_id = str(uuid.uuid4())
    request_id_ctx.set(request_id)

    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id

    return response


async def add_locale_translator(request: Request, call_next):
    """
    Middleware to add the translator to the request.state with priority URL -> Header
    """
    i18n = get_i18n()

    # Check if the locale is specified in the URL
    query_params = parse_qs(request.url.query)
    lang = query_params.get("lang", [None])[0]

    if lang and i18n.is_supported_locale(lang.lower()):
        locale = lang.lower()
    else:
        # If not, use the Accept-Language header
        accept_language = request.headers.get("Accept-Language", "")
        languages = [lang.split(";")[0].split("-")[0].lower() for lang in accept_language.split(",")]
        locale = next((locale for locale in languages if i18n.is_supported_locale(locale)), i18n.default_locale)

    # Add the translator to the request state
    request.state.translator = i18n.get_translator(locale)
    request.state.locale = locale

    response = await call_next(request)
    return response
