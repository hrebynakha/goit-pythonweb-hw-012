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
    __version__: str = getattr(bcrypt, "__version__")


class Hash:
    setattr(bcrypt, "__about__", SolveBugBcryptWarning())

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        return self.pwd_context.hash(password)


class TokenService:

    def create_token(
        self,
        data: dict,
        expires_delta: timedelta,
        token_type: Literal["access", "refresh"],
    ) -> str:
        to_encode = data.copy()
        now = datetime.now(timezone.utc)
        expire = now + expires_delta
        to_encode.update({"exp": expire, "iat": now, "token_type": token_type})
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def create_email_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=7)
        to_encode.update({"iat": datetime.now(timezone.utc), "exp": expire})
        token = jwt.encode(
            to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
        )
        return token

    async def get_email_from_token(self, token: str) -> str | None:
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
        if expires_delta:
            return self.create_token(data, expires_delta, "refresh")
        return self.create_token(
            data,
            timedelta(minutes=settings.REFRESH_JWT_EXPIRATION_SECONDS),
            "refresh",
        )


class AuthService(TokenService):
    def __init__(self, db: AsyncSession):

        self.user_repository = UserRepository(db)

    async def verify_refresh_token(
        self,
        refresh_token: str,
    ) -> User | None:
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

    async def geneate_jwt(self, username: str) -> dict:
        access_token = await self.create_access_token(data={"sub": username})
        refresh_token = await self.create_refresh_token(data={"sub": username})
        await self.user_repository.update_user_refresh_token(username, refresh_token)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    async def update_jwt(self, username: str, refresh_token: str) -> dict:
        access_token = await self.create_access_token(data={"sub": username})
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }
