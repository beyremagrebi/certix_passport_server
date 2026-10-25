from app.models.user import User


def member_to_dict(user: User) -> dict:
    """Admin-facing view of a member (never includes the password hash)."""
    return {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role": user.role.value,
        "is_active": user.is_active,
        "public_slug": user.public_slug,
        "created_at": user.created_at.isoformat(),
    }