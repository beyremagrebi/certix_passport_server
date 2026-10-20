
import logging

from flask import Flask

from app.config import Config
from app.database import check_database_connection
from app.extensions import init_extensions
from app.routes import register_routes

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    init_extensions(app)
    register_routes(app)

    return app



