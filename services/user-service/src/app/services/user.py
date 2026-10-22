
from app.repositories.user_repository import UserRepository
from app.validators.user import validate_user_id


class UserService:

    @staticmethod
    def get_me(user_id):
        validated_id = validate_user_id(user_id)

        user = UserRepository.get_by_id(validated_id)

        if user is None:
            raise LookupError("User not found.")

        return {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": (
                user.role.value
                if hasattr(user.role, "value")
                else user.role
            ),
        }

    @staticmethod
    def get_profile(user_id):
        validated_id = validate_user_id(user_id)
        user = UserRepository.get_by_id(validated_id)

        if user is None:
            raise LookupError("User not found.")

        return UserService._profile_data(user)

    @staticmethod
    def update_profile(user_id, profile_data):
        validated_id = validate_user_id(user_id)
        user = UserRepository.get_by_id(validated_id)

        if user is None:
            raise LookupError("User not found.")

        UserRepository.update_profile(user, profile_data)
        return UserService._profile_data(user)

    @staticmethod
    def _profile_data(user):
        return {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": (
                user.role.value
                if hasattr(user.role, "value")
                else user.role
            ),
            "profile_photo_ref": user.profile_photo_ref,
            "bio": user.bio,
            "study_program": user.study_program,
            "level": user.level,
            "linkedin_url": user.linkedin_url,
            "github_url": user.github_url,
        }
