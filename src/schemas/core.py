"""Core response schemas for the application.

This module defines base response models that are used across the application.
It provides:
- Standard error response format
- Base classes for other response models
"""

from pydantic import BaseModel


class ErrorResponseModel(BaseModel):
    """Base model for error responses.

    This model defines a standard format for error responses across all API endpoints.
    It is used as a base class for specific error response types.

    Attributes:
        detail (str): Human-readable error message describing what went wrong

    Example:
        >>> error = ErrorResponseModel(detail="Resource not found")
        >>> error.model_dump()
        {'detail': 'Resource not found'}
    """

    detail: str
