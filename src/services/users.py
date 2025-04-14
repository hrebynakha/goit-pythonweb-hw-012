import logging
from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from libgravatar import Gravatar


from src.services.auth import Hash
from src.repository.users import UserRepository
from src.schemas.users import UserCreate
from src.services.email import EmailService


class UserService:
    def __init__(self, db: AsyncSession):
        self.repository = UserRepository(db)

    async def create_user_and_send_email(
        self, body: UserCreate, background_tasks: BackgroundTasks, host_url: str = None
    ):
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

    async def get_user_by_id(self, user_id: int):
        return await self.repository.get_user_by_id(user_id)

    async def get_user_by_username(self, username: str):
        return await self.repository.get_user_by_username(username)

    async def get_user_by_email(self, email: str):
        return await self.repository.get_user_by_email(email)

    async def confirmed_email(self, email: str):
        return await self.repository.confirmed_email(email)

    async def update_avatar_url(self, email: str, url: str):
        return await self.repository.update_avatar_url(email, url)
