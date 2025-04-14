from pydantic import BaseModel, Field
from src.schemas.core import ErrorResponseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenRefreshRequest(BaseModel):
    refresh_token: str


class UnauthorizedResponse(ErrorResponseModel):
    """Contact not authorized schehma"""

    detail: str = Field(default="User not authorized.")


class EmailVerifyResponse(BaseModel):
    message: str
