"""Helpers for the free-text search used by list endpoints."""

MAX_SEARCH_TERMS = 5


def escape_like(value: str) -> str:
    """Escape the characters that have a special meaning in SQL LIKE.

    Without this, a search for ``100%`` or ``a_b`` would behave like a
    wildcard pattern instead of a plain text search.
    """
    return (
        value.replace("\\", "\\\\")
        .replace("%", "\\%")
        .replace("_", "\\_")
    )


def parse_search_terms(query: str) -> list[str]:
    """Split a search string into at most ``MAX_SEARCH_TERMS`` words."""
    return query.split()[:MAX_SEARCH_TERMS]