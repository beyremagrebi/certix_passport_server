from flask import Flask
from werkzeug.exceptions import RequestEntityTooLarge

from app.utils.api_response import error_response


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(RequestEntityTooLarge)
    def handle_request_entity_too_large(_error):
        return error_response(
            message="Request exceeds the maximum allowed file size.",
            code="FILE_TOO_LARGE",
            status_code=413,
        )