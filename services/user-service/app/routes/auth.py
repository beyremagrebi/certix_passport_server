from app.validators.auth_validator import AuthValidator
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers.auth_controller import AuthController
from app.db.session import get_db
from app.repositories.user_repository import UserRepository
from app.repositories.refresh_token_repository import (
    RefreshTokenRepository,
)
from app.services.auth_service import AuthService
from app.schemas.user import UserLogin, UserRegister, RefreshRequest
from app.services.token_service import TokenService
from app.services.refresh_token_service import RefreshTokenService

router = APIRouter(prefix="/auth", tags=["Authentication"])





def get_auth_controller(db: Session = Depends(get_db)) -> AuthController:
    user_repository = UserRepository(db)
    refresh_repository = RefreshTokenRepository(db)

    token_service = TokenService()
    refresh_token_service = RefreshTokenService(
        refresh_repository,
        token_service,
    )

    validator = AuthValidator(
        user_repository=user_repository,
        refresh_token_service=refresh_token_service,
    )

    service = AuthService(
        user_repository=user_repository,
        refresh_repository=refresh_repository,
        token_service=token_service,
        refresh_token_service=refresh_token_service,
        validator=validator,
    )

    return AuthController(service)



@router.post("/register", status_code=201)
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


@router.post("/refresh")
def refresh(
    data: RefreshRequest,
    controller: AuthController = Depends(get_auth_controller),
):
    return controller.refresh(data.refresh_token)


@router.post("/logout")
def logout(
    data: RefreshRequest,
    controller: AuthController = Depends(get_auth_controller),
):
    return controller.logout(data.refresh_token)