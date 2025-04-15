"""User repository module for database operations related to users.

This module provides a repository pattern implementation for user-related database operations
using SQLAlchemy async session for PostgreSQL database interactions.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users import User
from src.schemas.users import UserCreate


class UserRepository:
    """Repository for handling user-related database operations.

    This class implements the repository pattern for user operations including:
    - User CRUD operations
    - Authentication-related user queries
    - Email verification
    - Avatar management
    """

    def __init__(self, session: AsyncSession):
        """Initialize repository with database session.

        Args:
            session (AsyncSession): SQLAlchemy async session for database operations
        """
        self.db = session

    async def get_user_by_id(self, user_id: int) -> User | None:
        """Retrieve user by their ID.

        Args:
            user_id (int): User's unique identifier

        Returns:
            User | None: User object if found, None otherwise
        """
        query = select(User).filter_by(id=user_id)
        user = await self.db.execute(query)
        return user.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> User | None:
        """Retrieve user by their username.

        Args:
            username (str): User's unique username

        Returns:
            User | None: User object if found, None otherwise
        """
        query = select(User).filter_by(username=username)
        user = await self.db.execute(query)
        return user.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> User | None:
        """Retrieve user by their email address.

        Args:
            email (str): User's unique email address

        Returns:
            User | None: User object if found, None otherwise
        """
        query = select(User).filter_by(email=email)
        user = await self.db.execute(query)
        return user.scalar_one_or_none()

    async def create_user(self, body: UserCreate, avatar: str = None) -> User:
        """Create a new user in the database.

        Args:
            body (UserCreate): User creation data including username, email, and password
            avatar (str, optional): URL to user's avatar image. Defaults to None

        Returns:
            User: Created user object
        """
        user = User(
            **body.model_dump(exclude_unset=True, exclude={"password"}),
            hashed_password=body.password,
            avatar=avatar,
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update_user_refresh_token(self, username: str, token: str) -> User:
        """Update user's refresh token.

        Args:
            username (str): Username of the user to update
            token (str): New refresh token value

        Returns:
            User: Updated user object
        """
        user = await self.get_user_by_username(username)
        user.refresh_token = token
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_user_by_username_and_token(
        self, username: str, token: str
    ) -> User | None:
        """Retrieve user by username and refresh token combination.

        Used for validating refresh token operations.

        Args:
            username (str): Username to match
            token (str): Refresh token to match

        Returns:
            User | None: User object if found with matching token, None otherwise
        """
        query = select(User).filter(
            User.username == username, User.refresh_token == token
        )
        user = await self.db.execute(query)
        return user.scalar_one_or_none()

    async def confirmed_email(self, email: str):
        """Mark user's email as verified.

        Args:
            email (str): Email address of the user to verify
        """
        user = await self.get_user_by_email(email)
        user.is_verified = True
        await self.db.commit()

    async def update_avatar_url(self, email: str, url: str) -> User:
        """Update user's avatar URL.

        Args:
            email (str): Email of the user to update
            url (str): New avatar URL

        Returns:
            User: Updated user object
        """
        user = await self.get_user_by_email(email)
        user.avatar = url
        await self.db.commit()
        await self.db.refresh(user)
        return user
