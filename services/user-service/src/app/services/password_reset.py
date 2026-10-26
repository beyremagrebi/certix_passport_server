import hashlib
import logging
import secrets
from datetime import datetime, timedelta, timezone
from urllib.parse import quote

from flask import current_app

from app.extensions import db
from app.models.password_reset_token import PasswordResetToken
from app.models.refresh_token import RefreshToken
from app.repositories.user_repository import UserRepository
from app.services.email import EmailDeliveryError, EmailService


logger = logging.getLogger(__name__)


class PasswordResetService:
    @staticmethod
    def _hash_token(token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    @staticmethod
    def request_reset(email: str) -> None:
        user = UserRepository.get_by_email(email)
        if user is None or not user.is_active:
            return

        now = datetime.now(timezone.utc)
        db.session.execute(
            db.update(PasswordResetToken)
            .where(
                PasswordResetToken.user_id == user.id,
                PasswordResetToken.used_at.is_(None),
            )
            .values(used_at=now)
        )

        raw_token = secrets.token_urlsafe(32)
        db.session.add(
            PasswordResetToken(
                user_id=user.id,
                token_hash=PasswordResetService._hash_token(raw_token),
                expires_at=now
                + timedelta(
                    minutes=current_app.config["PASSWORD_RESET_EXPIRES_MINUTES"]
                ),
            )
        )
        db.session.commit()

        reset_url = (
            f"{current_app.config['APP_BASE_URL']}/auth/reset-password"
            f"?token={quote(raw_token)}"
        )
        try:
            EmailService.send_password_reset_email(
                recipient=user.email,
                recipient_name=user.first_name,
                reset_url=reset_url,
            )
        except EmailDeliveryError:
            logger.exception("Password reset email delivery failed.")

    @staticmethod
    def reset_password(*, raw_token: str, new_password: str) -> None:
        now = datetime.now(timezone.utc)
        token_record = db.session.execute(
            db.select(PasswordResetToken).where(
                PasswordResetToken.token_hash
                == PasswordResetService._hash_token(raw_token)
            )
        ).scalar_one_or_none()

        if (
            token_record is None
            or token_record.used_at is not None
            or token_record.expires_at <= now
        ):
            raise ValueError("The password reset link is invalid or expired.")

        user = UserRepository.get_by_id(token_record.user_id)
        if user is None or not user.is_active:
            raise ValueError("The password reset link is invalid or expired.")

        user.set_password(new_password)
        token_record.used_at = now
        db.session.execute(
            db.update(RefreshToken)
            .where(RefreshToken.user_id == user.id)
            .values(revoked=True)
        )
        db.session.commit()
