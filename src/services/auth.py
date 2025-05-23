"""Authentication service module for handling password hashing and JWT token operations.

This module provides services for:
- Password hashing and verification using bcrypt
- JWT token generation and validation for authentication
- Email verification token handling
- User authentication and token refresh operations
"""

from datetime import datetime, timedelta, timezone
from dataclasses import dataclass
from typing import Optional, Literal


import bcrypt
from passlib.context import CryptContext
from jose import JWTError, jwt

from sqlalchemy.ext.asyncio import AsyncSession


from src.conf.config import settings
from src.repository.users import UserRepository
from src.schemas.users import User


# tmp fix for   https://github.com/pyca/bcrypt/issues/684
@dataclass
class SolveBugBcryptWarning:
    """Temporary fix for bcrypt warning issue #684.

    See: https://github.com/pyca/bcrypt/issues/684
    """

    __version__: str = getattr(bcrypt, "__version__")


class Hash:
    """Password hashing service using bcrypt."""

    setattr(bcrypt, "__about__", SolveBugBcryptWarning())

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password, hashed_password) -> bool:
        """Verify a password against its hash.

        Args:
            plain_password: The plain text password to verify
            hashed_password: The hashed password to verify against

        Returns:
            bool: True if password matches, False otherwise
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """Generate a password hash.

        Args:
            password (str): Plain text password to hash

        Returns:
            str: Bcrypt hash of the password
        """
        return self.pwd_context.hash(password)


class TokenService:
    """Service for JWT token operations including creation and validation."""

    def create_token(
        self,
        data: dict,
        expires_delta: timedelta,
        token_type: Literal["access", "refresh"],
    ) -> str:
        """Create a JWT token with specified type and expiration.

        Args:
            data (dict): Payload data for the token
            expires_delta (timedelta): Token expiration time
            token_type (Literal["access", "refresh"]): Type of token to create

        Returns:
            str: Encoded JWT token
        """
        to_encode = data.copy()
        now = datetime.now(timezone.utc)
        expire = now + expires_delta
        to_encode.update({"exp": expire, "iat": now, "token_type": token_type})
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def create_email_token(self, data: dict) -> str:
        """Create a JWT token for email verification.

        Args:
            data (dict): Email data to encode in token

        Returns:
            str: Encoded JWT token valid for 7 days
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=7)
        to_encode.update({"iat": datetime.now(timezone.utc), "exp": expire})
        token = jwt.encode(
            to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
        )
        return token

    def create_reset_password_token(self, data: dict) -> str:
        """Create a JWT token for reset password verification.

        Args:
            data (dict): Email data to encode in token

        Returns:
            str: Encoded JWT token valid for 15 minutes
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"iat": datetime.now(timezone.utc), "exp": expire})
        token = jwt.encode(
            to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
        )
        return token

    async def get_email_from_token(self, token: str) -> str | None:
        """Extract email from a verification token.

        Args:
            token (str): JWT token containing email

        Returns:
            str | None: Email if token is valid, None otherwise
        """
        try:
            payload = jwt.decode(
                token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
            )
            email = payload.get("sub")
            return email
        except JWTError:
            return None

    async def create_access_token(
        self, data: dict, expires_delta: Optional[float] = None
    ) -> str:
        """Create a JWT access token.

        Args:
            data (dict): Payload data for the token
            expires_delta (Optional[float], optional): Custom expiration time in seconds

        Returns:
            str: Encoded JWT access token
        """
        if expires_delta:
            return self.create_token(data, expires_delta, "access")

        return self.create_token(
            data,
            timedelta(minutes=settings.ACCESS_JWT_EXPIRATION_SECONDS),
            "access",
        )

    async def create_refresh_token(
        self, data: dict, expires_delta: Optional[float] = None
    ) -> str:
        """Create a JWT refresh token.

        Args:
            data (dict): Payload data for the token
            expires_delta (Optional[float], optional): Custom expiration time in seconds

        Returns:
            str: Encoded JWT refresh token
        """
        if expires_delta:
            return self.create_token(data, expires_delta, "refresh")
        return self.create_token(
            data,
            timedelta(minutes=settings.REFRESH_JWT_EXPIRATION_SECONDS),
            "refresh",
        )


class AuthService(TokenService):
    """Authentication service handling user authentication and token management."""

    def __init__(self, db: AsyncSession):
        """Initialize auth service with database session.

        Args:
            db (AsyncSession): SQLAlchemy async database session
        """
        self.user_repository = UserRepository(db)

    async def verify_refresh_token(
        self,
        refresh_token: str,
    ) -> User | None:
        """Verify a refresh token and return associated user.

        Args:
            refresh_token (str): JWT refresh token to verify

        Returns:
            User | None: User if token is valid and matches stored token, None otherwise
        """
        try:
            payload = jwt.decode(
                refresh_token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
            )
            username: str = payload.get("sub")
            token_type: str = payload.get("token_type")
            if username is None or token_type != "refresh":
                return None
            return await self.user_repository.get_user_by_username_and_token(
                username, refresh_token
            )
        except JWTError:
            return None

    async def generate_jwt(self, username: str) -> dict:
        """Generate new access and refresh tokens for a user.

        Args:
            username (str): Username to generate tokens for

        Returns:
            dict: Dictionary containing access_token, refresh_token, and token_type
        """
        access_token = await self.create_access_token(data={"sub": username})
        refresh_token = await self.create_refresh_token(data={"sub": username})
        await self.user_repository.update_user_refresh_token(username, refresh_token)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    async def update_jwt(self, username: str, refresh_token: str) -> dict:
        """Update access token using existing refresh token.

        Args:
            username (str): Username to update token for
            refresh_token (str): Existing valid refresh token

        Returns:
            dict: Dictionary containing new access_token, existing refresh_token, and token_type
        """
        access_token = await self.create_access_token(data={"sub": username})
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }
