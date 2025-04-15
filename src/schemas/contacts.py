"""Contact data validation and serialization schemas.

This module defines Pydantic models for contact management:
- Contact creation and update validation
- Response serialization
- Error handling
- Field-level validation using Pydantic types
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, PastDate
from pydantic_extra_types.phone_numbers import PhoneNumber

from src.schemas.core import ErrorResponseModel


class ContactModel(BaseModel):
    """Base model for contact data validation.

    This model defines the core fields for a contact and their validation rules.
    Used for both creating new contacts and updating existing ones.

    Attributes:
        first_name (str): Contact's first name, max 50 chars
        last_name (str): Contact's last name, max 50 chars
        email (EmailStr): Valid email address, max 255 chars
        phone (PhoneNumber): Optional phone number in international format
        birthday (PastDate): Optional birth date, must be in the past
        description (str): Optional notes about the contact, max 255 chars

    Example:
        >>> contact = ContactModel(
        ...     first_name="John",
        ...     last_name="Doe",
        ...     email="john@example.com",
        ...     phone="+1234567890",
        ...     birthday="1990-01-01"
        ... )
    """

    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: EmailStr = Field(max_length=255)
    phone: Optional[PhoneNumber] = Field(default=None, max_length=20)
    birthday: Optional[PastDate] = None
    description: Optional[str] | None = Field(default=None, max_length=255)


class ContactResponse(ContactModel):
    """Response model for contact data.

    Extends the base ContactModel to include database-generated fields
    that are returned in API responses.

    Attributes:
        id (int): Contact's unique identifier
        created_at (datetime): Timestamp of contact creation
        updated_at (datetime): Timestamp of last update

    Example:
        >>> response = ContactResponse(
        ...     id=1,
        ...     first_name="John",
        ...     last_name="Doe",
        ...     email="john@example.com",
        ...     created_at="2024-01-01T00:00:00",
        ...     updated_at="2024-01-01T00:00:00"
        ... )
    """

    id: int
    created_at: datetime
    updated_at: datetime


class ContactNotFoundResponse(ErrorResponseModel):
    """Error response for contact not found errors.

    Used when a requested contact cannot be found in the database.
    Inherits from ErrorResponseModel to maintain consistent error format.

    Attributes:
        detail (str): Error message, defaults to "Contact not found"

    Example:
        >>> error = ContactNotFoundResponse()
        >>> error.model_dump()
        {'detail': 'Contact not found'}
    """

    detail: str = Field(default="Contact not found")
