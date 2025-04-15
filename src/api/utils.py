"""Database and caching utility check endpoints.

This module provides health check endpoints to verify:
- Database connectivity and configuration
- Redis cache connectivity
- Overall application health status

These endpoints are useful for monitoring, deployment health checks,
and ensuring the application's core services are functioning properly.
"""

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
        500: {"model": HealthCheckErrorModel, "description": "Database or Redis connection error"},
    },
)
async def healthchecker(
    db: AsyncSession = Depends(get_db), redis: RedisSessionManager = Depends(get_redis)
):
    """Check health status of critical application services.

    Performs connectivity checks for both the database and Redis cache
    to verify that all core services are functioning properly. This is
    essential for monitoring application health in production.

    Args:
        db (AsyncSession): Database session for SQL connectivity check
        redis (RedisSessionManager): Redis connection manager for cache check

    Returns:
        HealthCheckModel: Success message if all checks pass

    Raises:
        DatabaseConfigError: If database query returns no result, indicating config issue
        DatabaseConnectionError: If database connection fails or throws error
        RedisConnectionError: If Redis connection fails or ping unsuccessful

    Note:
        - Executes a simple SELECT 1 query to verify database connectivity
        - Performs a Redis PING to verify cache connectivity
        - Useful for automated health monitoring and deployment checks
    """
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
