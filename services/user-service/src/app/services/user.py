from app.repositories.user_repository import UserRepository
from app.validators.user import validate_user_id
from app.schemas.user import user_to_dict


class UserService:

    @staticmethod
    def _get_user(user_id):
        validated_id = validate_user_id(user_id)
        user = UserRepository.get_by_id(validated_id)

        if user is None:
            raise LookupError("User not found.")

        return user

    @staticmethod
    def get_me(user_id):
        user = UserService._get_user(user_id)
        return user_to_dict(user)


    @staticmethod
    def update_profile(user_id, profile_data):
        user = UserService._get_user(user_id)

        UserRepository.update_profile(user, profile_data)

        return user_to_dict(user)