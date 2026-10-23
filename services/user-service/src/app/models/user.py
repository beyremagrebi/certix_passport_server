from sqlalchemy import Enum as SQLAlchemyEnum, String
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import (
    check_password_hash,
    generate_password_hash,
)

from app.models.base import BaseModel
from app.models.user_role import UserRole


class User(BaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )
    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    role: Mapped[UserRole] = mapped_column(
        SQLAlchemyEnum(
            UserRole,
            name="user_role",
            values_callable=lambda enum_cls: [
                role.value for role in enum_cls
            ],
        ),
        nullable=False,
        default=UserRole.STUDENT,
        server_default=UserRole.STUDENT.value,
    )
    profile_photo_ref: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )
    bio: Mapped[str | None] = mapped_column(String(300), nullable=True)
    study_program: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )
    level: Mapped[str | None] = mapped_column(String(50), nullable=True)
    linkedin_url: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )
    github_url: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)