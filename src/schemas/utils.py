"""HealthCheckModel"""

from pydantic import BaseModel, Field
from src.schemas.core import ErrorResponseModel


class HealthCheckModel(BaseModel):
    """Base contact model"""

    message: str = Field(default="Welcome to FastAPI!")


class HealthCheckErrorModel(ErrorResponseModel):
    """Health Check error model"""
