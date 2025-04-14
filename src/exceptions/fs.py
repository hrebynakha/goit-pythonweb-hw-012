from fastapi import status
from src.exceptions.core import AppHttpError


class FileUploadError(AppHttpError):
    def __init__(
        self,
        status_code=status.HTTP_400_BAD_REQUEST,
        detail: str = "File not uploaded successfuly",
        headers: dict = None,
    ):
        super().__init__(status_code, detail, headers)
