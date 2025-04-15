"""SQLAlchemy models for user management.

This module defines the database models for user accounts using SQLAlchemy ORM.
It includes:
- User model with authentication fields
- Email verification tracking
- JWT refresh token storage
- Avatar URL management
- Automatic timestamp handling
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Integer, String, func, Boolean
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.sql.sqltypes import DateTime

from src.database.basic import Base


class User(Base):
    """SQLAlchemy model for user accounts.

    This model represents a user in the system and includes fields for
    authentication, profile data, and account status tracking.

    Table name: users

    Attributes:
        id (int): Primary key
        username (str): Unique username, max 40 chars
        email (str): Unique email address, max 255 chars
        hashed_password (str): Bcrypt hashed password
        created_at (datetime): Automatic timestamp of account creation
        avatar (str): Optional URL to user's avatar image, max 255 chars
        refresh_token (str): Optional JWT refresh token, max 255 chars
        is_verified (bool): Email verification status, defaults to False

    Note:
        - Both username and email have unique constraints
        - Password is stored as a bcrypt hash, never in plain text
        - created_at is automatically set on creation
        - refresh_token is updated on each token refresh operation
        - Avatar URL is typically set via Gravatar or file upload
    """

    __tablename__ = "users"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Authentication fields
    username: Mapped[str] = mapped_column(String(40), unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    hashed_password: Mapped[str] = mapped_column(String)

    # Metadata
    created_at: Mapped[datetime] = mapped_column(
        "created_at", DateTime, default=func.now()  # pylint: disable=not-callable
    )

    # Profile and authentication state
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)
    refresh_token: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
