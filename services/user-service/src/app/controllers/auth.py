from flask import request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from app.utils.api_response import success_response, error_response
from app.validators.auth import validate_login, validate_registration
from app.services.auth import AuthService, AuthError


def register():
    try:
        data = validate_registration(request.get_json(silent=True))
        result = AuthService.register(data)

        return success_response(
            message="Registration successful.",
            data=result,
            status_code=201,
        )

    except ValueError as exc:
        return error_response(
            message=str(exc),
            code="VALIDATION_ERROR",
            status_code=400,
        )

    except AuthError as exc:
        return error_response(
            message=str(exc),
            code="AUTH_ERROR",
            status_code=exc.status_code,
        )


def login():
    try:
        data = validate_login(request.get_json(silent=True))
        result = AuthService.login(data)

        return success_response(
            message="Login successful.",
            data=result,
        )

    except ValueError as exc:
        return error_response(
            message=str(exc),
            code="VALIDATION_ERROR",
            status_code=400,
        )

    except AuthError as exc:
        return error_response(
            message=str(exc),
            code="AUTH_ERROR",
            status_code=exc.status_code,
        )


@jwt_required(refresh=True)
def refresh():
    try:
        result = AuthService.refresh(
            user_id=get_jwt_identity(),
            old_jti=get_jwt()["jti"],
        )

        return success_response(
            message="Token refreshed successfully.",
            data=result,
        )

    except AuthError as exc:
        return error_response(
            message="Token refresh failed.",
            code="AUTH_ERROR",
            status_code=exc.status_code,
        )


@jwt_required(refresh=True)
def logout():
    try:
        claims = get_jwt()

        AuthService.logout(
            jti=claims["jti"],
            user_id=get_jwt_identity(),
        )

        return success_response(
            message="Logged out successfully.",
            data=None,
        )

    except AuthError as exc:
        return error_response(
            message="Logout failed.",
            code="AUTH_ERROR",
            status_code=exc.status_code,
        )
