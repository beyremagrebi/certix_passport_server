
from flask import Flask, g, request
from flask_jwt_extended import (
    get_jwt_identity,
    verify_jwt_in_request,
)
from flask_jwt_extended.exceptions import JWTExtendedException

from app.repositories.user_repository import UserRepository
from app.utils.api_response import error_response


# Routes handled without global JWT authentication.
# refresh/logout keep their own @jwt_required(refresh=True).
EXEMPT_ENDPOINTS = {
    "auth.register",
    "auth.login",
    "auth.refresh",
    "auth.logout",
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

        # A token stays cryptographically valid for minutes after an admin
        # deactivates the account, so the account state is checked here.
        try:
            user = UserRepository.get_by_id(int(g.current_user_id))
        except (TypeError, ValueError):
            user = None

        if user is None:
            return error_response(
                message="Missing or invalid access token.",
                code="UNAUTHORIZED",
                status_code=401,
            )

        if not user.is_active:
            return error_response(
                message="This account has been deactivated.",
                code="ACCOUNT_DISABLED",
                status_code=403,
            )

        return None