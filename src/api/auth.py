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
    user_service = UserService(db)
    user = await user_service.get_user_by_username(form_data.username)
    if not user or not Hash().verify_password(form_data.password, user.hashed_password):
        raise AuthError(detail="User or password is incorrect")

    return await AuthService(db).geneate_jwt(user.username)


@router.post("/refresh-token", response_model=Token)
async def new_token(request: TokenRefreshRequest, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    user = auth_service.verify_refresh_token(request.refresh_token)
    if user is None:
        raise AuthError(detail="Invalid or expired refresh token")

    return await auth_service.update_jwt(user.username, request.refresh_token)


@router.get("/confirmed_email/{token}", response_model=EmailVerifyResponse)
async def confirmed_email(token: str, db: AsyncSession = Depends(get_db)):
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
