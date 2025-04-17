from unittest.mock import AsyncMock
import pytest
from sqlalchemy import select

from tests.conftest import TestingSessionLocal
from src.models.users import User
from src.services.email import EmailService
from src.services.auth import TokenService

user_data = {
    "username": "not_real_user",
    "email": "not_real_email@gmail.com",
    "password": "not_real_password",
}

VERIFY_TOKEN = TokenService().create_email_token({"sub": user_data["email"]})


def test_signup(client, monkeypatch):
    mock_send_email = AsyncMock()
    monkeypatch.setattr(EmailService, "send_email", mock_send_email)
    response = client.post("api/auth/register", json=user_data)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]
    assert "hashed_password" not in data
    assert "avatar" in data


def test_repeat_signup(client, monkeypatch):
    mock_send_email = AsyncMock()
    monkeypatch.setattr(EmailService, "send_email", mock_send_email)
    response = client.post("api/auth/register", json=user_data)
    assert response.status_code == 409, response.text
    data = response.json()
    assert data["detail"] == "User with this email already exist"


def test_repeat_signup_with_different_email(client, monkeypatch):
    mock_send_email = AsyncMock()
    monkeypatch.setattr(EmailService, "send_email", mock_send_email)
    user_data_ = user_data.copy()
    user_data_["email"] = "not_real_email2@gmail.com"
    response = client.post("api/auth/register", json=user_data_)
    assert response.status_code == 409, response.text
    data = response.json()
    assert data["detail"] == "User with this username already exists"


def test_not_confirmed_login(client):
    response = client.post(
        "api/auth/login",
        data={
            "username": user_data.get("username"),
            "password": user_data.get("password"),
        },
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "User is not verified"


@pytest.mark.asyncio
async def test_login(client):
    async with TestingSessionLocal() as session:
        current_user = await session.execute(
            select(User).where(User.email == user_data.get("email"))
        )
        current_user = current_user.scalar_one_or_none()
        if current_user:
            current_user.is_verified = True
            await session.commit()

    response = client.post(
        "api/auth/login",
        data={
            "username": user_data.get("username"),
            "password": user_data.get("password"),
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data


def test_wrong_password_login(client):
    response = client.post(
        "api/auth/login",
        data={"username": user_data.get("username"), "password": "password"},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "User or password is incorrect"


def test_wrong_username_login(client):
    response = client.post(
        "api/auth/login",
        data={"username": "username", "password": user_data.get("password")},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "User or password is incorrect"


def test_validation_error_login(client):
    response = client.post(
        "api/auth/login", data={"password": user_data.get("password")}
    )
    assert response.status_code == 422, response.text
    data = response.json()
    assert "detail" in data


@pytest.mark.asyncio
async def test_reset_password_request(client, monkeypatch):
    async with TestingSessionLocal() as session:
        current_user = await session.execute(
            select(User).where(User.email == user_data.get("email"))
        )
        current_user = current_user.scalar_one_or_none()
        if current_user:
            current_user.is_verified = True
            await session.commit()
    assert current_user.is_verified is True
    mock_send_email = AsyncMock()
    monkeypatch.setattr(EmailService, "send_email", mock_send_email)
    response = client.post(
        "api/auth/reset-password", json={"email": user_data["email"]}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["message"] == "If the email exists, a reset link was sent."


def test_reset_password_request_no_exist_email(client, monkeypatch):
    mock_send_email = AsyncMock()
    monkeypatch.setattr(EmailService, "send_email", mock_send_email)
    response = client.post(
        "api/auth/reset-password", json={"email": "random_not_exist_email@gmail.com"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["message"] == "If the email exists, a reset link was sent."


@pytest.mark.asyncio
async def test_reset_password_request_not_verified(client, monkeypatch):
    async with TestingSessionLocal() as session:
        current_user = await session.execute(
            select(User).where(User.email == user_data.get("email"))
        )
        current_user = current_user.scalar_one_or_none()
        if current_user:
            current_user.is_verified = False
            await session.commit()
    assert current_user.is_verified is False
    mock_send_email = AsyncMock()
    monkeypatch.setattr(EmailService, "send_email", mock_send_email)
    response = client.post(
        "api/auth/reset-password", json={"email": user_data["email"]}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["message"] == "If the email exists, a reset link was sent."


def test_set_password_invalid_form_request(
    client,
):
    response = client.post(
        "/api/auth/set-password",
        json={
            "token": VERIFY_TOKEN,
            "password": "new_password",
            "confirm_password": "new_password",
        },
    )
    assert response.status_code == 422, response.text
    data = response.json()
    assert "detail" in data


def test_set_password_invalid_token(
    client,
):
    response = client.post(
        "/api/auth/set-password",
        data={
            "token": "1234567890",
            "password": "new_password",
            "confirm_password": "new_password",
        },
    )
    assert response.status_code == 422, response.text
    data = response.json()
    assert data["detail"] == "Invalid reset password token"


def test_set_password_invalid_sub(
    client,
):
    token = TokenService().create_email_token(
        {"sub": "test_not_valid_email@example.com"}
    )
    response = client.post(
        "/api/auth/set-password",
        data={
            "token": token,
            "password": "new_password",
            "confirm_password": "new_password",
        },
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Verification error"


def test_set_password_not_match(
    client,
):
    response = client.post(
        "/api/auth/set-password",
        data={
            "token": VERIFY_TOKEN,
            "password": "new_password",
            "confirm_password": "new_password2",
        },
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Passwords do not match"


def test_set_password(
    client,
):
    response = client.post(
        "/api/auth/set-password",
        data={
            "token": VERIFY_TOKEN,
            "password": "new_password",
            "confirm_password": "new_password",
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["message"] == "Password successfully updated"


@pytest.mark.asyncio
async def test_confirm_email_invalid_token(client):
    response = client.get("/api/auth/confirmed_email/12234")
    assert response.status_code == 422, response.text
    data = response.json()
    assert data["detail"] == "Invalid email verification token"


@pytest.mark.asyncio
async def test_confirm_email_valid_token_not_valid_user(client):
    token = TokenService().create_email_token(
        {"sub": "test_not_valid_email@example.com"}
    )
    response = client.get(f"/api/auth/confirmed_email/{token}")
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Verification error"


@pytest.mark.asyncio
async def test_confirm_email(client):
    async def get_user(set_not_verified: bool = False):
        async with TestingSessionLocal() as session:
            current_user = await session.execute(
                select(User).where(User.email == user_data.get("email"))
            )
            current_user = current_user.scalar_one_or_none()
            if set_not_verified is True:
                current_user.is_verified = False
                await session.commit()
        return current_user

    current_user = await get_user(True)
    assert current_user.is_verified is False

    response = client.get(f"/api/auth/confirmed_email/{VERIFY_TOKEN}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["message"] == "Email verified successfully"

    current_user = await get_user()
    assert current_user.is_verified is True


@pytest.mark.asyncio
async def test_reconfirm_email(client):
    response = client.get(f"/api/auth/confirmed_email/{VERIFY_TOKEN}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["message"] == "Your email has already been confirmed."
