import logging
import cloudinary
import cloudinary.uploader
from cloudinary.exceptions import Error as CloudinaryError

from src.conf.config import settings


class UploadFileService:

    def __init__(
        self,
        cloud_name: str = settings.CLOUDINARY_NAME,
        api_key: str = settings.CLOUDINARY_API_KEY,
        api_secret: str = settings.CLOUDINARY_API_SECRET,
    ):
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
