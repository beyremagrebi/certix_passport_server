
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        return self.db.scalar(statement)

    def create(
        self,
        *,
        email: str,
        first_name: str,
        last_name: str,
        password_hash: str,
    ) -> User:
        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password_hash=password_hash,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user
