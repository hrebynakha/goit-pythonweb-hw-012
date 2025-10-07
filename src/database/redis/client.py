"""Redis client module for managing session data and caching.

This module provides a Redis client wrapper for handling session management and caching operations.
It includes automatic JSON serialization/deserialization of values and connection management.
"""

import json
import redis.asyncio as redis


from src.conf.config import settings


class AsyncRedisSessionManager:
    """Async Redis session manager for handling cached data with JSON serialization."""

    def __init__(self):
        self.__client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            decode_responses=True,  # Ensures Redis returns strings instead of bytes
        )

    async def ping(self) -> bool:
        """Test Redis server connection."""
        return await self.__client.ping()

    async def get(self, key: str):
        """Retrieve and deserialize JSON value from Redis."""
        value = await self.__client.get(key)
        if value is None:
            return None
        return json.loads(value)

    async def set(self, key: str, value, *args, **kwargs):
        """Store JSON serialized value in Redis."""
        return await self.__client.set(key, json.dumps(value), *args, **kwargs)


# Global async Redis client instance
client = AsyncRedisSessionManager()


async def get_redis():
    """Get the global Redis session manager instance (for FastAPI Depends)."""
    if settings.USE_REDIS is False:
        return None
    return client
