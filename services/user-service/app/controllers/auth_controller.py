from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.schemas.user import UserLogin, UserRegister, UserResponse
from app.services.auth_service import AuthService

from app.validators.auth_validator import (
    EmailAlreadyRegistered,
    InvalidCredentials,
    InvalidRefreshToken,
)
from app.utils.response import success_response, error_response


class AuthController:
    def __init__(self, auth_service: AuthService) -> None:
        self.auth_service = auth_service

    def register(self, data: UserRegister) -> JSONResponse:
        try:
            user = self.auth_service.register(data)
        except EmailAlreadyRegistered:
            return error_response(
                message="Email is already registered",
                status_code=409,
            )

        safe_user = UserResponse.model_validate(user).model_dump(mode="json")

        return success_response(
            data=safe_user,
            message="User registered successfully",
            status_code=201,
        )

    def login(self, data: UserLogin) -> JSONResponse:
        try:
            tokens = self.auth_service.login(data)
        except InvalidCredentials:
            return error_response(
                message="Invalid email or password",
                status_code=401,
            )

        return success_response(
            data=tokens,
            message="Login successful",
        )

    def refresh(self, refresh_token: str) -> JSONResponse:
        try:
            tokens = self.auth_service.refresh(refresh_token)
        except InvalidRefreshToken:
            return error_response(
                message="Invalid or expired refresh token",
                status_code=401,
            )

        return success_response(
            data=tokens,
            message="Tokens refreshed successfully",
        )

    def logout(self, refresh_token: str) -> JSONResponse:
        self.auth_service.logout(refresh_token)

        return success_response(
            data=None,
            message="Logged out successfully",
        )