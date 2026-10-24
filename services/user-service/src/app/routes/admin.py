from flask import Blueprint

from app.controllers.admin_user import list_members, update_member
from app.models.user_role import UserRole
from app.decorators.authorization import roles_required
from app.utils.api_response import success_response

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.get("/dashboard")
@roles_required(UserRole.ADMIN)
def dashboard():
    return success_response(
        "Admin access granted.",
        {"section": "dashboard"},
    )



admin_bp.add_url_rule("/users", view_func=list_members, methods=["GET"])
admin_bp.add_url_rule(
    "/users/<int:user_id>", view_func=update_member, methods=["PATCH"]
)