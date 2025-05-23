# test_contact_repository_unit.py - Unit tests for ContactRepository

# pylint: disable=redefined-outer-name

from unittest.mock import AsyncMock, MagicMock
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users import User
from src.models.contacts import Contact
from src.repository.contacts import ContactRepository
from src.schemas.contacts import ContactModel


@pytest.fixture
def mock_session():
    mock_session = AsyncMock(spec=AsyncSession)
    return mock_session


@pytest.fixture
def contact_repository(mock_session):
    return ContactRepository(mock_session)


@pytest.fixture
def user():
    return User(id=1, username="testuser")


@pytest.mark.asyncio
async def test_get_contacts(contact_repository, mock_session, user):
    # Setup mock
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [
        Contact(id=1, first_name="test", last_name="test", user=user)
    ]
    mock_session.execute = AsyncMock(return_value=mock_result)

    # Call method
    contacts = await contact_repository.get_contacts(
        query="", skip=0, limit=10, user=user
    )

    # Assertions
    assert len(contacts) == 1
    assert contacts[0].first_name == "test"


@pytest.mark.asyncio
async def test_get_contact_by_id(contact_repository, mock_session, user):
    # Setup mock
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = Contact(
        id=1, first_name="test", last_name="test", user=user
    )
    mock_session.execute = AsyncMock(return_value=mock_result)

    # Call method
    contact = await contact_repository.get_contact_by_id(contact_id=1, user=user)

    # Assertions
    assert contact is not None
    assert contact.id == 1
    assert contact.first_name == "test"


@pytest.mark.asyncio
async def test_create_contact(contact_repository, mock_session, user):
    # Setup
    contact_data = ContactModel(
        first_name="new contact",
        last_name="new contact",
        email="new_contact@example.com",
    )

    # Call method
    result = await contact_repository.create_contact(body=contact_data, user=user)

    # Assertions
    assert isinstance(result, Contact)
    assert result.first_name == "new contact"
    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once_with(result)


@pytest.mark.asyncio
async def test_update_contact(contact_repository, mock_session, user):
    # Setup
    contact_data = ContactModel(
        first_name="updated contact",
        last_name="updated contact",
        email="updated_contact@example.com",
    )
    existing_contact = Contact(
        id=1, first_name="old contact", last_name="old contact", user=user
    )
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = existing_contact
    mock_session.execute = AsyncMock(return_value=mock_result)

    # Call method
    result = await contact_repository.update_contact(
        contact_id=1, body=contact_data, user=user
    )

    # Assertions
    assert result is not None
    assert result.first_name == "updated contact"
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once_with(existing_contact)


@pytest.mark.asyncio
async def test_remove_contact(contact_repository, mock_session, user):
    # Setup
    existing_contact = Contact(
        id=1, first_name="contact to delete", last_name="contact to delete", user=user
    )
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = existing_contact
    mock_session.execute = AsyncMock(return_value=mock_result)

    # Call method
    result = await contact_repository.remove_contact(contact_id=1, user=user)

    # Assertions
    assert result is not None
    assert result.first_name == "contact to delete"
    mock_session.delete.assert_awaited_once_with(existing_contact)
    mock_session.commit.assert_awaited_once()
