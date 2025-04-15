"""SQLAlchemy models for contact management.

This module defines the database models for contacts using SQLAlchemy ORM.
It includes:
- Contact model with user association
- Automatic timestamp management
- Unique constraint enforcement
- Cascade deletion rules
"""

from datetime import date, datetime

from sqlalchemy import Integer, String, Date, func, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.sql.schema import UniqueConstraint

from src.database.basic import Base
from src.models.users import User


class Contact(Base):
    """SQLAlchemy model for contact information.

    This model represents a contact in the system, associated with a user.
    It includes personal information, contact details, and metadata fields.

    Table name: contacts

    Attributes:
        id (int): Primary key
        first_name (str): Contact's first name, max 50 chars, required
        last_name (str): Contact's last name, max 50 chars, required
        email (str): Contact's email address, max 255 chars, required
        phone (str): Optional phone number, max 20 chars
        birthday (date): Optional birth date for birthday reminders
        description (str): Optional notes about contact, max 255 chars
        created_at (datetime): Automatic timestamp of creation
        updated_at (datetime): Automatic timestamp of last update
        user_id (int): Foreign key to users table
        user (User): Relationship to User model

    Constraints:
        - Email addresses must be unique per user (composite unique constraint)
        - First name and last name are required
        - Deleting a user will cascade delete their contacts
        - created_at and updated_at are automatically managed
    """

    __tablename__ = "contacts"
    __table_args__ = (UniqueConstraint("email", "user_id", name="unique_email_user"),)

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Personal information
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    birthday: Mapped[date] = mapped_column(Date, nullable=True)
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    # Metadata timestamps
    created_at: Mapped[datetime] = mapped_column(
        "created_at", DateTime, default=func.now()  # pylint: disable=not-callable
    )
    updated_at: Mapped[datetime] = mapped_column(
        "updated_at",
        DateTime,
        default=func.now(),  # pylint: disable=not-callable
        onupdate=func.now(),  # pylint: disable=not-callable
    )

    # Relationships
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), default=None
    )
    user: Mapped["User"] = relationship("User", backref="contacts")
