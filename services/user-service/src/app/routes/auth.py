from flask import Blueprint

from app.controllers.auth import register, login, refresh, logout

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

auth_bp.add_url_rule("/register", view_func=register, methods=["POST"])
auth_bp.add_url_rule("/login", view_func=login, methods=["POST"])
auth_bp.add_url_rule("/refresh", view_func=refresh, methods=["POST"])
auth_bp.add_url_rule("/logout", view_func=logout, methods=["POST"])