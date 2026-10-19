
# app/schemas/user.py

from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)


class RequestSchema(BaseModel):
    """Common rules for incoming API data."""

    model_config = ConfigDict(extra="forbid")


class UserRegister(RequestSchema):
    """Data accepted when creating a new account."""

    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

    @field_validator("first_name", "last_name", mode="before")
    @classmethod
    def normalize_name(cls, value: object) -> object:
        if isinstance(value, str):
            value = value.strip()
            if not value:
                raise ValueError("Name cannot be empty or whitespace")
        return value


class UserLogin(RequestSchema):
    """Credentials accepted during login."""

    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class UserResponse(BaseModel):
    """Public user representation. Never expose password hashes."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(ge=1)
    first_name: str
    last_name: str
    email: EmailStr


class TokenResponse(BaseModel):
    """Authentication token returned after successful login."""

    access_token: str
    token_type: Literal["bearer"] = "bearer"
