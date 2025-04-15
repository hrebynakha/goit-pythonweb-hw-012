"""File storage exception classes.

This module defines exceptions specific to file storage operations,
particularly for handling file upload failures through services
like Cloudinary.
"""

from fastapi import status
from src.exceptions.core import AppHttpError


class FileUploadError(AppHttpError):
    """Exception raised when file upload operations fail.

    This exception is used when a file upload fails due to:
    - Network errors
    - Invalid file types
    - File size limits
    - Storage service errors
    - Other upload-related issues

    Args:
        status_code (int, optional): HTTP status code. Defaults to 400.
        detail (str, optional): Error message. Defaults to "File not uploaded successfully".
        headers (dict, optional): Additional HTTP headers. Defaults to None.

    Example:
        raise FileUploadError(
            detail="File size exceeds maximum allowed limit"
        )
    """

    def __init__(
        self,
        status_code=status.HTTP_400_BAD_REQUEST,
        detail: str = "File not uploaded successfully",
        headers: dict = None,
    ):
        super().__init__(status_code, detail, headers)
