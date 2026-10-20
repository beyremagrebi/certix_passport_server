import logging
from sqlalchemy import text
from app.extensions import db

import logging


def check_database_connection() -> None:
    try:
        db.session.execute(text("SELECT 1"))
        print("PostgreSQL DB connection successful")
    except Exception:
        print("PostgreSQL DB connection failed")
        raise