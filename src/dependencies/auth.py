from fastapi import Depends, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt

from src.conf.config import settings
from src.database.db import get_db

from src.repository.users import UserRepository
from src.exceptions.auth import AuthError
from src.redis.client import get_redis, RedisSessionManager
from src.models.users import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme),
    redis: RedisSessionManager = Depends(get_redis),
):
    cached_item = redis.get(f"user_{token}")
    if cached_item:
        return User(**cached_item)

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
    background_tasks.add_task(
        redis.set,
        f"user_{token}",
        jsonable_encoder(user),
        ex=settings.ACCESS_JWT_EXPIRATION_SECONDS,
    )
    return user
