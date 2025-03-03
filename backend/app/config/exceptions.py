"""
Centralized exception handling for the application.
Defines custom exceptions and utilities for consistent error handling.
"""

import logging

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
