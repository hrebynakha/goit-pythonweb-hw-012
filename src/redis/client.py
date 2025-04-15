"""Redis client module for managing session data and caching.

This module provides a Redis client wrapper for handling session management and caching operations.
It includes automatic JSON serialization/deserialization of values and connection management.
"""

import json
from src.conf.config import settings
from redis import Redis


class RedisSessionManager:
    """Redis session manager for handling cached data with JSON serialization.

    This class provides a wrapper around Redis client with JSON serialization support.
    It automatically handles connection setup using configuration from settings.

    Attributes:
        __client (Redis): Internal Redis client instance
    """

    def __init__(
        self,
    ):
        """Initialize Redis connection using settings.

        Connects to Redis server using host, port, and password from application settings.
        """
        print(settings.REDIS_PASSWORD)
        self.__client = Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
        )

    def ping(self):
        """Test Redis server connection.

        Returns:
            bool: True if connection is alive, False otherwise
        """
        return self.__client.ping()

    def get(self, key):
        """Retrieve and deserialize JSON value from Redis.

        Args:
            key (str): Redis key to retrieve

        Returns:
            dict | None: Deserialized JSON data if key exists, None otherwise
        """
        value = self.__client.get(key)
        if value is None:
            return None
        return json.loads(value)

    def set(self, key, value, ex=None, px=None, nx=False, xx=False):
        """Store JSON serialized value in Redis.

        Args:
            key (str): Redis key to set
            value (Any): Value to serialize and store
            ex (int, optional): Expire time in seconds. Defaults to None
            px (int, optional): Expire time in milliseconds. Defaults to None
            nx (bool, optional): Only set if key doesn't exist. Defaults to False
            xx (bool, optional): Only set if key exists. Defaults to False

        Returns:
            bool: True if successful, False otherwise
        """
        return self.__client.set(key, json.dumps(value), ex=ex, px=px, nx=nx, xx=xx)


# Global Redis client instance
client = RedisSessionManager()


def get_redis():
    """Get the global Redis session manager instance.

    This function is designed to be used as a FastAPI dependency.

    Returns:
        RedisSessionManager: Global Redis session manager instance
    """
    return client
