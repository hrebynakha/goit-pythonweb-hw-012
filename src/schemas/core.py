"""Core schemas response"""

from pydantic import BaseModel


class ErrorResponseModel(BaseModel):
    """Error health check response model"""

    detail: str
