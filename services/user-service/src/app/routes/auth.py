from flask import Blueprint

from app.controllers.auth import (
    login,
    logout,
    refresh,
    register,
    request_password_reset,
    reset_password,
)

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

auth_bp.add_url_rule("/register", view_func=register, methods=["POST"])
auth_bp.add_url_rule("/login", view_func=login, methods=["POST"])
auth_bp.add_url_rule(
    "/forgot-password",
    view_func=request_password_reset,
    methods=["POST"],
)
auth_bp.add_url_rule(
    "/reset-password",
    view_func=reset_password,
    methods=["GET", "POST"],
)
auth_bp.add_url_rule("/refresh", view_func=refresh, methods=["POST"])
auth_bp.add_url_rule("/logout", view_func=logout, methods=["POST"])