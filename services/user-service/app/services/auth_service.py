from datetime import datetime, timedelta, timezone

from sqlalchemy.exc import IntegrityError

from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    hash_refresh_token,
    verify_password,
)
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.repositories.refresh_token_repository import (
    RefreshTokenRepository,
)
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserLogin, UserRegister


class EmailAlreadyRegistered(Exception):
    """Raised when an email is already registered."""


class InvalidCredentials(Exception):
    """Raised when login credentials are invalid."""


class InvalidRefreshToken(Exception):
    """Raised when a refresh token is invalid, expired, or revoked."""


class AuthService:
    """Business logic for authentication and token management."""

    def __init__(
        self,
        user_repository: UserRepository,
        refresh_repository: RefreshTokenRepository,
    ) -> None:
        self.user_repository = user_repository
        self.refresh_repository = refresh_repository

    def _issue_tokens(self, user: User) -> dict[str, str]:
        """Generate an access token and persist a hashed refresh token."""
        now = datetime.now(timezone.utc)
        raw_refresh_token = create_refresh_token()

        refresh_record = RefreshToken(
            user_id=user.id,
            token_hash=hash_refresh_token(raw_refresh_token),
            expires_at=now
            + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )

        self.refresh_repository.save(refresh_record)

        return {
            "access_token": create_access_token(str(user.id)),
            "refresh_token": raw_refresh_token,
            "token_type": "bearer",
        }

    def register(self, data: UserRegister) -> User:
        """Register a new user."""
        email = str(data.email).strip().lower()

        if self.user_repository.get_by_email(email) is not None:
            raise EmailAlreadyRegistered

        try:
            return self.user_repository.create(
                email=email,
                first_name=data.first_name,
                last_name=data.last_name,
                password_hash=hash_password(data.password),
            )
        except IntegrityError as exc:
            # Handles a concurrent registration with the same email.
            # Ideally, distinguish the email uniqueness constraint from
            # other database integrity errors.
            raise EmailAlreadyRegistered from exc

    def login(self, data: UserLogin) -> dict[str, str]:
        """Validate credentials and issue both tokens."""
        email = str(data.email).strip().lower()
        user = self.user_repository.get_by_email(email)

        if user is None or not verify_password(
            data.password,
            user.password_hash,
        ):
            raise InvalidCredentials

        try:
            tokens = self._issue_tokens(user)
            self.refresh_repository.commit()
            return tokens
        except Exception:
            self.refresh_repository.rollback()
            raise

    def refresh(self, raw_token: str) -> dict[str, str]:
        """Rotate a refresh token and issue a new pair of tokens."""
        token_hash = hash_refresh_token(raw_token)

        try:
            # get_by_hash() should use SELECT ... FOR UPDATE.
            record = self.refresh_repository.get_by_hash(token_hash)

            if record is None:
                raise InvalidRefreshToken

            now = datetime.now(timezone.utc)

            # PostgreSQL normally returns timezone-aware values for
            # TIMESTAMP WITH TIME ZONE columns.
            expires_at = record.expires_at
            if expires_at.tzinfo is None:
                expires_at = expires_at.replace(tzinfo=timezone.utc)

            if record.revoked_at is not None or expires_at <= now:
                raise InvalidRefreshToken

            user = self.user_repository.get_by_id(record.user_id)

            if user is None:
                raise InvalidRefreshToken

            # Revoke the old token and save its replacement in the
            # same database transaction.
            self.refresh_repository.revoke(record)
            tokens = self._issue_tokens(user)
            self.refresh_repository.commit()

            return tokens

        except InvalidRefreshToken:
            self.refresh_repository.rollback()
            raise
        except Exception:
            self.refresh_repository.rollback()
            raise

    def logout(self, raw_token: str) -> None:
        """Revoke a refresh token if it is still active."""
        try:
            record = self.refresh_repository.get_by_hash(
                hash_refresh_token(raw_token)
            )

            if record is None or record.revoked_at is not None:
                self.refresh_repository.rollback()
                return

            self.refresh_repository.revoke(record)
            self.refresh_repository.commit()

        except Exception:
            self.refresh_repository.rollback()
            raise