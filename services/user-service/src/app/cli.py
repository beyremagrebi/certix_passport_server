from app import create_app, check_database_connection
from app.config import Config


def main() -> None:
    app = create_app()

    with app.app_context():
        check_database_connection()

    app.run(
        debug=True,
        use_reloader=True,
        port=Config.PORT,
    )


