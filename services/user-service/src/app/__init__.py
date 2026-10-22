
import logging

from app.middlewares.jwt_middleware import register_jwt_middleware
from flask import Flask
from werkzeug.exceptions import RequestEntityTooLarge

from app.config import Config
from app.database import check_database_connection
from app.extensions import init_extensions
from app.routes import register_routes
from app.utils.api_response import error_response

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    init_extensions(app)
    register_jwt_middleware(app)
    register_routes(app)
    

    @app.errorhandler(RequestEntityTooLarge)
    def handle_request_entity_too_large(_error):
        return error_response(
            message="Request exceeds the maximum allowed file size.",
            code="FILE_TOO_LARGE",
            status_code=413,
        )

    return app


