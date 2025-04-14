"""Utils exception"""

from fastapi import HTTPException, status


class DatabaseException(HTTPException):
    """DB configuration error"""

    def __init__(
        self,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail: str = "Database error",
        headers: dict = None,
    ):

        super().__init__(status_code, detail, headers)


class DatabaseConfigError(DatabaseException):
    """Database configuration error"""

    def __init__(self, detail="Database is not configured correctly", **kwargs):
        super().__init__(detail=detail, **kwargs)


class DatabaseConnectionError(DatabaseException):
    """Database connection error"""

    def __init__(self, detail="Database connection error", **kwargs):
        super().__init__(detail=detail, **kwargs)
