"""Main app exceptions"""

from fastapi import HTTPException, status


class AppHttpError(HTTPException):
    """Main class for application error"""

    def __init__(
        self,
        status_code=status.HTTP_400_BAD_REQUEST,
        detail: str = "Some error happend",
        headers: dict = None,
    ):

        super().__init__(status_code, detail, headers)


class AppValueError(ValueError):
    """Base appliaction value error"""


class AppKeyError(KeyError):
    """Base application key error"""
