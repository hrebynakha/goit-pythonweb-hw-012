"""Authentication API endpoints for user registration, login, and email verification.

This module provides FastAPI router with endpoints for:
- User registration with email verification
- User login with JWT token generation
- JWT token refresh
- Email verification confirmation
"""

from fastapi import APIRouter, Depends, status, Request, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.auth import Token, TokenRefreshRequest, EmailVerifyResponse
from src.schemas.users import User, UserCreate
from src.services.auth import AuthService, Hash, TokenService
from src.services.users import UserService

from src.database.db import get_db
from src.exceptions.auth import (
    AuthError,
    RegistrationError,
    VerificationError,
    InvalidVerificationTokenError,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    background_tasks: BackgroundTasks,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Register a new user with email verification.

    Args:
        user_data (UserCreate): User registration data including username, email, and password
        background_tasks (BackgroundTasks): FastAPI background tasks for sending verification email
        request (Request): FastAPI request object for getting base URL
        db (AsyncSession, optional): Database session. Defaults to Depends(get_db)

    Returns:
        User: Created user object

    Raises:
        RegistrationError: If email or username already exists
    """
    user_service = UserService(db)

    if await user_service.get_user_by_email(user_data.email):
        raise RegistrationError(detail="User with this email alredy exist")

    if await user_service.get_user_by_username(user_data.username):
        raise RegistrationError

    new_user = await user_service.create_user_and_send_email(
        user_data, background_tasks, request.base_url
    )
    return new_user


@router.post("/login", response_model=Token)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    """Authenticate user and generate JWT tokens.

    Args:
        form_data (OAuth2PasswordRequestForm): Login credentials with username and password
        db (AsyncSession, optional): Database session. Defaults to Depends(get_db)

    Returns:
        Token: Access and refresh JWT tokens

    Raises:
        AuthError: If username/password combination is invalid
    """
    user_service = UserService(db)
    user = await user_service.get_user_by_username(form_data.username)
    if not user or not Hash().verify_password(form_data.password, user.hashed_password):
        raise AuthError(detail="User or password is incorrect")

    return await AuthService(db).generate_jwt(user.username)


@router.post("/refresh-token", response_model=Token)
async def new_token(request: TokenRefreshRequest, db: AsyncSession = Depends(get_db)):
    """Generate new JWT tokens using a refresh token.

    Args:
        request (TokenRefreshRequest): Request containing the refresh token
        db (AsyncSession, optional): Database session. Defaults to Depends(get_db)

    Returns:
        Token: New access and refresh JWT tokens

    Raises:
        AuthError: If refresh token is invalid or expired
    """
    auth_service = AuthService(db)
    user = auth_service.verify_refresh_token(request.refresh_token)
    if user is None:
        raise AuthError(detail="Invalid or expired refresh token")

    return await auth_service.update_jwt(user.username, request.refresh_token)


@router.get("/confirmed_email/{token}", response_model=EmailVerifyResponse)
async def confirmed_email(token: str, db: AsyncSession = Depends(get_db)):
    """Verify user's email address using verification token.

    Args:
        token (str): Email verification token
        db (AsyncSession, optional): Database session. Defaults to Depends(get_db)

    Returns:
        EmailVerifyResponse: Success message indicating email verification status

    Raises:
        InvalidVerificationTokenError: If verification token is invalid
        VerificationError: If user not found for the email in token
    """
    email = await TokenService().get_email_from_token(token)
    if not email:
        raise InvalidVerificationTokenError
    user_service = UserService(db)
    user = await user_service.get_user_by_email(email)
    if user is None:
        raise VerificationError

    if user.is_verified:
        return {"message": "Your email has already been confirmed."}
    await user_service.confirmed_email(email)
    return {"message": "Email verified successfully"}
