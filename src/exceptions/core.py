"""Core exception classes for the application.

This module defines the base exception classes used throughout the application.
It provides a hierarchy of exceptions for:
- HTTP errors with status codes and headers
- Value validation errors
- Key-related errors

All application-specific exceptions should inherit from these base classes
to ensure consistent error handling and response formatting.
"""

from fastapi import HTTPException, status


class AppHttpError(HTTPException):
    """Base HTTP exception for application errors.

    This class extends FastAPI's HTTPException to provide consistent error
    handling across the application. It sets default status code and message
    while allowing customization through parameters.

    Args:
        status_code (int, optional): HTTP status code. Defaults to 400.
        detail (str, optional): Error message. Defaults to "Some error happened".
        headers (dict, optional): Additional HTTP headers. Defaults to None.

    Example:
        raise AppHttpError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )
    """

    def __init__(
        self,
        status_code=status.HTTP_400_BAD_REQUEST,
        detail: str = "Some error happened",
        headers: dict = None,
    ):
        super().__init__(status_code, detail, headers)


class AppValueError(ValueError):
    """Base exception for value validation errors.

    This class should be used as the base for all exceptions related to
    value validation, such as format errors, range errors, or type mismatches.

    Example:
        class EmailFormatError(AppValueError):
            pass
    """


class AppKeyError(KeyError):
    """Base exception for key-related errors.

    This class should be used as the base for all exceptions related to
    key operations, such as missing keys, duplicate keys, or invalid keys.

    Example:
        class DuplicateUserError(AppKeyError):
            pass
    """
