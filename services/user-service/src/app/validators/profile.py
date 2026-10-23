from urllib.parse import urlparse


PROFILE_FIELDS = {
    "first_name": 100,
    "last_name": 100,
    "bio": 300,
    "study_program": 100,
    "level": 50,
    "linkedin_url": 255,
    "github_url": 255,
}

URL_FIELDS = {"linkedin_url", "github_url"}
REQUIRED_FIELDS = {"first_name", "last_name"}


def validate_profile_update(data: object) -> dict[str, str | None]:
    if not isinstance(data, dict):
        raise ValueError("Request body must be a JSON object.")

    if not data:
        raise ValueError("At least one profile field is required.")

    if any(not isinstance(field, str) for field in data):
        raise ValueError("Profile field names must be strings.")

    unknown_fields = data.keys() - PROFILE_FIELDS.keys()
    if unknown_fields:
        field = sorted(unknown_fields)[0]
        raise ValueError(f"Unsupported profile field: {field}.")

    validated: dict[str, str | None] = {}

    for field, value in data.items():
        if value is None:
            if field in REQUIRED_FIELDS:
                raise ValueError(f"{field} cannot be null.")

            validated[field] = None
            continue

        if not isinstance(value, str):
            raise ValueError(f"{field} must be a string or null.")

        value = value.strip()

        if field in REQUIRED_FIELDS and not value:
            raise ValueError(f"{field} cannot be empty.")

        if len(value) > PROFILE_FIELDS[field]:
            raise ValueError(
                f"{field} must not exceed "
                f"{PROFILE_FIELDS[field]} characters."
            )

        if field in URL_FIELDS and value and not _is_valid_url(value):
            raise ValueError(
                f"{field} must be a valid HTTP or HTTPS URL."
            )

        validated[field] = value or None

    return validated


def _is_valid_url(value: str) -> bool:
    try:
        parsed = urlparse(value)

        return (
            parsed.scheme in {"http", "https"}
            and bool(parsed.hostname)
            and "." in parsed.hostname
            and not any(char.isspace() for char in value)
            and parsed.port != 0
        )
    except ValueError:
        return False