from datetime import datetime, timedelta, timezone

from app.core.config import settings
from app.models.refresh_token import RefreshToken
from app.repositories.refresh_token_repository import (
    RefreshTokenRepository,
)
from app.services.token_service import TokenService


class RefreshTokenService:
    """Responsible for refresh-token persistence and revocation."""

    def __init__(
        self,
        repository: RefreshTokenRepository,
        token_service: TokenService,
    ) -> None:
        self.repository = repository
        self.token_service = token_service

    def create_for_user(self, user_id: int) -> str:
        raw_token = self.token_service.issue_refresh_token()

        record = RefreshToken(
            user_id=user_id,
            token_hash=self.token_service.hash_refresh_token(raw_token),
            expires_at=datetime.now(timezone.utc)
            + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )

        self.repository.save(record)
        return raw_token

    def get_by_raw_token(self, raw_token: str) -> RefreshToken | None:
        token_hash = self.token_service.hash_refresh_token(raw_token)
        return self.repository.get_by_hash(token_hash)

    def revoke(self, record: RefreshToken) -> None:
        self.repository.revoke(record)