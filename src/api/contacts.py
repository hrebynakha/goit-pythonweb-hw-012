"""Contact management API endpoints.

This module provides REST API endpoints for managing user contacts, including:
- CRUD operations for contacts
- Contact list filtering and pagination
- Upcoming birthday notifications
- Redis-based caching for improved performance

All endpoints require user authentication and support proper error handling.
"""

from typing import List

from fastapi import APIRouter, Depends, status, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.schemas.contacts import ContactModel, ContactResponse
from src.services.contacts import ContactService
from src.dependencies.roles import get_current_user
from src.exceptions.contacts import ContactNotFound
from src.schemas.auth import UnauthorizedResponse
from src.schemas.contacts import ContactNotFoundResponse
from src.helpers.helpers import filter_normalize
from src.models.users import User
from src.database.redis.client import get_redis, AsyncRedisSessionManager

router = APIRouter(
    prefix="/contacts",
    tags=["contacts"],
    responses={
        401: {"model": UnauthorizedResponse, "description": "Unauthorized"},
    },
)


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(
    skip: int = 0,
    limit: int = 100,
    query: str = Query(default=""),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    redis: AsyncRedisSessionManager = Depends(get_redis),
):
    """Get a paginated and filtered list of user contacts with caching.

    Args:
        skip (int, optional): Number of records to skip. Defaults to 0
        limit (int, optional): Maximum number of records to return. Defaults to 100
        filter (str, optional): Filter query string. Defaults to ""
        db (AsyncSession, optional): Database session. Defaults to Depends(get_db)
        user (User, optional): Authenticated user. Defaults to Depends(get_current_user)
        redis (RedisSessionManager, optional): Redis connection. Defaults to Depends(get_redis)

    Returns:
        List[ContactResponse]: List of contact objects

    Note:
        Results are cached in Redis for 10 seconds to improve performance
    """
    key = f"contacts_{str(query)}{skip}{limit}{user.id}"
    cached_item = await redis.get(key)
    if cached_item:
        return cached_item
    contact_service = ContactService(db)
    contacts = await contact_service.get_contacts(
        filter_normalize(query), skip, limit, user
    )
    await redis.set(key, jsonable_encoder(contacts), ex=10)
    return contacts


@router.get(
    "/get-upcoming-birthday",
    response_model=List[ContactResponse],
)
async def get_upcoming_birthday(
    skip: int = 0,
    limit: int = 100,
    time_range: int = 7,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    redis: AsyncRedisSessionManager = Depends(get_redis),
):
    """Get contacts with upcoming birthdays within specified time range.

    Args:
        skip (int, optional): Number of records to skip. Defaults to 0
        limit (int, optional): Maximum number of records to return. Defaults to 100
        time_range (int, optional): Days to look ahead for birthdays. Defaults to 7
        db (AsyncSession, optional): Database session. Defaults to Depends(get_db)
        user (User, optional): Authenticated user. Defaults to Depends(get_current_user)
        redis (AsyncRedisSessionManager, optional): Redis connection. Defaults to Depends(get_redis)

    Returns:
        List[ContactResponse]: List of contacts with upcoming birthdays

    Note:
        Results are cached in Redis for 1 hour to improve performance
    """
    key = f"upcoming_birthday_{user.id}{skip}{limit}{time_range}"
    cached_item = await redis.get(key)
    if cached_item:
        return cached_item
    contact_service = ContactService(db)

    contacts = await contact_service.get_upcoming_birthday_contacts(
        skip, limit, time_range, user
    )
    await redis.set(key, jsonable_encoder(contacts), ex=3600)
    return contacts


@router.get(
    "/{contact_id}",
    response_model=ContactResponse,
    responses={
        404: {"model": ContactNotFoundResponse, "description": "Not found response"},
    },
)
async def read_contact(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    redis: AsyncRedisSessionManager = Depends(get_redis),
    user: User = Depends(get_current_user),
):
    """Get a specific contact by ID with caching.

    Args:
        contact_id (int): ID of the contact to retrieve
        db (AsyncSession, optional): Database session. Defaults to Depends(get_db)
        redis (AsyncRedisSessionManager, optional): Redis connection. Defaults to Depends(get_redis)
        user (User, optional): Authenticated user. Defaults to Depends(get_current_user)

    Returns:
        ContactResponse: Contact details

    Raises:
        ContactNotFound: If contact with given ID doesn't exist

    Note:
        Results are cached in Redis for 10 seconds to improve performance
    """
    cached_item = await redis.get(f"contact_{contact_id}")
    if cached_item:
        return cached_item
    contact_service = ContactService(db)
    contact = await contact_service.get_contact(contact_id, user)
    if contact is None:
        raise ContactNotFound

    await redis.set(f"contact_{contact_id}", jsonable_encoder(contact), ex=10)
    return contact


@router.post(
    "/",
    response_model=ContactResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_contact(
    body: ContactModel,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Create a new contact.

    Args:
        body (ContactModel): Contact data including name, email, phone, etc.
        db (AsyncSession, optional): Database session. Defaults to Depends(get_db)
        user (User, optional): Authenticated user. Defaults to Depends(get_current_user)

    Returns:
        ContactResponse: Created contact details

    Note:
        The contact will be associated with the authenticated user
    """
    contact_service = ContactService(db)
    return await contact_service.create_contact(body, user)


@router.put(
    "/{contact_id}",
    response_model=ContactResponse,
    responses={
        404: {"model": ContactNotFoundResponse, "description": "Not found response"},
    },
)
async def update_contact(
    body: ContactModel,
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Update an existing contact.

    Args:
        body (ContactModel): Updated contact data
        contact_id (int): ID of the contact to update
        db (AsyncSession, optional): Database session. Defaults to Depends(get_db)
        user (User, optional): Authenticated user. Defaults to Depends(get_current_user)

    Returns:
        ContactResponse: Updated contact details

    Raises:
        ContactNotFound: If contact with given ID doesn't exist
    """
    contact_service = ContactService(db)
    contact = await contact_service.update_contact(contact_id, body, user)
    if contact is None:
        raise ContactNotFound
    return contact


@router.delete(
    "/{contact_id}",
    response_model=ContactResponse,
    responses={
        404: {"model": ContactNotFoundResponse, "description": "Not found response"},
    },
)
async def remove_contact(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Delete a contact.

    Args:
        contact_id (int): ID of the contact to delete
        db (AsyncSession, optional): Database session. Defaults to Depends(get_db)
        user (User, optional): Authenticated user. Defaults to Depends(get_current_user)

    Returns:
        ContactResponse: Deleted contact details

    Raises:
        ContactNotFound: If contact with given ID doesn't exist
    """
    contact_service = ContactService(db)
    contact = await contact_service.remove_contact(contact_id, user)
    if contact is None:
        raise ContactNotFound
    return contact
