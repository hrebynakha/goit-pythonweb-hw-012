import json
from src.conf.config import settings
from redis import Redis


class RedisSessionManager:
    """Session manager"""

    def __init__(
        self,
    ):
        print(settings.REDIS_PASSWORD)
        self.__client = Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
        )

    def ping(self):
        """Ping redis"""
        return self.__client.ping()

    def get(self, key):
        value = self.__client.get(key)
        if value is None:
            return None
        return json.loads(value)

    def set(self, key, value, ex=None, px=None, nx=False, xx=False):
        return self.__client.set(key, json.dumps(value), ex=ex, px=px, nx=nx, xx=xx)


client = RedisSessionManager()


def get_redis():
    return client
