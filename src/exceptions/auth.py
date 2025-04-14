from fastapi import status
from src.exceptions.core import AppHttpError


class AuthError(AppHttpError):
    def __init__(
        self,
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail: str = "Could not validate credentials",
    ):
        super().__init__(status_code, detail, {"WWW-Authenticate": "Bearer"})


class RegistrationError(AppHttpError):
    def __init__(
        self,
        status_code=status.HTTP_409_CONFLICT,
        detail: str = "User with this username alredy exist",
        headers: dict = None,
    ):
        super().__init__(status_code, detail, headers)


class InvalidVerificationTokenError(AppHttpError):
    def __init__(
        self,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail: str = "Invalid email verification token",
        headers: dict = None,
    ):
        super().__init__(status_code, detail, headers)


class VerificationError(AppHttpError):
    def __init__(
        self,
        status_code=status.HTTP_400_BAD_REQUEST,
        detail: str = "Verification error",
        headers: dict = None,
    ):
        super().__init__(status_code, detail, headers)
