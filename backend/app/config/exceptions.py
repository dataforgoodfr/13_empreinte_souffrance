"""
Centralized exception handling for the application.
Defines custom exceptions and utilities for consistent error handling.
"""

import logging

from app.schemas.open_food_facts.internal import PainReport

logger = logging.getLogger("app")


class BaseAppException(Exception):
    """Base exception for all application-specific exceptions."""

    status_code = 500
    default_message = "An unexpected error occurred"

    def __init__(self, message=None, status_code=None):
        """
        Initialize the exception with a message and status code.

        Args:
            message: The error message
            status_code: HTTP status code
        """
        self.message = message or self.default_message
        self.status_code = status_code or self.status_code
        super().__init__(self.message)


class ResourceNotFoundException(BaseAppException):
    """Exception raised when a requested resource is not found."""

    status_code = 404
    default_message = "Resource not found"


class ExternalServiceException(BaseAppException):
    """Exception raised when an external service fails."""

    status_code = 502
    default_message = "External service error"


class MissingBreedingType(Exception):
    """Exception raised when breeding type is missing for an animal product
    Catched in PainReportCalculator to return empty pain levels
    and generate specific knowledge panel."""

    default_message = "Missing breeding type for animal product."


class EggButNotFreshEgg(Exception):
    def __init__(self, pain_report: PainReport, message: str = "Egg but not fresh egg"):
        self.message = message
        self.pain_report = pain_report
        super().__init__(message)
