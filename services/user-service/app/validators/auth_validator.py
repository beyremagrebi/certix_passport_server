from datetime import datetime, timezone

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.services.refresh_token_service import RefreshTokenService
from app.schemas.user import UserLogin, UserRegister


class EmailAlreadyRegistered(Exception):
    """Email is already registered."""


class InvalidCredentials(Exception):
    """Email or password is invalid."""


class InvalidRefreshToken(Exception):
    """Refresh token is invalid, expired, or revoked."""


class AuthValidator:
    """Validates authentication business rules."""

    def __init__(
        self,
        user_repository: UserRepository,
        refresh_token_service: RefreshTokenService,
    ) -> None:
        self.user_repository = user_repository
        self.refresh_token_service = refresh_token_service

    def validate_registration(self, data: UserRegister) -> str:
        email = str(data.email).strip().lower()

        if self.user_repository.get_by_email(email) is not None:
            raise EmailAlreadyRegistered

        return email

    def validate_login(self, data: UserLogin) -> User:
        email = str(data.email).strip().lower()
        user = self.user_repository.get_by_email(email)

        if user is None:
            raise InvalidCredentials

        from app.core.security import verify_password

        if not verify_password(data.password, user.password_hash):
            raise InvalidCredentials

        return user

    def validate_refresh_token(self, raw_token: str):
        record = self.refresh_token_service.get_by_raw_token(raw_token)

        if record is None:
            raise InvalidRefreshToken

        if record.revoked_at is not None:
            raise InvalidRefreshToken

        expires_at = record.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)

        if expires_at <= datetime.now(timezone.utc):
            raise InvalidRefreshToken

        return record