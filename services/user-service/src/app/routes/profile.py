from flask import Blueprint

from app.controllers.profile import (
    upload_profile_photo,
)

profile_bp = Blueprint("profile", __name__, url_prefix="/users/me")


profile_bp.add_url_rule("/profile-photo",view_func=upload_profile_photo,methods=["POST"])
