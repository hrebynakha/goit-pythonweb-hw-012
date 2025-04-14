"""Contacts models"""

from datetime import date, datetime

from sqlalchemy import Integer, String, Date, func, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.sql.schema import UniqueConstraint

from src.database.basic import Base
from src.models.users import User


class Contact(Base):
    """Contact model"""

    __tablename__ = "contacts"
    __table_args__ = (UniqueConstraint("email", "user_id", name="unique_email_user"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    birthday: Mapped[date] = mapped_column(Date, nullable=True)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        "created_at", DateTime, default=func.now()  # pylint: disable=not-callable
    )
    updated_at: Mapped[datetime] = mapped_column(
        "updated_at",
        DateTime,
        default=func.now(),  # pylint: disable=not-callable
        onupdate=func.now(),  # pylint: disable=not-callable
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), default=None
    )
    user: Mapped["User"] = relationship("User", backref="contacts")
