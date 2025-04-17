# pylint: disable=redefined-outer-name

from unittest.mock import AsyncMock, MagicMock
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users import User

# from src.models.contacts import Contact
# from src.repository.contacts import ContactRepository
# from src.schemas.contacts import ContactModel
from src.repository.users import UserRepository
from src.schemas.users import UserCreate


@pytest.fixture
def mock_session():
    mock_session = AsyncMock(spec=AsyncSession)
    return mock_session


@pytest.fixture
def user_repository(mock_session):
    return UserRepository(mock_session)


@pytest.fixture
def user():
    return User(
        id=1,
        username="testuser",
        email="testuser@example.com",
        refresh_token="testtoken",
        is_verified=False,
        avatar="testavatar",
        hashed_password="testpassword",
    )


@pytest.mark.asyncio
async def test_get_user_by_id(user_repository, mock_session, user):
    # Setup mock
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = user
    mock_session.execute = AsyncMock(return_value=mock_result)

    # Call method
    result = await user_repository.get_user_by_id(user_id=user.id)

    # Assertions
    assert result is not None
    assert result.id == user.id
    assert result.username == user.username
    assert result.email == user.email


@pytest.mark.asyncio
async def test_get_user_by_username(user_repository, mock_session, user):
    # Setup mock
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = user
    mock_session.execute = AsyncMock(return_value=mock_result)

    # Call method
    result = await user_repository.get_user_by_username(username=user.username)

    # Assertions
    assert result is not None
    assert result.id == user.id
    assert result.username == user.username
    assert result.email == user.email


@pytest.mark.asyncio
async def test_get_user_by_email(user_repository, mock_session, user):
    # Setup mock
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = user
    mock_session.execute = AsyncMock(return_value=mock_result)

    # Call method
    result = await user_repository.get_user_by_email(email=user.email)

    # Assertions
    assert result is not None
    assert result.id == user.id
    assert result.username == user.username
    assert result.email == user.email


@pytest.mark.asyncio
async def test_get_user_by_username_and_token(user_repository, mock_session, user):
    # Setup mock
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = user
    mock_session.execute = AsyncMock(return_value=mock_result)

    # Call method
    result = await user_repository.get_user_by_username_and_token(
        username=user.username, token=user.refresh_token
    )

    # Assertions
    assert result is not None
    assert result.id == user.id
    assert result.username == user.username
    assert result.email == user.email


@pytest.mark.asyncio
async def test_create_user(user_repository, mock_session):
    result = await user_repository.create_user(
        body=UserCreate(
            username="testuser", email="testuser@example.com", password="password"
        )
    )

    # Assertions
    assert isinstance(result, User)
    assert result.username == "testuser"
    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once_with(result)


@pytest.mark.asyncio
async def test_update_user_refresh_token(user_repository, mock_session, user):
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = user
    mock_session.execute = AsyncMock(return_value=mock_result)

    # Call method
    result = await user_repository.update_user_refresh_token(
        username=user.username, token="newtoken"
    )
    assert result is not None
    assert result.refresh_token == "newtoken"


@pytest.mark.asyncio
async def test_user_set_email_verified(user_repository, mock_session, user):
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = user
    mock_session.execute = AsyncMock(return_value=mock_result)

    # Call method
    result = await user_repository.confirmed_email(email=user.email)
    assert result is None
    assert user.is_verified is True
    mock_session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_user_set_new_avatar(user_repository, mock_session, user):
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = user
    mock_session.execute = AsyncMock(return_value=mock_result)

    # Call method
    result = await user_repository.update_avatar_url(email=user.email, url="newurl")
    assert result is not None
    assert user.avatar == "newurl"


@pytest.mark.asyncio
async def test_user_set_new_password(user_repository, mock_session, user):
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = user
    mock_session.execute = AsyncMock(return_value=mock_result)

    # Call method
    result = await user_repository.update_password(
        email=user.email, hashed_password="newpassword"
    )
    assert result is not None
    assert user.hashed_password == "newpassword"
