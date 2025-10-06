"""Application configuration management.

This module defines the application's configuration using Pydantic settings management.
It handles:
- Environment variable loading
- Configuration validation
- Default values
- Type checking

Configuration is loaded from environment variables and .env files, with
validation performed at startup to ensure all required values are present.
"""

from pydantic_settings import BaseSettings
from pydantic import ConfigDict, EmailStr


class Settings(BaseSettings):
    """Application configuration settings.

    This class defines all configuration settings for the application,
    including database connections, external services, and security settings.

    Settings are loaded from environment variables or .env file with
    validation performed on all values. Required fields must be set
    in the environment or .env file.

    Attributes:
        DEBUG (bool): Debug mode flag
        DB_URL (str): Database connection URL
        ALLOWED_CORS (list[str]): List of allowed CORS origins

        # Redis Configuration
        REDIS_HOST (str): Redis server hostname, defaults to "localhost"
        REDIS_PORT (int): Redis server port, defaults to 6379
        REDIS_PASSWORD (str | None): Optional Redis password

        # Email Configuration
        MAIL_USERNAME (EmailStr): SMTP username
        MAIL_PASSWORD (str): SMTP password
        MAIL_FROM (EmailStr): Sender email address
        MAIL_PORT (int): SMTP port, defaults to 465
        MAIL_SERVER (str): SMTP server hostname
        MAIL_FROM_NAME (str): Sender name
        MAIL_STARTTLS (bool): Enable STARTTLS, defaults to False
        MAIL_SSL_TLS (bool): Enable SSL/TLS, defaults to True
        USE_CREDENTIALS (bool): Use SMTP authentication, defaults to True
        VALIDATE_CERTS (bool): Validate SSL certificates, defaults to True

        # Cloudinary Configuration
        CLOUDINARY_NAME (str): Cloudinary cloud name
        CLOUDINARY_API_KEY (int): Cloudinary API key
        CLOUDINARY_API_SECRET (str): Cloudinary API secret

        # JWT Configuration
        JWT_SECRET (str): Secret key for JWT signing
        JWT_ALGORITHM (str): JWT signing algorithm, defaults to "HS256"
        ACCESS_JWT_EXPIRATION_SECONDS (int): Access token lifetime in seconds
        REFRESH_JWT_EXPIRATION_SECONDS (int): Refresh token lifetime in seconds

    Note:
        - All required fields must be set in environment variables or .env file
        - The .env file is automatically loaded if present
        - Case sensitivity is enforced for all settings
        - Unknown fields in .env file are ignored
    """

    # Core Settings
    DEBUG: bool = False
    DB_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/contacts_app"
    ALLOWED_CORS: list[str] = ["*"]

    # Redis Configuration
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str | None = None

    # Email Configuration
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

    # Cloudinary Configuration
    CLOUDINARY_NAME: str = "cloudinary"
    CLOUDINARY_API_KEY: int = 123456789
    CLOUDINARY_API_SECRET: str = "secret"

    # JWT Configuration
    JWT_SECRET: str = "secret"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_JWT_EXPIRATION_SECONDS: int = 900  # 15 min
    REFRESH_JWT_EXPIRATION_SECONDS: int = 604800  # 7 days

    # Optional configuration

    TITLE: str = "UContacts REST API Service"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = """
    UContacts is a secure REST API for managing personal and business contacts.
    Features include JWT authentication, role-based access, advanced filtering, and more.
    """

    CONTACT: dict[str, str] = {
        "name": "Hrebynakha Anatolii",
        "url": "https://github.com/hrebynakha/goit-pythonweb-hw-012",
        "email": "hrebynakha@gmail.com",
    }
    LICENSE_INFO: dict[str, str] = {
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    }

    model_config = ConfigDict(
        extra="ignore", env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )


settings = Settings()
