"""Authentication and authorization schemas.

This module defines Pydantic models for JWT token handling and authentication responses.
It includes:
- JWT token response models
- Token refresh request validation
- Authorization error responses
- Email verification responses
"""

from pydantic import BaseModel, Field
from src.schemas.core import ErrorResponseModel


class Token(BaseModel):
    """JWT token response model.

    Used for returning access and refresh tokens after successful authentication.

    Attributes:
        access_token (str): JWT access token for API authorization
        refresh_token (str): JWT refresh token for obtaining new access tokens
        token_type (str): Token type, typically "bearer"
    """

    access_token: str
    refresh_token: str
    token_type: str


class TokenRefreshRequest(BaseModel):
    """Token refresh request model.

    Used to validate refresh token requests for obtaining new access tokens.

    Attributes:
        refresh_token (str): Valid refresh token from previous authentication
    """

    refresh_token: str


class UnauthorizedResponse(ErrorResponseModel):
    """Unauthorized access error response.

    Used when a request requires authentication but valid credentials
    were not provided.

    Attributes:
        detail (str): Error message, defaults to "User not authorized."
    """

    detail: str = Field(default="User not authorized.")


class EmailVerifyResponse(BaseModel):
    """Email verification response model.

    Used for responses to email verification requests.

    Attributes:
        message (str): Status message about the verification result
    """

    message: str
