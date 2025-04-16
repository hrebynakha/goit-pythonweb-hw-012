"""Contact repository module for managing user contacts.

This module provides a repository pattern implementation for contact-related database operations,
including:
- Contact CRUD operations
- Contact filtering and pagination
- Birthday reminder functionality
- User-specific contact management
"""

from typing import List
from datetime import datetime, timedelta, timezone

from fastapi_sa_orm_filter.main import FilterCore

from sqlalchemy import select, func, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users import User
from src.models.contacts import Contact
from src.schemas.contacts import ContactModel
from src.filters.contacts import contact_filter


class ContactRepository:
    """Repository for handling contact-related database operations.

    This class provides methods for managing user contacts including:
    - Creating, reading, updating, and deleting contacts
    - Filtering and paginating contact lists
    - Finding contacts by various criteria (ID, email)
    - Managing upcoming birthday notifications
    """

    def __init__(self, session: AsyncSession):
        """Initialize repository with database session.

        Args:
            session (AsyncSession): SQLAlchemy async session for database operations
        """
        self.db = session

    async def get_contacts(
        self, query: str, skip: int, limit: int, user: User
    ) -> List[Contact]:
        """Retrieve filtered and paginated list of user contacts.

        Args:
            query (str): Filter query string for contact filtering
            skip (int): Number of records to skip (offset)
            limit (int): Maximum number of records to return
            user (User): User whose contacts to retrieve

        Returns:
            List[Contact]: List of filtered contact objects
        """
        filter_inst = FilterCore(
            Contact, contact_filter, select(Contact).filter(Contact.user_id == user.id)
        )
        query_ = (
            filter_inst.get_query(query).offset(skip).limit(limit).order_by(Contact.id)
        )
        contacts = await self.db.execute(query_)
        return contacts.scalars().all()

    async def get_contact_by_id(self, contact_id: int, user: User) -> Contact | None:
        """Retrieve a specific contact by ID for a user.

        Args:
            contact_id (int): ID of the contact to retrieve
            user (User): User who owns the contact

        Returns:
            Contact | None: Contact object if found, None otherwise
        """
        query = select(Contact).filter_by(id=contact_id, user=user)
        contact = await self.db.execute(query)
        return contact.scalar_one_or_none()

    async def get_contact_by_email(
        self,
        contact_email: str,
        user: User,
    ) -> Contact | None:
        """Retrieve a contact by email address for a user.

        Args:
            contact_email (str): Email address of the contact
            user (User): User who owns the contact

        Returns:
            Contact | None: Contact object if found, None otherwise
        """
        query = select(Contact).filter_by(email=contact_email, user=user)
        contact = await self.db.execute(query)
        return contact.scalar_one_or_none()

    async def get_contact_by_email_and_contact_id(
        self,
        contact_email: str,
        contact_id: int,
        user: User,
    ) -> Contact | None:
        """Find a contact by email excluding a specific contact ID.

        Used for checking email uniqueness when updating contacts.

        Args:
            contact_email (str): Email address to search for
            contact_id (int): Contact ID to exclude from search
            user (User): User who owns the contacts

        Returns:
            Contact | None: Contact object if found, None otherwise
        """
        query = select(Contact).filter(
            Contact.email == contact_email,
            Contact.id != contact_id,
            Contact.user_id == user.id,
        )

        contact = await self.db.execute(query)
        return contact.scalar_one_or_none()

    async def create_contact(self, body: ContactModel, user: User) -> Contact:
        """Create a new contact for a user.

        Args:
            body (ContactModel): Contact data including name, email, etc.
            user (User): User who will own the contact

        Returns:
            Contact: Created contact object
        """
        contact = Contact(**body.model_dump(exclude_unset=True), user=user)
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return contact

    async def update_contact(
        self, contact_id: int, body: ContactModel, user: User
    ) -> Contact | None:
        """Update an existing contact's information.

        Only updates fields that have changed from their current values.

        Args:
            contact_id (int): ID of the contact to update
            body (ContactModel): Updated contact data
            user (User): User who owns the contact

        Returns:
            Contact | None: Updated contact object if found, None otherwise
        """
        contact = await self.get_contact_by_id(contact_id, user)
        for field, value in body.model_dump(exclude_unset=True).items():
            current_value = getattr(contact, field)
            if current_value != value:
                setattr(contact, field, value)
        await self.db.commit()
        await self.db.refresh(contact)
        return contact

    async def remove_contact(self, contact_id: int, user: User) -> Contact | None:
        """Delete a contact from the database.

        Args:
            contact_id (int): ID of the contact to delete
            user (User): User who owns the contact

        Returns:
            Contact | None: Deleted contact object if found, None otherwise
        """
        contact = await self.get_contact_by_id(contact_id, user)
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
        return contact

    async def get_upcoming_birthday_contacts(
        self,
        skip: int,
        limit: int,
        user: User,
        time_range: int = 7,
    ) -> List[Contact]:
        """
        Search contacts in database where birthday for user is in set range.Default - 7 day
        Debug to change current time manually:
        current_time = datetime.strptime("Dec 24 2005  1:33PM", "%b %d %Y %I:%M%p")
        """
        current_time = datetime.now(tz=timezone.utc)
        delta = current_time + timedelta(days=time_range)
        start, end = current_time.strftime("%m-%d"), delta.strftime("%m-%d")
        fn_ = or_ if current_time.month > delta.month else and_
        query = (
            select(Contact)
            .filter(
                fn_(
                    func.to_char(Contact.birthday, "MM-DD") >= start,
                    func.to_char(Contact.birthday, "MM-DD") <= end,
                ),
                Contact.user_id == user.id,
            )
            .offset(skip)
            .limit(limit)
        )
        contacts = await self.db.execute(query)
        return contacts.scalars().all()
