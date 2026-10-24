"""Helpers to build public profile slugs such as ``maki-test-482913``."""

import re
import secrets
import unicodedata

SLUG_SUFFIX_DIGITS = 6
SLUG_BASE_MAX_LENGTH = 60
SLUG_FALLBACK_BASE = "member"

_NON_ALPHANUMERIC = re.compile(r"[^a-z0-9]+")


def slugify(value: str) -> str:
    """Return a lowercase ASCII, hyphen-separated version of ``value``.

    Accents are stripped (``Élève`` -> ``eleve``) and every other character
    that is not a letter or a digit becomes a hyphen.
    """
    ascii_value = (
        unicodedata.normalize("NFKD", value)
        .encode("ascii", "ignore")
        .decode("ascii")
    )
    return _NON_ALPHANUMERIC.sub("-", ascii_value.lower()).strip("-")


def build_slug_base(first_name: str, last_name: str) -> str:
    """Return the ``firstname-lastname`` part of a slug.

    Falls back to a neutral word when the name has no ASCII letters
    (for example a name written only in Arabic script).
    """
    base = slugify(f"{first_name} {last_name}")[:SLUG_BASE_MAX_LENGTH]
    return base.strip("-") or SLUG_FALLBACK_BASE


def generate_slug(first_name: str, last_name: str) -> str:
    """Return ``firstname-lastname-<random digits>``.

    The suffix comes from ``secrets`` so slugs cannot be guessed or
    enumerated. Uniqueness is NOT guaranteed here: the caller checks it and
    the database unique constraint is the final guard.
    """
    suffix = f"{secrets.randbelow(10**SLUG_SUFFIX_DIGITS):0{SLUG_SUFFIX_DIGITS}d}"
    return f"{build_slug_base(first_name, last_name)}-{suffix}"
