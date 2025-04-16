"""Email service for sending transactional emails.

This module provides email functionality using FastAPI-Mail, supporting:
- HTML email templates
- Email verification flows
- Configurable SMTP settings
- Error handling and logging

The service uses environment variables for configuration and supports
both TLS and SSL connections to the SMTP server.
"""

import logging
from pathlib import Path
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors

from pydantic import EmailStr

from src.conf.config import settings
from src.services.auth import TokenService


class EmailService:
    """Service for sending transactional emails.

    This class handles email sending operations using FastAPI-Mail, including:
    - Configuration of SMTP settings
    - Template-based email sending
    - Email verification token generation
    - Error handling and logging

    The service is configured using environment variables defined in settings.
    """

    def __init__(
        self,
    ):
        """Initialize email service with SMTP configuration.

        Sets up the FastAPI-Mail connection configuration using settings from
        environment variables. The configuration includes:
        - SMTP server details (host, port)
        - Authentication credentials
        - TLS/SSL settings
        - Template directory location
        """
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
        """Send an email using FastAPI-Mail.

        Args:
            message (MessageSchema): Email message configuration including recipients,
                                   subject, and template variables
            template_name (str, optional): Name of the HTML template file. Defaults to None

        Note:
            If template_name is provided, the email will be rendered using the specified
            HTML template. Otherwise, it will be sent as plain text.
        """
        fm = FastMail(self.conf)
        await fm.send_message(message, template_name)

    async def send_confirm_mail(
        self,
        email: EmailStr,
        username: str,
        host: str,
    ):
        """Send an email verification message.

        This method:
        1. Generates an email verification token
        2. Creates an HTML email using the confirm_email.html template
        3. Sends the verification email with the token
        4. Handles and logs any connection errors

        Args:
            email (EmailStr): Recipient's email address
            username (str): Recipient's username
            host (str): Base URL for the verification link

        Note:
            If sending fails, the error is logged but no exception is raised
            to prevent disrupting the registration flow.
        """
        try:
            token_verification = TokenService().create_email_token({"sub": email})
            message = MessageSchema(
                subject=f"{settings.TITLE} - Confirm your email",
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
            logging.error("Failed send confirm email to %s , error: %s", email, err)

    async def send_reset_password_link(self, email: EmailStr, username: str, host: str):
        try:
            token_verification = TokenService().create_reset_password_token(
                {"sub": email}
            )
            message = MessageSchema(
                # Reset password subjects marks as SPAM
                subject=f"{settings.TITLE} - Service maintenance request",  # no SPAM title
                recipients=[email],
                template_body={
                    "host": host,
                    "username": username,
                    "token": token_verification,
                },
                subtype=MessageType.html,
            )
            await self.send_email(message, "reset_password_via_email.html")

        except ConnectionErrors as err:
            logging.error("Failed send confirm email to %s , error: %s", email, err)
