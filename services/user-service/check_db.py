
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import engine


def main() -> None:
    print("Checking PostgreSQL connection...")

    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print(f"Connection successful. Test result: {result.scalar()}")

    except SQLAlchemyError as exc:
        print(f"Connection failed: {type(exc).__name__}")
        print(f"Details: {exc}")


if __name__ == "__main__":
    main()
