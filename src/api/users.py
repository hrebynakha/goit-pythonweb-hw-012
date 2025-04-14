from fastapi import APIRouter, Depends, Request, File, UploadFile

from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.models.users import User as UserModel
from src.schemas.users import User
from src.schemas.auth import UnauthorizedResponse
from src.dependencies.auth import get_current_user
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
    # @limiter issue https://github.com/laurentS/slowapi/issues/177
    return user


@router.patch("/avatar", response_model=User)
async def update_avatar_user(
    file: UploadFile = File(),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    avatar_url = UploadFileService().upload_file(file, user.username)
    if not avatar_url:
        raise FileUploadError
    user_service = UserService(db)
    user = await user_service.update_avatar_url(user.email, avatar_url)
    return user
