from app.models.user import User


def user_to_dict(user: User) -> dict:
    return {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role": user.role.value,
        "profile_photo_ref": user.profile_photo_ref,
        "bio": user.bio,
        "study_program": user.study_program,
        "level": user.level,
        "linkedin_url": user.linkedin_url,
        "github_url": user.github_url,
    }