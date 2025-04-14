"""Main app entrypoint"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded

from src.api import utils, contacts, auth, users

from src.conf.config import settings
from src.exceptions.core import AppHttpError, AppValueError, AppKeyError
from src.exceptions.contacts import EmailValueError, ContactNotFound
from src.schemas.core import ErrorResponseModel

app = FastAPI(
    responses={
        500: {"model": ErrorResponseModel, "description": "Internal server error"},
        400: {"model": ErrorResponseModel, "description": "Bad request"},
    }
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_CORS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(utils.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, error: RateLimitExceeded):
    raise AppHttpError(
        status_code=429,
        detail="Request limit exceeded. Please try again later.",
    )


@app.exception_handler(AppValueError)
async def value_exception_handler(
    request: Request, error: AppValueError  # pylint: disable=unused-argument
):
    """Value error"""
    if isinstance(error, EmailValueError):
        raise AppHttpError(detail=str(error))
    raise AppHttpError(detail="Ooops, some value error happend!")


@app.exception_handler(AppKeyError)
async def key_exception_handler(
    request: Request, error: AppValueError  # pylint: disable=unused-argument
):
    """Key error"""
    if isinstance(error, ContactNotFound):
        raise AppHttpError(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    raise AppHttpError(detail="Ooops, some value error happend!")


@app.exception_handler(ConnectionRefusedError)
async def connection_exception_handler(
    request: Request, error: ConnectionRefusedError  # pylint: disable=unused-argument
):
    """ConnectionR efusedError)"""
    if isinstance(error, ConnectionRefusedError):
        raise AppHttpError(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection error",
        )
    raise AppHttpError(detail="Ooops, some value error happend!")
