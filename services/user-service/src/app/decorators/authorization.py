
from functools import wraps
from typing import Callable

from flask_jwt_extended import get_jwt_identity, jwt_required

from app.extensions import db
from app.models.user import User
from app.models.user_role import UserRole
from app.utils.api_response import error_response


def roles_required(*allowed_roles: UserRole):
    def decorator(view: Callable):
        @wraps(view)
        @jwt_required()
        def wrapped(*args, **kwargs):
            user_id = get_jwt_identity()

            try:
                user = db.session.get(User, int(user_id))
            except (TypeError, ValueError):
                user = None

            if user is None:
                return error_response(
                    "User not found.",
                    "UNAUTHORIZED",
                    401,
                )

            if user.role not in allowed_roles:
                return error_response(
                    "You do not have permission to access this resource.",
                    "FORBIDDEN",
                    403,
                )

            return view(*args, **kwargs)

        return wrapped

    return decorator
