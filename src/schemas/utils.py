"""Utility response schemas for API health checking.

This module defines models used in the API health check endpoint.
It provides:
- Health check success response
- Health check error response
"""

from pydantic import BaseModel, Field
from src.schemas.core import ErrorResponseModel


class HealthCheckModel(BaseModel):
    """Health check success response model.

    Used for the API health check endpoint to indicate that the service
    is running correctly.

    Attributes:
        message (str): Welcome message, defaults to "Welcome to FastAPI!"

    Example:
        >>> health = HealthCheckModel()
        >>> health.model_dump()
        {'message': 'Welcome to FastAPI!'}
    """

    message: str = Field(default="Welcome to FastAPI!")


class HealthCheckErrorModel(ErrorResponseModel):
    """Health check error response model.

    Used when the health check endpoint detects a problem with the service.
    Inherits from ErrorResponseModel to maintain consistent error response format.

    Example:
        >>> error = HealthCheckErrorModel(detail="Database connection failed")
        >>> error.model_dump()
        {'detail': 'Database connection failed'}
    """
