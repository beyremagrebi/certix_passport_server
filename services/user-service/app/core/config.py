
import os

from dotenv import load_dotenv

load_dotenv()

class Settings:
    app_name: str = os.getenv(
        "APP_NAME", "Certix Passport - User Service"
    )
    app_version: str = os.getenv("APP_VERSION", "0.1.0")
    host: str = os.getenv("HOST", "127.0.0.1")
    port: int = int(os.getenv("PORT", "8001"))
    debug: bool = os.getenv("DEBUG", "true").lower() in ("true", "1", "yes", "on")
    database_url: str = os.getenv("DATABASE_URL", "")


settings = Settings() 
