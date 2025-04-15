"""Authentication and authorization exception classes.

This module defines exceptions specific to authentication and authorization operations.
It includes exceptions for:
- Invalid credentials
- User registration conflicts
- Email verification issues
- Token validation errors
"""

from fastapi import status
from src.exceptions.core import AppHttpError


class AuthError(AppHttpError):
    """Exception raised for general authentication errors.

    This exception is used when authentication fails due to invalid or expired
    credentials, missing tokens, or other authentication-related issues.

    Args:
        status_code (int, optional): HTTP status code. Defaults to 401.
        detail (str, optional): Error message. Defaults to "Could not validate credentials".

    Note:
        Automatically adds WWW-Authenticate: Bearer header as per RFC 6750.
    """

    def __init__(
        self,
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail: str = "Could not validate credentials",
    ):
        super().__init__(status_code, detail, {"WWW-Authenticate": "Bearer"})


class RegistrationError(AppHttpError):
    """Exception raised when user registration fails.

    This exception is used when a new user cannot be registered,
    typically due to conflicts with existing users.

    Args:
        status_code (int, optional): HTTP status code. Defaults to 409.
        detail (str, optional): Error message. Defaults to "User with this username already exists".
        headers (dict, optional): Additional HTTP headers. Defaults to None.
    """

    def __init__(
        self,
        status_code=status.HTTP_409_CONFLICT,
        detail: str = "User with this username already exists",
        headers: dict = None,
    ):
        super().__init__(status_code, detail, headers)


class InvalidVerificationTokenError(AppHttpError):
    """Exception raised for invalid email verification tokens.

    This exception is used when an email verification token is invalid,
    expired, or has been tampered with.

    Args:
        status_code (int, optional): HTTP status code. Defaults to 422.
        detail (str, optional): Error message. Defaults to "Invalid email verification token".
        headers (dict, optional): Additional HTTP headers. Defaults to None.
    """

    def __init__(
        self,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail: str = "Invalid email verification token",
        headers: dict = None,
    ):
        super().__init__(status_code, detail, headers)


class VerificationError(AppHttpError):
    """Exception raised for general verification process errors.

    This exception is used when the verification process fails due to
    system errors, invalid states, or other verification-related issues.

    Args:
        status_code (int, optional): HTTP status code. Defaults to 400.
        detail (str, optional): Error message. Defaults to "Verification error".
        headers (dict, optional): Additional HTTP headers. Defaults to None.
    """

    def __init__(
        self,
        status_code=status.HTTP_400_BAD_REQUEST,
        detail: str = "Verification error",
        headers: dict = None,
    ):
        super().__init__(status_code, detail, headers)
