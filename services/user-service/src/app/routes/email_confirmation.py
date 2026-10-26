from flask import Blueprint

from app.controllers.email_confirmation import confirm_email


email_confirmation_bp = Blueprint(
    "email_confirmation",
    __name__,
    url_prefix="/auth",
)

email_confirmation_bp.add_url_rule(
    "/confirm-email",
    view_func=confirm_email,
    methods=["GET"],
)
