
from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Shared configuration for API schemas."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        validate_assignment=True,
    )


class ORMBaseSchema(BaseSchema):
    """Base for schemas built from ORM objects."""

    model_config = ConfigDict(from_attributes=True)
