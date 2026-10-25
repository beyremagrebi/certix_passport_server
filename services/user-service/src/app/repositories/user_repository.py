
from app.extensions import db
from app.models.user import User


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
