from flask import request

from app.services.email_confirmation import (
    EmailConfirmationError,
    EmailConfirmationService,
)
from app.utils.api_response import error_response, success_response


def confirm_email():
    try:
        EmailConfirmationService.confirm(request.args.get("token", ""))
        return success_response(
            message="Email confirmed successfully.",
            data=None,
        )
    except EmailConfirmationError as exc:
        return error_response(
            message=str(exc),
            code="EMAIL_CONFIRMATION_ERROR",
            status_code=exc.status_code,
        )
