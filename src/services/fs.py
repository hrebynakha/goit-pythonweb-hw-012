"""File storage service using Cloudinary.

This module provides file upload functionality using Cloudinary as the storage backend.
It handles:
- Image upload and transformation
- URL generation for uploaded files
- Error handling and logging
- Cloudinary configuration management
"""

import logging
import cloudinary
import cloudinary.uploader
from cloudinary.exceptions import Error as CloudinaryError

from src.conf.config import settings


class UploadFileService:
    """Service for managing file uploads to Cloudinary.

    This service handles file uploads to Cloudinary, particularly focused on
    avatar image uploads. It provides automatic image transformation and
    URL generation.

    Attributes:
        cloud_name (str): Cloudinary cloud name from settings
        api_key (str): Cloudinary API key from settings
        api_secret (str): Cloudinary API secret from settings
    """

    def __init__(
        self,
        cloud_name: str = settings.CLOUDINARY_NAME,
        api_key: str = settings.CLOUDINARY_API_KEY,
        api_secret: str = settings.CLOUDINARY_API_SECRET,
    ):
        """Initialize Cloudinary configuration.

        Args:
            cloud_name (str): Cloudinary cloud name. Defaults to settings value.
            api_key (str): Cloudinary API key. Defaults to settings value.
            api_secret (str): Cloudinary API secret. Defaults to settings value.

        Note:
            The service will use environment variables from settings by default,
            but allows override for testing or multi-tenant scenarios.
        """
        self.cloud_name = cloud_name
        self.api_key = api_key
        self.api_secret = api_secret
        cloudinary.config(
            cloud_name=self.cloud_name,
            api_key=self.api_key,
            api_secret=self.api_secret,
            secure=True,
        )

    @staticmethod
    def upload_file(file, username) -> str | None:
        """Upload a file to Cloudinary and return its URL.

        This method:
        1. Uploads the file to Cloudinary under the RestApp folder
        2. Transforms the image to 250x250 pixels with crop
        3. Returns a secure URL to the transformed image

        Args:
            file: File-like object containing the image
            username (str): Username to use in the public_id

        Returns:
            str | None: URL to the uploaded and transformed image,
                       or None if upload fails

        Note:
            - Files are stored under the 'RestApp/{username}' path
            - Existing files with the same name are overwritten
            - Images are automatically transformed to 250x250 pixels
        """
        public_id = f"RestApp/{username}"
        try:
            r = cloudinary.uploader.upload(
                file.file, public_id=public_id, overwrite=True
            )
            src_url = cloudinary.CloudinaryImage(public_id).build_url(
                width=250, height=250, crop="fill", version=r.get("version")
            )
            return src_url
        except CloudinaryError as e:
            logging.error("Cannot upload file to Cloudinary error:%s", e)
            return None
