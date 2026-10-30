
from flask import Flask, g, request
from flask_jwt_extended import (
    get_jwt_identity,
    verify_jwt_in_request,
)
from flask_jwt_extended.exceptions import JWTExtendedException

from app.utils.api_response import error_response


# Routes handled without global JWT authentication.
# refresh/logout keep their own @jwt_required(refresh=True).
EXEMPT_ENDPOINTS = {
    "auth.register",
    "auth.login",
    "auth.request_password_reset",
    "auth.reset_password",
    "auth.refresh",
    "auth.logout",
    "email_confirmation.confirm_email",
    "health.health_check",
}


def register_jwt_middleware(app: Flask) -> None:
    @app.before_request
    def authenticate_request():
        endpoint = request.endpoint
        print("JWT middleware endpoint:", endpoint)

        # Let Flask handle unmatched URLs normally (404).
        if endpoint is None:
            return None

        # Public routes or routes with their own JWT decorator.
        if endpoint in EXEMPT_ENDPOINTS:
            return None

        try:
            verify_jwt_in_request()
            g.current_user_id = get_jwt_identity()

        except JWTExtendedException:
            return error_response(
                message="Missing or invalid access token.",
                code="UNAUTHORIZED",
                status_code=401,
            )

        return None
