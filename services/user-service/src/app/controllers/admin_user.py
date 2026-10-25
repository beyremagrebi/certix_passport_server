from flask import request
from flask_jwt_extended import get_jwt_identity

from app.decorators.authorization import roles_required
from app.models.user_role import UserRole
from app.services.admin_user import AdminUserError, AdminUserService
from app.utils.api_response import error_response, success_response
from app.validators.admin_user import (
    validate_member_filters,
    validate_member_update,
)
from app.validators.user import validate_user_id


@roles_required(UserRole.ADMIN)
def list_members():
    try:
        filters = validate_member_filters(request.args)
        data = AdminUserService.list_members(filters)

        return success_response(
            message="Members retrieved successfully.",
            data=data,
        )

    except ValueError as exc:
        return error_response(
            message=str(exc),
            code="VALIDATION_ERROR",
            status_code=400,
        )


@roles_required(UserRole.ADMIN)
def update_member(user_id: int):
    try:
        actor_id = validate_user_id(get_jwt_identity())
        changes = validate_member_update(request.get_json(silent=True))
        data = AdminUserService.update_member(actor_id, user_id, changes)

        return success_response(
            message="Member updated successfully.",
            data=data,
        )

    except ValueError as exc:
        return error_response(
            message=str(exc),
            code="VALIDATION_ERROR",
            status_code=400,
        )

    except LookupError as exc:
        return error_response(
            message=str(exc),
            code="USER_NOT_FOUND",
            status_code=404,
        )

    except AdminUserError as exc:
        return error_response(
            message=str(exc),
            code=exc.code,
            status_code=exc.status_code,
        )