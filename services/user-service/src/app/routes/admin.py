from flask import Blueprint

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