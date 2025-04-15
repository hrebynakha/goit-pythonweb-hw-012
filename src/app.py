"""FastAPI application entry point.

This module initializes and configures the FastAPI application, including:
- CORS middleware setup
- API router registration
- Global exception handlers
- Rate limiting configuration

The application provides RESTful endpoints for:
- User authentication and management
- Contact management
- Utility endpoints

All routes are prefixed with '/api' and include proper error handling
with standardized error responses.
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded

from src.api import utils, contacts, auth, users

from src.conf.config import settings
from src.exceptions.core import AppHttpError, AppValueError, AppKeyError
from src.exceptions.contacts import EmailValueError, ContactNotFound
from src.schemas.core import ErrorResponseModel

# Initialize FastAPI app with global error response models
app = FastAPI(
    responses={
        500: {"model": ErrorResponseModel, "description": "Internal server error"},
        400: {"model": ErrorResponseModel, "description": "Bad request"},
    }
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_CORS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(utils.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, error: RateLimitExceeded):
    """Handle rate limit exceeded errors.

    Args:
        request (Request): FastAPI request object
        error (RateLimitExceeded): Rate limit error

    Raises:
        AppHttpError: HTTP 429 error with rate limit message
    """
    raise AppHttpError(
        status_code=429,
        detail="Request limit exceeded. Please try again later.",
    )


@app.exception_handler(AppValueError)
async def value_exception_handler(
    request: Request, error: AppValueError  # pylint: disable=unused-argument
):
    """Handle application value errors.

    Special handling for email validation errors, with generic handling
    for other value errors.

    Args:
        request (Request): FastAPI request object
        error (AppValueError): Application value error

    Raises:
        AppHttpError: HTTP error with appropriate message
    """
    if isinstance(error, EmailValueError):
        raise AppHttpError(detail=str(error))
    raise AppHttpError(detail="Ooops, some value error happened!")


@app.exception_handler(AppKeyError)
async def key_exception_handler(
    request: Request, error: AppValueError  # pylint: disable=unused-argument
):
    """Handle application key errors.

    Special handling for contact not found errors, with generic handling
    for other key errors.

    Args:
        request (Request): FastAPI request object
        error (AppValueError): Application key error

    Raises:
        AppHttpError: HTTP error with appropriate status code and message
    """
    if isinstance(error, ContactNotFound):
        raise AppHttpError(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    raise AppHttpError(detail="Ooops, some value error happened!")


@app.exception_handler(ConnectionRefusedError)
async def connection_exception_handler(
    request: Request, error: ConnectionRefusedError  # pylint: disable=unused-argument
):
    """Handle database connection errors.

    Args:
        request (Request): FastAPI request object
        error (ConnectionRefusedError): Database connection error

    Raises:
        AppHttpError: HTTP 500 error with database connection message
    """
    if isinstance(error, ConnectionRefusedError):
        raise AppHttpError(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection error",
        )
    raise AppHttpError(detail="Ooops, some value error happened!")
