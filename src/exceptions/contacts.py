"""Contact management exception classes.

This module defines exceptions specific to contact operations including:
- Email validation errors
- Entity lookup failures
- Contact-specific errors

All exceptions inherit from the core application exceptions to ensure
consistent error handling and response formatting.
"""

from src.exceptions.core import AppKeyError, AppValueError


class EmailValueError(AppValueError):
    """Exception raised for invalid email addresses.

    This exception is used when an email address fails validation,
    such as incorrect format or duplicate email within a user's contacts.

    Example:
        raise EmailValueError("Email address is already in use")
    """


class EntityNotFound(AppKeyError):
    """Base exception for database entity lookup failures.

    This exception is raised when attempting to access or modify
    an entity that does not exist in the database.

    Example:
        raise EntityNotFound("User with ID 123 not found")
    """


class ContactNotFound(EntityNotFound):
    """Exception raised when a contact is not found.

    This exception is used specifically for contact lookup failures,
    inheriting from EntityNotFound for consistent error handling.

    Example:
        raise ContactNotFound("Contact with ID 456 not found")
    """
