from flask import Flask

from app.routes.health import health_bp
from app.routes.auth import auth_bp
from app.routes.admin import admin_bp
from app.routes.user import user_bp
from app.routes.profile import profile_bp
from app.routes.email_confirmation import email_confirmation_bp


def register_routes(app: Flask) -> None:
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(email_confirmation_bp)
