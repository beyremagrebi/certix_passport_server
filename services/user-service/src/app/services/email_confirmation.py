import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from urllib.parse import quote

from flask import current_app

from app.extensions import db
from app.models.email_confirmation_token import EmailConfirmationToken
from app.models.user import User
from app.services.email import EmailDeliveryError, EmailService


class EmailConfirmationError(Exception):
    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self.status_code = status_code


class EmailConfirmationService:
    @staticmethod
    def _hash_token(token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    @staticmethod
    def create_and_send(user: User) -> None:
        raw_token = secrets.token_urlsafe(32)
        expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=current_app.config["EMAIL_CONFIRMATION_EXPIRES_MINUTES"]
        )
        db.session.add(
            EmailConfirmationToken(
                user_id=user.id,
                token_hash=EmailConfirmationService._hash_token(raw_token),
                expires_at=expires_at,
            )
        )
        db.session.commit()

        confirmation_url = (
            f"{current_app.config['APP_BASE_URL']}/auth/confirm-email"
            f"?token={quote(raw_token)}"
        )
        try:
            EmailService.send_confirmation_email(
                recipient=user.email,
                recipient_name=user.first_name,
                confirmation_url=confirmation_url,
            )
        except EmailDeliveryError as exc:
            raise EmailConfirmationError(str(exc), 503) from exc

    @staticmethod
    def confirm(raw_token: str) -> None:
        if not raw_token:
            raise EmailConfirmationError("Confirmation token is required.", 400)

        token_record = db.session.execute(
            db.select(EmailConfirmationToken).where(
                EmailConfirmationToken.token_hash
                == EmailConfirmationService._hash_token(raw_token)
            )
        ).scalar_one_or_none()
        now = datetime.now(timezone.utc)

        if (
            token_record is None
            or token_record.used_at is not None
            or token_record.expires_at <= now
        ):
            raise EmailConfirmationError(
                "The confirmation link is invalid or expired.", 400
            )

        user = db.session.get(User, token_record.user_id)
        if user is None:
            raise EmailConfirmationError(
                "The confirmation link is invalid or expired.", 400
            )

        user.email_confirmed = True
        token_record.used_at = now
        db.session.commit()
