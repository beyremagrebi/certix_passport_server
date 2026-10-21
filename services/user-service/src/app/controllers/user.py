
from flask_jwt_extended import get_jwt_identity

from app.services.user import UserService
from app.utils.api_response import success_response, error_response


def get_me():
    try:
        user_id = get_jwt_identity()
        user_data = UserService.get_me(user_id)

        return success_response(
            message="User profile retrieved successfully.",
            data=user_data,
        )

    except ValueError as exc:
        return error_response(
            message=str(exc),
            code="VALIDATION_ERROR",
            status_code=400,
        )

    except LookupError:
        return error_response(
            message="User not found.",
            code="USER_NOT_FOUND",
            status_code=404,
        )
