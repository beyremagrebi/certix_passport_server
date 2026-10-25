from sqlalchemy import update

from app.extensions import db
from app.models.refresh_token import RefreshToken


class RefreshTokenRepository:
    @staticmethod
    def revoke_all_for_user(user_id: int) -> int:
        """Revoke every active refresh token of a user.

        Does not commit: the caller decides the transaction boundary.
        """
        result = db.session.execute(
            update(RefreshToken)
            .where(
                RefreshToken.user_id == user_id,
                RefreshToken.revoked.is_(False),
            )
            .values(revoked=True)
        )
        return result.rowcount