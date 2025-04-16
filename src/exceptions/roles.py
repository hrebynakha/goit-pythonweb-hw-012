from fastapi import status
from src.exceptions.core import AppHttpError


class AccessDeniedError(AppHttpError):
    """Exception raised for general authentication errors.

    This exception is used when authentication fails due to invalid or expired
    credentials, missing tokens, or other authentication-related issues.

    Args:
        status_code (int, optional): HTTP status code. Defaults to 403.
        detail (str, optional): Error message. Defaults to "Access denied".

    Note:
        Automatically adds WWW-Authenticate: Bearer header as per RFC 6750.
    """

    def __init__(
        self,
        status_code=status.HTTP_403_FORBIDDEN,
        detail: str = "Access denied",
    ):
        super().__init__(status_code, detail, {"WWW-Authenticate": "Bearer"})
