from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_refresh_token,
    verify_password,
)


class TokenService:
    """Responsible for token operations and password verification."""

    def issue_access_token(self, user_id: int) -> str:
        return create_access_token(str(user_id))

    def issue_refresh_token(self) -> str:
        return create_refresh_token()

    def hash_refresh_token(self, token: str) -> str:
        return hash_refresh_token(token)

    def verify_user_password(
        self,
        plain_password: str,
        password_hash: str,
    ) -> bool:
        return verify_password(plain_password, password_hash)