
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.schemas.user import UserLogin, UserRegister
from app.services.auth_service import (
    AuthService,
    EmailAlreadyRegistered,
    InvalidCredentials,
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

        return success_response(
            data=jsonable_encoder(user, include={
                "id", "first_name", "last_name", "email"
            }),
            message="User registered successfully",
            status_code=201,
        )

    def login(self, data: UserLogin) -> JSONResponse:
        try:
            token = self.auth_service.login(data)
        except InvalidCredentials:
            return error_response(
                message="Invalid email or password",
                status_code=401,
            )

        return success_response(
            data={
                "access_token": token,
                "token_type": "bearer",
            },
            message="Login successful",
            status_code=200,
        )
