import os
from pathlib import Path

from dotenv import load_dotenv
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env", override=False)


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PORT = int(os.getenv("PORT", "5000"))
    PROFILE_PHOTO_STORAGE_DIR = Path(
        os.getenv("PROFILE_PHOTO_STORAGE_DIR", str(BASE_DIR / "storage" / "profile-photos"))
    )
    PROFILE_PHOTO_MAX_BYTES = int(
        os.getenv("PROFILE_PHOTO_MAX_BYTES", str(5 * 1024 * 1024))
    )
    MAX_CONTENT_LENGTH = PROFILE_PHOTO_MAX_BYTES + 1024 * 1024
    PROFILE_PHOTO_MAX_WIDTH = int(os.getenv("PROFILE_PHOTO_MAX_WIDTH", "2048"))
    PROFILE_PHOTO_MAX_HEIGHT = int(os.getenv("PROFILE_PHOTO_MAX_HEIGHT", "2048"))
    PROFILE_PHOTO_ALLOWED_FORMATS = frozenset(
        format_name.strip().upper()
        for format_name in os.getenv(
            "PROFILE_PHOTO_ALLOWED_FORMATS", "JPEG,PNG,WEBP"
        ).split(",")
        if format_name.strip()
    )

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_MINUTES", "15"))
    )

    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        days=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES_DAYS", "30"))
    )
