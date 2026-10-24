
from sqlalchemy import or_

from app.extensions import db
from app.models.user import User
from app.models.user_role import UserRole
from app.utils.search import escape_like


class UserRepository:
    @staticmethod
    def get_by_id(user_id: int) -> User | None:
        return db.session.get(User, user_id)

    @staticmethod
    def get_by_email(email: str) -> User | None:
        return db.session.execute(
            db.select(User).where(User.email == email)
        ).scalar_one_or_none()

    @staticmethod
    def public_slug_exists(slug: str) -> bool:
        return (
            db.session.execute(
                db.select(User.id).where(User.public_slug == slug).limit(1)
            ).first()
            is not None
        )

    @staticmethod
    def paginate_members(
        *,
        terms: list[str],
        role: UserRole | None,
        is_active: bool | None,
        page: int,
        per_page: int,
    ):
        query = db.select(User)

        # Every word must match the first name, last name or email, so
        # "maki test" finds "Maki Test" while "maki zzz" finds nobody.
        for term in terms:
            pattern = f"%{escape_like(term)}%"
            query = query.where(
                or_(
                    User.first_name.ilike(pattern, escape="\\"),
                    User.last_name.ilike(pattern, escape="\\"),
                    User.email.ilike(pattern, escape="\\"),
                )
            )

        if role is not None:
            query = query.where(User.role == role)

        if is_active is not None:
            query = query.where(User.is_active == is_active)

        return db.paginate(
            query.order_by(User.id.desc()),
            page=page,
            per_page=per_page,
            max_per_page=100,
            error_out=False,
        )

    @staticmethod
    def create(user: User) -> User:
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_by_id(user_id: int):
        return db.session.get(User, user_id)

    @staticmethod
    def update_profile_photo(user: User, asset_ref: str) -> None:
        user.profile_photo_ref = asset_ref
        db.session.add(user)

    @staticmethod
    def update_profile(user: User, profile_data: dict) -> User:
        allowed_fields = {
            "first_name",
            "last_name",
            "bio",
            "study_program",
            "level",
            "linkedin_url",
            "github_url",
        }

        for field, value in profile_data.items():
            if field in allowed_fields:
                setattr(user, field, value)

        db.session.commit()
        return user
