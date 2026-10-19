
import uvicorn

from app.core.config import settings


def display_startup_info() -> None:
    """Display service information before starting the server."""
    base_url = f"http://{settings.host}:{settings.port}"
    environment = "Development" if settings.debug else "Production"

    print()
    print("╭──────────────────────────────────────────────────╮")
    print(f"│  {settings.app_name:<48}│")
    print("├──────────────────────────────────────────────────┤")
    print(f"│  Environment : {environment:<34}│")
    print(f"│  Host        : {settings.host:<34}│")
    print(f"│  Port        : {settings.port:<34}│")
    print(f"│  API         : {base_url:<34}│")
    print(f"│  Swagger     : {(base_url + '/docs'):<34}│")
    print("╰──────────────────────────────────────────────────╯")
    print()


def main() -> None:
    display_startup_info()

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info" if settings.debug else "warning",
        access_log=True,
    )


if __name__ == "__main__":
    main()
