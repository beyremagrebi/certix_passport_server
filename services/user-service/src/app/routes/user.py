
from flask import Blueprint

from app.controllers.user import get_me

user_bp = Blueprint("user", __name__)

user_bp.add_url_rule("/me",view_func=get_me,methods=["GET"])
