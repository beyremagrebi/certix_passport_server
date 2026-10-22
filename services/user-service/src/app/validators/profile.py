from urllib.parse import urlparse


PROFILE_FIELDS = {
    "bio": 300,
    "study_program": 100,
    "level": 50,
    "linkedin_url": 255,
    "github_url": 255,
}


def validate_profile_update(data: object) -> dict[str, str | None]:
    if not isinstance(data, dict):
        raise ValueError("Request body must be a JSON object.")

    unknown_fields = set(data) - PROFILE_FIELDS.keys()
    if unknown_fields:
        field = sorted(unknown_fields)[0]
        raise ValueError(f"Unsupported profile field: {field}.")

    validated: dict[str, str | None] = {}
    for field, max_length in PROFILE_FIELDS.items():
        if field not in data:
            continue

        value = data[field]
        if value is None:
            validated[field] = None
            continue

        if not isinstance(value, str):
            raise ValueError(f"{field} must be a string or null.")

        value = value.strip()
        if len(value) > max_length:
            raise ValueError(
                f"{field} must not exceed {max_length} characters."
            )

        if field.endswith("_url") and value and not _is_valid_url(value):
            raise ValueError(f"{field} must be a valid URL.")

        validated[field] = value or None

    return validated


def _is_valid_url(value: str) -> bool:
    parsed = urlparse(value)
    return (
        parsed.scheme in {"http", "https"}
        and bool(parsed.hostname)
        and not any(char.isspace() for char in value)
    )
