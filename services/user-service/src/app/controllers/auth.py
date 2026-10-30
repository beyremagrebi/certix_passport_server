from flask import request, render_template_string
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from app.utils.api_response import success_response, error_response
from app.validators.auth import (
    validate_login,
    validate_password_reset,
    validate_password_reset_request,
    validate_registration,
)
from app.services.auth import AuthService, AuthError
from app.services.email_confirmation import EmailConfirmationError
from app.services.password_reset import PasswordResetService


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

    except EmailConfirmationError as exc:
        return error_response(
            message=str(exc),
            code="EMAIL_DELIVERY_ERROR",
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


def request_password_reset():
    try:
        data = validate_password_reset_request(request.get_json(silent=True))
        PasswordResetService.request_reset(data["email"])
        return success_response(
            message=(
                "If an account exists for this email, a password reset link "
                "has been sent."
            ),
            status_code=202,
        )
    except ValueError as exc:
        return error_response(
            message=str(exc),
            code="VALIDATION_ERROR",
            status_code=400,
        )


def reset_password():
    if request.method == "GET":
        token = request.args.get("token", "")
        if not token:
            return "Invalid or missing password reset token.", 400
        return render_template_string(
            """
            <!doctype html>
            <title>Reset password</title>
            <h1>Reset your password</h1>
            <form method="post">
                <input type="hidden" name="token" value="{{ token }}">
                <label>
                    New password
                    <input type="password" name="new_password"
                           minlength="8" maxlength="128" required>
                </label>
                <br><br>
                <label>
                    Confirm new password
                    <input type="password" name="confirm_password"
                           minlength="8" maxlength="128" required>
                </label>
                <br><br>
                <button type="submit">Reset password</button>
            </form>
            """,
            token=token,
        )

    if request.form:
        token = request.form.get("token", "")
        new_password = request.form.get("new_password", "")
        confirm_password = request.form.get("confirm_password", "")
        if new_password != confirm_password:
            return "Passwords do not match.", 400
        data = {"token": token, "new_password": new_password}
    else:
        data = request.get_json(silent=True)

    try:
        data = validate_password_reset(data)
        PasswordResetService.reset_password(
            raw_token=data["token"],
            new_password=data["new_password"],
        )
        if request.form:
            return "<h1>Password reset successfully.</h1>"
        return success_response(message="Password reset successfully.")
    except ValueError as exc:
        return error_response(
            message=str(exc),
            code="PASSWORD_RESET_ERROR",
            status_code=400,
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
