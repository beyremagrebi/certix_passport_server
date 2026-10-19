
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.controllers.auth_controller import AuthController
from app.db.session import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserLogin, UserRegister
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_auth_controller(
    db: Session = Depends(get_db),
) -> AuthController:
    repository = UserRepository(db)
    service = AuthService(repository)
    return AuthController(service)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
)
def register(
    data: UserRegister,
    controller: AuthController = Depends(get_auth_controller),
):
    return controller.register(data)


@router.post("/login")
def login(
    data: UserLogin,
    controller: AuthController = Depends(get_auth_controller),
):
    return controller.login(data)
