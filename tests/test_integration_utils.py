# test_integration_utils.py - Integration tests for utility functions and error handling

# pylint: disable=redefined-outer-name, unused-argument

import pytest
from src.exceptions.utils import (
    DatabaseConfigError,
    DatabaseConnectionError,
    RedisConnectionError,
)
from src.app import app
from src.database.db import get_db
from src.database.redis.client import get_redis


@pytest.fixture
def override_db_down_bad_config():
    def broken_db():
        raise DatabaseConfigError

    app.dependency_overrides[get_db] = broken_db
    yield
    app.dependency_overrides.pop(get_db, None)


@pytest.fixture
def override_db_down_bad_connection():
    def broken_db():
        raise DatabaseConnectionError

    app.dependency_overrides[get_db] = broken_db
    yield
    app.dependency_overrides.pop(get_db, None)


@pytest.fixture
def override_redis_down():
    def broken_redis():
        raise RedisConnectionError

    app.dependency_overrides[get_redis] = broken_redis
    yield
    app.dependency_overrides.pop(get_db, None)


def test_health_check(
    client,
):
    response = client.get(
        "api/healthchecker",
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["message"] == "Welcome to FastAPI!"


def test_health_check_db_down(client, override_db_down_bad_connection):
    response = client.get(
        "api/healthchecker",
    )
    assert response.status_code == 500, response.text
    data = response.json()
    assert data["detail"] == "Database connection error"


def test_health_check_redis_down(client, override_redis_down):
    response = client.get(
        "api/healthchecker",
    )
    assert response.status_code == 500, response.text
    data = response.json()
    assert data["detail"] == "Redis connection error"


def test_health_check_redis_and_db_down(
    client, override_redis_down, override_db_down_bad_connection
):
    response = client.get(
        "api/healthchecker",
    )
    assert response.status_code == 500, response.text
    data = response.json()
    assert data["detail"] == "Database connection error"


def test_health_check_db_down_config(client, override_db_down_bad_config):
    response = client.get(
        "api/healthchecker",
    )
    assert response.status_code == 500, response.text
    data = response.json()
    assert data["detail"] == "Database is not configured correctly"
