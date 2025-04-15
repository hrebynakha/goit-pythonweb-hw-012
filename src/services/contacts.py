"""Contact management service layer.

This module provides business logic for contact operations including:
- Contact creation and validation
- Contact retrieval with filtering and pagination
- Contact updates and deletion
- Birthday reminder functionality
- Email uniqueness enforcement
"""

from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.contacts import ContactRepository
from src.schemas.contacts import ContactModel
from src.exceptions.contacts import EmailValueError
from src.models.users import User


class ContactService:
    """Service for managing contact operations.

    This service handles all contact-related business logic, including:
    - Contact CRUD operations
    - Email uniqueness validation
    - Birthday reminders
    - Pagination and filtering

    Attributes:
        repository (ContactRepository): Data access layer for contacts
    """

    def __init__(self, db: AsyncSession):
        """Initialize contact service with database session.

        Args:
            db (AsyncSession): SQLAlchemy async database session
        """
        self.repository = ContactRepository(db)

    async def create_contact(self, body: ContactModel, user: User):
        """Create a new contact for a user.

        This method ensures email uniqueness within a user's contacts before
        creating the new contact.

        Args:
            body (ContactModel): Contact data for creation
            user (User): User who owns the contact

        Returns:
            Contact: Created contact object

        Raises:
            EmailValueError: If a contact with the same email already exists
        """
        existing_contact = await self.repository.get_contact_by_email(body.email, user)
        if existing_contact:
            raise EmailValueError(f"Contact with this email {body.email} already exists")
        return await self.repository.create_contact(body, user)

    async def get_contacts(self, filter_: str, skip: int, limit: int, user: User):
        """Retrieve filtered and paginated contacts for a user.

        Args:
            filter_ (str): Filter string for searching contacts
            skip (int): Number of records to skip (offset)
            limit (int): Maximum number of records to return
            user (User): User whose contacts to retrieve

        Returns:
            List[Contact]: List of contacts matching the criteria
        """
        return await self.repository.get_contacts(filter_, skip, limit, user)

    async def get_contact(self, contact_id: int, user: User):
        """Retrieve a specific contact by ID.

        Args:
            contact_id (int): ID of the contact to retrieve
            user (User): User who owns the contact

        Returns:
            Contact | None: Contact if found, None otherwise
        """
        return await self.repository.get_contact_by_id(contact_id, user)

    async def update_contact(self, contact_id: int, body: ContactModel, user: User):
        """Update an existing contact.

        This method ensures email uniqueness is maintained when updating
        contact information.

        Args:
            contact_id (int): ID of the contact to update
            body (ContactModel): Updated contact data
            user (User): User who owns the contact

        Returns:
            Contact: Updated contact object

        Raises:
            EmailValueError: If the new email conflicts with another contact
        """
        existing_contact = await self.repository.get_contact_by_email_and_contact_id(
            body.email, contact_id, user
        )
        if existing_contact:
            raise EmailValueError(f"Contact with this email {body.email} already exists")
        return await self.repository.update_contact(contact_id, body, user)

    async def remove_contact(self, contact_id: int, user: User):
        """Delete a contact.

        Args:
            contact_id (int): ID of the contact to delete
            user (User): User who owns the contact

        Returns:
            Contact: Deleted contact object
        """
        return await self.repository.remove_contact(contact_id, user)

    async def get_upcoming_birthday_contacts(self, skip, limit, time_range, user: User):
        """Retrieve contacts with upcoming birthdays.

        Args:
            skip (int): Number of records to skip (offset)
            limit (int): Maximum number of records to return
            time_range (int): Number of days to look ahead
            user (User): User whose contacts to check

        Returns:
            List[Contact]: List of contacts with birthdays in the specified range
        """
        return await self.repository.get_upcoming_birthday_contacts(
            skip,
            limit,
            user,
            time_range,
        )
