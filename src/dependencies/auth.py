from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt

from src.conf.config import settings
from src.database.db import get_db

from src.repository.users import UserRepository
from src.exceptions.auth import AuthError
from src.models.users import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_auth_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> User:
    """Authenticate and retrieve the current user from JWT token with Redis caching.

    This function performs the following steps:
    1. Checks Redis cache for user data using the token as key
    2. If not in cache, decodes and validates the JWT token
    3. Retrieves user from database using the username from token
    4. Validates user verification status
    5. Caches user data in Redis for future requests

    Args:
        background_tasks (BackgroundTasks): FastAPI background tasks for async Redis caching
        db (AsyncSession): Database session for user lookup. Defaults to Depends(get_db)
        token (str): JWT authentication token. Defaults to Depends(oauth2_scheme)
        redis (RedisSessionManager): Redis connection manager. Defaults to Depends(get_redis)

    Returns:
        User: Authenticated user object

    Raises:
        AuthError: In the following cases:
            - Invalid/expired JWT token
            - Missing username in token payload
            - User not found in database
            - User email not verified
    """
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
