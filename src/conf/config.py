"""Configuration app file"""

from pydantic_settings import BaseSettings
from pydantic import ConfigDict, EmailStr


class Settings(BaseSettings):
    """Class for keeping app settings and environment configuration."""

    DEBUG: bool
    DB_URL: str
    ALLOWED_CORS: list[str]

    MAIL_USERNAME: EmailStr = "example@meta.ua"
    MAIL_PASSWORD: str = "secretPassword"
    MAIL_FROM: EmailStr = "example@meta.ua"
    MAIL_PORT: int = 465
    MAIL_SERVER: str = "smtp.meta.ua"
    MAIL_FROM_NAME: str = "Rest API Service"
    MAIL_STARTTLS: bool = False
    MAIL_SSL_TLS: bool = True
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

    CLOUDINARY_NAME: str
    CLOUDINARY_API_KEY: int = 123456789
    CLOUDINARY_API_SECRET: str = "secret"

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_JWT_EXPIRATION_SECONDS: int = 900  # 15 min
    REFRESH_JWT_EXPIRATION_SECONDS: int = 604800  # 7 days

    model_config = ConfigDict(
        extra="ignore", env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )


settings = Settings()
