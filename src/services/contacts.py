"""Contacts serivices"""

from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.contacts import ContactRepository
from src.schemas.contacts import ContactModel
from src.exceptions.contacts import EmailValueError
from src.models.users import User


class ContactService:
    """Contact service"""

    def __init__(self, db: AsyncSession):
        self.repository = ContactRepository(db)

    async def create_contact(self, body: ContactModel, user: User):
        """Create contact service"""
        existing_contact = await self.repository.get_contact_by_email(body.email, user)
        if existing_contact:
            raise EmailValueError(f"Contact with this email {body.email} alredy exists")
        return await self.repository.create_contact(body, user)

    async def get_contacts(self, filter_: str, skip: int, limit: int, user: User):
        """Get contacts service"""
        return await self.repository.get_contacts(filter_, skip, limit, user)

    async def get_contact(self, contact_id: int, user: User):
        """get contact by id"""
        return await self.repository.get_contact_by_id(contact_id, user)

    async def update_contact(self, contact_id: int, body: ContactModel, user: User):
        """Update contact by id"""
        existing_contact = await self.repository.get_contact_by_email_and_contact_id(
            body.email, contact_id, user
        )
        if existing_contact:
            raise EmailValueError(f"Contact with this email {body.email} alredy exists")
        return await self.repository.update_contact(contact_id, body, user)

    async def remove_contact(self, contact_id: int, user: User):
        """Remove contact by ID"""
        return await self.repository.remove_contact(contact_id, user)

    async def get_upcoming_birthday_contacts(self, skip, limit, time_range, user: User):
        """Get contacts service"""
        return await self.repository.get_upcoming_birthday_contacts(
            skip,
            limit,
            user,
            time_range,
        )
