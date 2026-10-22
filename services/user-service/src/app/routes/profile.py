from flask import Blueprint

from app.controllers.profile import (
    get_profile,
    update_profile,
    upload_profile_photo,
)

profile_bp = Blueprint("profile", __name__, url_prefix="/users/me")

profile_bp.add_url_rule(
    "/profile",
    view_func=get_profile,
    methods=["GET"],
)
profile_bp.add_url_rule(
    "/profile",
    view_func=update_profile,
    methods=["PATCH", "PUT"],
)
profile_bp.add_url_rule(
    "/profile-photo",
    view_func=upload_profile_photo,
    methods=["POST"],
)
