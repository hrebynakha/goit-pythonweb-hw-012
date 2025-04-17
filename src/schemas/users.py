"""User data validation and serialization schemas.

This module defines Pydantic models for user data handling:
- User response serialization
- User creation validation
- ORM model integration
"""

import enum
from pydantic import ConfigDict, BaseModel, EmailStr, Field


class User(BaseModel):
    """User response model.

    Used for serializing user data in API responses. Sensitive fields like
    password and refresh_token are excluded.

    Attributes:
        id (int): User's unique identifier
        username (str): User's display name
        email (str): User's email address
        avatar (str): URL to user's avatar image

    Note:
        model_config enables automatic conversion from SQLAlchemy models
    """

    id: int
    username: str = Field(min_length=3, max_length=40)
    email: EmailStr
    avatar: str
    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    """User creation request model.

    Used for validating new user registration data.

    Attributes:
        username (str): Desired username, 3-40 chars
        email (EmailStr): Valid email address
        password (str): Password, minimum 8 chars

    Note:
        Email format is validated by Pydantic's EmailStr
        Password requirements are enforced at the service layer
    """

    username: str = Field(min_length=3, max_length=40)
    email: EmailStr
    password: str = Field(min_length=8)


class AdvancedUser(User):
    """User model with additional fields for caching."""

    role: str
    is_verified: bool
