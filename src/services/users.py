"""User management service module.

This module provides business logic for user management operations including:
- User creation with email verification
- Gravatar integration for user avatars
- User lookup by various identifiers
- Email confirmation handling
- Avatar URL management

The service layer acts as an intermediary between the API endpoints and the user repository,
handling data transformation, validation, and coordinating multiple operations.
"""

import logging
from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from libgravatar import Gravatar


from src.services.auth import Hash
from src.repository.users import UserRepository
from src.schemas.users import UserCreate
from src.services.email import EmailService


class UserService:
    """Service for managing user-related operations.

    This class coordinates user operations between the API layer and the repository,
    handling business logic like password hashing, avatar generation, and email notifications.

    Attributes:
        repository (UserRepository): Data access layer for user operations
    """

    def __init__(self, db: AsyncSession):
        """Initialize the user service.

        Args:
            db (AsyncSession): Database session for repository operations
        """
        self.repository = UserRepository(db)

    async def create_user_and_send_email(
        self, body: UserCreate, background_tasks: BackgroundTasks, host_url: str = None
    ):
        """Create a new user and send verification email.

        This method:
        1. Generates a Gravatar URL for the user's email
        2. Hashes the user's password
        3. Creates the user in the database
        4. Sends a verification email asynchronously

        Args:
            body (UserCreate): User creation data including email and password
            background_tasks (BackgroundTasks): FastAPI background task manager
            host_url (str, optional): Base URL for email verification. Defaults to None

        Returns:
            User: Created user object

        Note:
            If Gravatar generation fails, the error is logged but user creation continues
        """
        avatar = None
        mail_service = EmailService()

        try:
            g = Gravatar(body.email)
            avatar = g.get_image()
        except ValueError as e:
            logging.warning("Error get user avatar, error:%s", e)

        body.password = Hash().get_password_hash(body.password)
        new_user = await self.repository.create_user(body, avatar)

        background_tasks.add_task(
            mail_service.send_confirm_mail, new_user.email, new_user.username, host_url
        )
        return new_user

    async def send_reset_password_link(
        self,
        email: str,
        username: str,
        background_tasks: BackgroundTasks,
        host_url: str = None,
    ):
        """Send a password reset link to the user's email.

        Args:
            email (str): User's email address
            username (str): User's username
            background_tasks (BackgroundTasks): FastAPI background task manager
            host_url (str, optional): Base URL for email verification. Defaults to None
        """
        mail_service = EmailService()
        background_tasks.add_task(
            mail_service.send_reset_password_link, email, username, host_url
        )

    async def get_user_by_id(self, user_id: int):
        """Retrieve a user by their ID.

        Args:
            user_id (int): User's unique identifier

        Returns:
            User | None: User object if found, None otherwise
        """
        return await self.repository.get_user_by_id(user_id)

    async def get_user_by_username(self, username: str):
        """Retrieve a user by their username.

        Args:
            username (str): User's username

        Returns:
            User | None: User object if found, None otherwise
        """
        return await self.repository.get_user_by_username(username)

    async def get_user_by_email(self, email: str):
        """Retrieve a user by their email address.

        Args:
            email (str): User's email address

        Returns:
            User | None: User object if found, None otherwise
        """
        return await self.repository.get_user_by_email(email)

    async def confirmed_email(self, email: str):
        """Mark a user's email as confirmed.

        Args:
            email (str): Email address to confirm

        Returns:
            User | None: Updated user object if found, None otherwise
        """
        return await self.repository.confirmed_email(email)

    async def update_avatar_url(self, email: str, url: str):
        """Update a user's avatar URL.

        Args:
            email (str): User's email address
            url (str): New avatar URL

        Returns:
            User | None: Updated user object if found, None otherwise
        """
        return await self.repository.update_avatar_url(email, url)

    async def update_password(self, email: str, new_password: str):
        """Update a user's password.

        Args:
            user (User): User object
            new_password (str): New password

        Returns:
            User | None: Updated user object if found, None otherwise
        """
        hashed_password = Hash().get_password_hash(new_password)
        return await self.repository.update_password(email, hashed_password)
