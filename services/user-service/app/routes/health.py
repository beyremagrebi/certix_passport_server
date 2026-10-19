
from fastapi import APIRouter

from app.utils.response import success_response

router = APIRouter()


@router.get("/health", tags=["Health"])
def health_check():
    return success_response(
        message="User Service is healthy",
        data={
            "status": "ok",
            "service": "user-service",
        },
    )
