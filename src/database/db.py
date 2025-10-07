"""Database configuration and session management.

This module provides the core database configuration and session management for the application.
It implements an async session manager using SQLAlchemy's async features, providing:
- Async engine configuration
- Session management with automatic cleanup
- Error handling and transaction rollback
- Dependency injection for FastAPI endpoints
"""

import contextlib
import ssl

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)

from src.conf.config import settings as config


class DatabaseSessionManager:
    """Async database session manager.

    This class manages database connections and sessions, providing a context manager
    for safe session handling with automatic cleanup and error handling.

    Attributes:
        _engine (AsyncEngine | None): SQLAlchemy async engine instance
        _session_maker (async_sessionmaker): Factory for creating new database sessions
    """

    def __init__(self, url: str):
        """Initialize the session manager with database URL.

        Args:
            url (str): Database connection URL
        """
        if config.DB_SSL_MODE == "require":
            ssl_context = ssl.create_default_context(cafile="rds-ca-bundle.pem")
        else:
            ssl_context = None

        print("Created Database ssl context", ssl_context)

        self._engine: AsyncEngine | None = create_async_engine(
            url, connect_args={"ssl": ssl_context}
        )
        self._session_maker: async_sessionmaker = async_sessionmaker(
            autoflush=False, autocommit=False, bind=self._engine
        )

    @contextlib.asynccontextmanager
    async def session(self):
        """Create and manage a database session.

        Yields:
            AsyncSession: Database session

        Raises:
            SQLAlchemyError: If session initialization fails or database errors occur

        Note:
            Sessions are automatically closed and transactions rolled back on errors
        """
        if self._session_maker is None:
            raise SQLAlchemyError("Database session is not initialized")
        session = self._session_maker()
        try:
            yield session
        except SQLAlchemyError as e:
            await session.rollback()
            raise e from e
        finally:
            await session.close()


# Global session manager instance
sessionmanager = DatabaseSessionManager(config.DB_URL)


async def get_db():
    """FastAPI dependency for database session injection.

    Yields:
        AsyncSession: Database session for use in FastAPI endpoints

    Example:
        @router.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db)):
            # Use db session here
            pass
    """
    async with sessionmanager.session() as session:
        yield session
