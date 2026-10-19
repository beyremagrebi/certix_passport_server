from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    """Handle database operations for users."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        """Find a user by email."""
        statement = select(User).where(User.email == email)
        return self.db.scalar(statement)

    def get_by_id(self, user_id: int) -> User | None:
        """Find a user by primary key."""
        return self.db.get(User, user_id)

    def create(
        self,
        *,
        email: str,
        first_name: str,
        last_name: str,
        password_hash: str,
    ) -> User:
        """Create and persist a new user."""
        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password_hash=password_hash,
        )

        self.db.add(user)

        try:
            self.db.commit()
            self.db.refresh(user)
        except IntegrityError:
            self.db.rollback()
            raise

        return user