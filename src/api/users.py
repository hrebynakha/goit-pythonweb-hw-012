"""User management API endpoints for user profile operations.

This module provides FastAPI router with endpoints for:
- Retrieving user profile information
- Updating user avatar images
- Rate limiting on profile access

The endpoints in this module require authentication and implement
rate limiting to prevent abuse.
"""

from fastapi import APIRouter, Depends, Request, File, UploadFile

from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.models.users import User as UserModel
from src.schemas.users import User
from src.schemas.auth import UnauthorizedResponse
from src.dependencies.roles import get_current_user, get_current_admin_user
from src.services.fs import UploadFileService
from src.services.users import UserService
from src.exceptions.fs import FileUploadError

router = APIRouter(prefix="/users", tags=["users"])


limiter = Limiter(key_func=get_remote_address)


@router.get(
    "/me",
    response_model=User,
    description="No more than 5 requests per minute",
    responses={
        401: {"model": UnauthorizedResponse, "description": "Unauthorized"},
    },
)
@limiter.limit("5/minute")
async def me(
    request: Request, user: UserModel = Depends(get_current_user)
):  # pylint: disable=unused-argument
    """Get the current user's profile information.

    This endpoint returns the authenticated user's profile data.
    It is rate limited to prevent abuse.

    Args:
        request (Request): FastAPI request object (required for rate limiting)
        user (UserModel): Current authenticated user from JWT token

    Returns:
        User: User profile information

    Raises:
        HTTPException: 401 if user is not authenticated

    Note:
        Rate limited to 5 requests per minute per IP address
    """
    # @limiter issue https://github.com/laurentS/slowapi/issues/177
    return user


@router.patch("/avatar", response_model=User)
async def update_avatar_user(
    file: UploadFile = File(),
    user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """Update the current user's avatar image.

    This endpoint allows users to upload a new avatar image. The image
    is processed and stored using the file storage service (Cloudinary).

    Args:
        file (UploadFile): Image file to upload
        user (User): Current authenticated user
        db (AsyncSession): Database session

    Returns:
        User: Updated user profile with new avatar URL

    Raises:
        FileUploadError: If file upload to storage service fails
        HTTPException: 401 if user is not authenticated

    Note:
        The avatar URL is stored in the user's profile after successful upload
    """
    avatar_url = UploadFileService().upload_file(file, user.username)
    if not avatar_url:
        raise FileUploadError
    user_service = UserService(db)
    user = await user_service.update_avatar_url(user.email, avatar_url)
    return user
