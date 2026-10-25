from collections.abc import Mapping

from app.models.user_role import UserRole
from app.utils.search import parse_search_terms

MAX_QUERY_LENGTH = 100
DEFAULT_PAGE = 1
DEFAULT_PER_PAGE = 20
MAX_PER_PAGE = 100

UPDATABLE_FIELDS = frozenset({"role", "is_active"})
_ALLOWED_ROLES = ", ".join(role.value for role in UserRole)


def _parse_role(raw: object) -> UserRole:
    try:
        return UserRole(raw)
    except (ValueError, TypeError):
        raise ValueError(f"Invalid role. Allowed values: {_ALLOWED_ROLES}.") from None


def _parse_int(
    raw: str | None,
    name: str,
    default: int,
    minimum: int,
    maximum: int | None = None,
) -> int:
    if raw is None or raw == "":
        return default

    try:
        value = int(raw)
    except ValueError:
        raise ValueError(f"{name} must be an integer.") from None

    if value < minimum or (maximum is not None and value > maximum):
        if maximum is None:
            raise ValueError(f"{name} must be at least {minimum}.")
        raise ValueError(f"{name} must be between {minimum} and {maximum}.")

    return value


def validate_member_filters(args: Mapping[str, str]) -> dict:
    """Validate the query string of ``GET /admin/users``."""
    query = (args.get("q") or "").strip()
    if len(query) > MAX_QUERY_LENGTH:
        raise ValueError(f"q must not exceed {MAX_QUERY_LENGTH} characters.")

    raw_role = args.get("role")
    role = _parse_role(raw_role) if raw_role else None

    raw_active = args.get("is_active")
    if raw_active in (None, ""):
        is_active = None
    elif raw_active in ("true", "false"):
        is_active = raw_active == "true"
    else:
        raise ValueError("is_active must be 'true' or 'false'.")

    return {
        "terms": parse_search_terms(query),
        "role": role,
        "is_active": is_active,
        "page": _parse_int(args.get("page"), "page", DEFAULT_PAGE, 1),
        "per_page": _parse_int(
            args.get("per_page"), "per_page", DEFAULT_PER_PAGE, 1, MAX_PER_PAGE
        ),
    }


def validate_member_update(data: object) -> dict:
    """Validate the JSON body of ``PATCH /admin/users/<id>``.

    Returns only the fields that were provided, already converted
    (``role`` becomes a ``UserRole``).
    """
    if not isinstance(data, dict):
        raise ValueError("Request body must be a JSON object.")

    unknown = set(data) - UPDATABLE_FIELDS
    if unknown:
        raise ValueError(f"Unknown field(s): {', '.join(sorted(unknown))}.")

    if not data:
        raise ValueError("Provide at least one field to update: role, is_active.")

    changes: dict = {}

    if "role" in data:
        changes["role"] = _parse_role(data["role"])

    if "is_active" in data:
        if not isinstance(data["is_active"], bool):
            raise ValueError("is_active must be a boolean.")
        changes["is_active"] = data["is_active"]

    return changes