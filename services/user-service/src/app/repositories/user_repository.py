
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
    def create(user: User) -> User:
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_by_id(user_id: int):
        return db.session.get(User, user_id)
      
    def update_profile_photo(user: User, asset_ref: str) -> User:
        user.profile_photo_ref = asset_ref
        db.session.commit()
        return user
