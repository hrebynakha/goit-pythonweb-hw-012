"""Contacts validation schema"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, PastDate
from pydantic_extra_types.phone_numbers import PhoneNumber

from src.schemas.core import ErrorResponseModel


class ContactModel(BaseModel):
    """Base contact model"""

    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: EmailStr = Field(max_length=255)
    phone: Optional[PhoneNumber] = Field(default=None, max_length=20)
    birthday: Optional[PastDate] = None
    description: Optional[str] | None = Field(default=None, max_length=255)


class ContactResponse(ContactModel):
    """Response model"""

    id: int
    created_at: datetime
    updated_at: datetime


class ContactNotFoundResponse(ErrorResponseModel):
    """Contact not found schehma"""

    detail: str = Field(default="Contact not found")
