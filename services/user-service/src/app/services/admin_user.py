from app.extensions import db
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.repositories.user_repository import UserRepository
from app.schemas.member import member_to_dict


class AdminUserError(Exception):
    def __init__(self, message: str, code: str, status_code: int):
        super().__init__(message)
        self.code = code
        self.status_code = status_code


class AdminUserService:
    @staticmethod
    def list_members(filters: dict) -> dict:
        pagination = UserRepository.paginate_members(**filters)

        return {
            "items": [member_to_dict(user) for user in pagination.items],
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
            "pages": pagination.pages,
        }

    @staticmethod
    def update_member(actor_id: int, target_id: int, changes: dict) -> dict:
        user = UserRepository.get_by_id(target_id)
        if user is None:
            raise LookupError("User not found.")

        # An admin cannot lock themselves out or remove their own rights.
        if actor_id == user.id:
            raise AdminUserError(
                "Admins cannot change their own role or status.",
                "SELF_MODIFICATION_FORBIDDEN",
                403,
            )

        applied = {
            field: value
            for field, value in changes.items()
            if getattr(user, field) != value
        }

        # Nothing to change: the request is idempotent.
        if not applied:
            return member_to_dict(user)

        try:
            for field, value in applied.items():
                setattr(user, field, value)

            # A deactivated member must not be able to renew their session.
            if applied.get("is_active") is False:
                RefreshTokenRepository.revoke_all_for_user(user.id)

            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

        return member_to_dict(user)