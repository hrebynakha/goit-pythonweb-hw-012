from fastapi import Depends
from src.dependencies.auth import get_auth_user
from src.models.users import User
from src.models.roles import Role
from src.exceptions.roles import AccessDeniedError


def get_current_user(current_user: User = Depends(get_auth_user)):
    if current_user.role not in [Role.USER, Role.ADMIN]:
        raise AccessDeniedError
    return current_user


def get_current_admin_user(current_user: User = Depends(get_auth_user)):
    if current_user.role != Role.ADMIN:
        raise AccessDeniedError
    return current_user
