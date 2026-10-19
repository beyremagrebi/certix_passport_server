
from sqlalchemy.exc import IntegrityError

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserLogin, UserRegister


class EmailAlreadyRegistered(Exception):
    pass


class InvalidCredentials(Exception):
    pass


class AuthService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def register(self, data: UserRegister) -> User:
        email = str(data.email).strip().lower()

        if self.user_repository.get_by_email(email):
            raise EmailAlreadyRegistered

        hashed_password = hash_password(data.password)

        try:
            return self.user_repository.create(
                email=email,
                first_name=data.first_name,
                last_name=data.last_name,
                password_hash=hashed_password,
            )
        except IntegrityError as exc:
            # Handles a concurrent registration with the same email.
            raise EmailAlreadyRegistered from exc

    def login(self, data: UserLogin) -> str:
        email = str(data.email).strip().lower()
        user = self.user_repository.get_by_email(email)

        if user is None or not verify_password(
            data.password,
            user.password_hash,
        ):
            raise InvalidCredentials

        return create_access_token(subject=str(user.id))
