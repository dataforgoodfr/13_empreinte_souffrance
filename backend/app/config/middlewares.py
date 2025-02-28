from urllib.parse import parse_qs

from fastapi import Request
from fastapi.responses import JSONResponse
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware

from app.config.exceptions import BaseAppException
from app.config.i18n import get_i18n


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
        languages = [
            lang.split(";")[0].split("-")[0].lower()
            for lang in accept_language.split(",")
        ]
        locale = next(
            (locale for locale in languages if i18n.is_supported_locale(locale)),
            i18n.default_locale,
        )

    # Add the translator to the request state
    request.state.translator = i18n.get_translator(locale)
    request.state.locale = locale

    response = await call_next(request)
    return response


class GlobalExceptionMiddleware(BaseHTTPMiddleware):
    """
    Middleware to catch and properly handle all unhandled exceptions.
    This ensures consistent error responses across the application.
    """

    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            # Log the exception with path context
            if isinstance(e, BaseAppException):
                # If it's a known exception, just log the message
                logger.warning(f"{str(e)} (path: {request.url.path})")
            else:
                # If it's not a known exception, log the full traceback
                logger.exception(f"Unknown exception: {e} (path: {request.url.path})")

            # Determine status code
            status_code = getattr(e, "status_code", 500)

            # Get error message
            detail = getattr(e, "detail", None) or str(e)

            # Hide internal server errors with a generic message
            if 500 <= status_code < 600:
                detail = "An unexpected server error occurred"
            
            # Create JSON response with error details
            return JSONResponse(
                status_code=status_code,
                content={
                    "error": {
                        "status": status_code,
                        "message": detail,
                    }
                },
            )
