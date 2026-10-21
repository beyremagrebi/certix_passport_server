
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
            "role": (
                user.role.value
                if hasattr(user.role, "value")
                else user.role
            ),
        }
