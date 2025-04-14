import logging
from pathlib import Path
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors

from pydantic import EmailStr

from src.conf.config import settings
from src.services.auth import TokenService


class EmailService:
    def __init__(
        self,
    ):
        self.conf = ConnectionConfig(
            MAIL_USERNAME=settings.MAIL_USERNAME,
            MAIL_PASSWORD=settings.MAIL_PASSWORD,
            MAIL_FROM=settings.MAIL_FROM,
            MAIL_PORT=settings.MAIL_PORT,
            MAIL_SERVER=settings.MAIL_SERVER,
            MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
            MAIL_STARTTLS=settings.MAIL_STARTTLS,
            MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
            USE_CREDENTIALS=settings.USE_CREDENTIALS,
            VALIDATE_CERTS=settings.VALIDATE_CERTS,
            TEMPLATE_FOLDER=Path(__file__).parent / "templates",
        )

    async def send_email(self, message: MessageSchema, template_name: str = None):
        fm = FastMail(self.conf)
        await fm.send_message(message, template_name)

    async def send_confirm_mail(
        self,
        email: EmailStr,
        username: str,
        host: str,
    ):
        try:
            token_verification = TokenService().create_email_token({"sub": email})
            message = MessageSchema(
                subject="Confirm your email",
                recipients=[email],
                template_body={
                    "host": host,
                    "username": username,
                    "token": token_verification,
                },
                subtype=MessageType.html,
            )
            await self.send_email(message, "confirm_email.html")

        except ConnectionErrors as err:
            print("error mail send", err)
            logging.error("Failed send confim email to %s , error: %s", email, err)
