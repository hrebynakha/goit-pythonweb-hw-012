"""Database and caching utility exceptions.

This module defines exceptions for database and Redis operations including:
- Database configuration and connection errors
- Redis configuration and connection errors
- General database operation failures

All exceptions inherit from FastAPI's HTTPException to ensure proper
error response formatting in the API.
"""

from fastapi import HTTPException, status


class DatabaseException(HTTPException):
    """Base exception for database-related errors.

    This exception serves as the base for all database-related errors,
    providing consistent error handling and response formatting.

    Args:
        status_code (int, optional): HTTP status code. Defaults to 500.
        detail (str, optional): Error message. Defaults to "Database error".
        headers (dict, optional): Additional HTTP headers. Defaults to None.

    Example:
        raise DatabaseException(detail="Failed to execute database query")
    """

    def __init__(
        self,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail: str = "Database error",
        headers: dict = None,
    ):
        super().__init__(status_code, detail, headers)


class RedisException(HTTPException):
    """Base exception for Redis-related errors.

    This exception serves as the base for all Redis-related errors,
    providing consistent error handling for caching operations.

    Args:
        status_code (int, optional): HTTP status code. Defaults to 500.
        detail (str, optional): Error message. Defaults to "Redis error".
        headers (dict, optional): Additional HTTP headers. Defaults to None.

    Example:
        raise RedisException(detail="Failed to set cache key")
    """

    def __init__(
        self,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail: str = "Redis error",
        headers: dict = None,
    ):
        super().__init__(status_code, detail, headers)


class DatabaseConfigError(DatabaseException):
    """Exception for database configuration errors.

    This exception is raised when there are issues with database
    configuration, such as invalid connection strings or missing credentials.

    Args:
        detail (str, optional): Error message. Defaults to "Database is not configured correctly".
        **kwargs: Additional arguments passed to DatabaseException.

    Example:
        raise DatabaseConfigError("Invalid database URL in configuration")
    """

    def __init__(self, detail="Database is not configured correctly", **kwargs):
        super().__init__(detail=detail, **kwargs)


class DatabaseConnectionError(DatabaseException):
    """Exception for database connection failures.

    This exception is raised when the application fails to establish
    a connection with the database server.

    Args:
        detail (str, optional): Error message. Defaults to "Database connection error".
        **kwargs: Additional arguments passed to DatabaseException.

    Example:
        raise DatabaseConnectionError("Failed to connect to database server")
    """

    def __init__(self, detail="Database connection error", **kwargs):
        super().__init__(detail=detail, **kwargs)


class RedisConnectionError(RedisException):
    """Exception for Redis connection failures.

    This exception is raised when the application fails to establish
    a connection with the Redis server.

    Args:
        detail (str, optional): Error message. Defaults to "Redis connection error".
        **kwargs: Additional arguments passed to RedisException.

    Example:
        raise RedisConnectionError("Failed to connect to Redis server")
    """

    def __init__(self, detail="Redis connection error", **kwargs):
        super().__init__(detail=detail, **kwargs)
