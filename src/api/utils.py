"""Utils api view"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from src.database.db import get_db
from src.schemas.utils import HealthCheckModel, HealthCheckErrorModel
from src.exceptions.utils import (
    DatabaseConfigError,
    DatabaseConnectionError,
    RedisConnectionError,
)
from src.redis.client import get_redis, RedisSessionManager

router = APIRouter(tags=["utils"])


@router.get(
    "/healthchecker",
    response_model=HealthCheckModel,
    responses={
        500: {"model": HealthCheckErrorModel, "description": "Database error"},
    },
)
async def healthchecker(
    db: AsyncSession = Depends(get_db), redis: RedisSessionManager = Depends(get_redis)
):
    """Health check"""
    try:
        result = await db.execute(text("SELECT 1"))
        result = result.scalar_one_or_none()

        if result is None:
            raise DatabaseConfigError
    except Exception as e:
        raise DatabaseConnectionError from e

    try:
        redis.ping()
    except Exception as e:
        raise RedisConnectionError from e
    return {"message": "Welcome to FastAPI!"}
