import asyncio

import pytest
import pytest_asyncio
import fakeredis.aioredis
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.models.users import User
from src.database.basic import Base
from src.database.db import get_db
from src.services.auth import Hash, TokenService
from src.app import app
from src.database.redis.client import AsyncRedisSessionManager, get_redis

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, expire_on_commit=False, bind=engine
)

test_user = {
    "username": "test",
    "email": "test@example.com",
    "avatar": "<https://test.com/gravatar>",
    "is_verified": True,
}
test_admin_user = {
    "username": "test_admin",
    "email": "test_admin@example.com",
    "avatar": "<https://test.com/gravatar>",
    "role": "admin",
    "is_verified": True,
}
TEST_PASSWORD = "1234test"


class FakeAasyncRedisManager(AsyncRedisSessionManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._AsyncRedisSessionManager__client = None  # pylint: disable=invalid-name

    async def init(self):
        self._AsyncRedisSessionManager__client = (
            await fakeredis.aioredis.FakeRedis()
        )  # pylint: disable=invalid-name
        return self


@pytest.fixture(scope="module", autouse=True)
def init_models_wrap():
    async def init_models():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        async with TestingSessionLocal() as session:
            hash_password = Hash().get_password_hash(TEST_PASSWORD)
            current_user = User(
                **test_user,
                hashed_password=hash_password,
            )
            admin_user = User(
                **test_admin_user,
                hashed_password=hash_password,
            )
            session.add(current_user)
            session.add(admin_user)
            await session.commit()

    asyncio.run(init_models())


@pytest.fixture(scope="module")
def client():
    # Dependency override

    async def override_get_db():
        async with TestingSessionLocal() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise  # pylint: disable=broad-exception-raised

    async def override_get_redis():
        return await FakeAasyncRedisManager().init()

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_redis] = override_get_redis

    yield TestClient(app)


@pytest_asyncio.fixture()
async def get_token():
    token = await TokenService().create_access_token(
        data={"sub": test_user["username"]}
    )
    return token


@pytest_asyncio.fixture()
async def get_admin_token():
    token = await TokenService().create_access_token(
        data={"sub": test_admin_user["username"]}
    )
    return token
