from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt

from src.conf.config import settings
from src.database.db import get_db

from src.repository.users import UserRepository
from src.exceptions.auth import AuthError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(
    db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        username = payload.get("sub")
        if username is None:
            raise AuthError
    except JWTError as e:
        raise AuthError(detail=str(e)) from e

    user_repository = UserRepository(db)
    user = await user_repository.get_user_by_username(username)
    if user is None:
        raise AuthError

    if not user.is_verified:
        # return user  # uncomment for testing
        raise AuthError(detail="User not verified.")
    return user
