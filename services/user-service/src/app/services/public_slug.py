from app.repositories.user_repository import UserRepository
from app.utils.slug import generate_slug


class PublicSlugService:
    MAX_ATTEMPTS = 10

    @staticmethod
    def generate_unique(first_name: str, last_name: str) -> str:
        """Return a public slug that is not used by any user yet."""
        for _ in range(PublicSlugService.MAX_ATTEMPTS):
            candidate = generate_slug(first_name, last_name)
            if not UserRepository.public_slug_exists(candidate):
                return candidate

        raise RuntimeError("Could not generate a unique public slug.")
