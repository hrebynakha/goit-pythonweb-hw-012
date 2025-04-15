"""SQLAlchemy declarative base configuration.

This module provides the base configuration for SQLAlchemy models
using the declarative mapping pattern. It defines the base class
that all models will inherit from to gain ORM functionality.

Example:
    from src.database.basic import Base

    class User(Base):
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True)
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """SQLAlchemy declarative base class.

    This class serves as the base for all database models in the application.
    It provides core SQLAlchemy ORM functionality including:
    - Table creation and schema management
    - Relationship management
    - Query interface
    - Session integration
    - Model validation

    All model classes should inherit from this base class to ensure
    proper database integration and consistent behavior.

    Example:
        class Contact(Base):
            __tablename__ = 'contacts'
            id = Column(Integer, primary_key=True)
            name = Column(String)
    """
