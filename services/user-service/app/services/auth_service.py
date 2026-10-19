from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.repositories.refresh_token_repository import (
    RefreshTokenRepository,
)
from app.schemas.user import UserLogin, UserRegister
from app.services.token_service import TokenService
from app.services.refresh_token_service import RefreshTokenService
from app.validators.auth_validator import (
    AuthValidator,
    EmailAlreadyRegistered,
    InvalidRefreshToken,
)


class AuthService:
    """Coordinates authentication use cases."""

    def __init__(
        self,
        user_repository: UserRepository,
        refresh_repository: RefreshTokenRepository,
        token_service: TokenService,
        refresh_token_service: RefreshTokenService,
        validator: AuthValidator,
    ) -> None:
        self.user_repository = user_repository
        self.refresh_repository = refresh_repository
        self.token_service = token_service
        self.refresh_token_service = refresh_token_service
        self.validator = validator

    def _issue_tokens(self, user: User) -> dict[str, str]:
        refresh_token = self.refresh_token_service.create_for_user(user.id)

        return {
            "access_token": self.token_service.issue_access_token(user.id),
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    def register(self, data: UserRegister) -> User:
        email = self.validator.validate_registration(data)

        from app.core.security import hash_password

        try:
            return self.user_repository.create(
                email=email,
                first_name=data.first_name,
                last_name=data.last_name,
                password_hash=hash_password(data.password),
            )
        except IntegrityError as exc:
            self.refresh_repository.rollback()
            raise EmailAlreadyRegistered from exc

    def login(self, data: UserLogin) -> dict[str, str]:
        user = self.validator.validate_login(data)

        try:
            tokens = self._issue_tokens(user)
            self.refresh_repository.commit()
            return tokens
        except Exception:
            self.refresh_repository.rollback()
            raise

    def refresh(self, raw_token: str) -> dict[str, str]:
        try:
            record = self.validator.validate_refresh_token(raw_token)

            user = self.user_repository.get_by_id(record.user_id)
            if user is None:
                raise InvalidRefreshToken

            self.refresh_token_service.revoke(record)
            tokens = self._issue_tokens(user)
            self.refresh_repository.commit()

            return tokens

        except Exception:
            self.refresh_repository.rollback()
            raise

    def logout(self, raw_token: str) -> None:
        try:
            record = self.refresh_token_service.get_by_raw_token(raw_token)

            if record is None or record.revoked_at is not None:
                self.refresh_repository.rollback()
                return

            self.refresh_token_service.revoke(record)
            self.refresh_repository.commit()

        except Exception:
            self.refresh_repository.rollback()
            raise