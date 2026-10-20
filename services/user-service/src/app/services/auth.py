from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    decode_token,
)

from app.extensions import db
from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.repositories.user_repository import UserRepository


class AuthError(Exception):
    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self.status_code = status_code


class AuthService:
    @staticmethod
    def _store_refresh_token(token: str, user_id: int) -> None:
        claims = decode_token(token)

        refresh_token = RefreshToken(
            jti=claims["jti"],
            user_id=user_id,
            revoked=False,
        )

        db.session.add(refresh_token)

    @staticmethod
    def register(data: dict) -> dict:
        if UserRepository.get_by_email(data["email"]):
            raise AuthError("Email already registered.", 409)

        user = User(
            email=data["email"],
            first_name=data["first_name"],
            last_name=data["last_name"],
        )
        user.set_password(data["password"])

        try:
            # Save user first so user.id is available.
            UserRepository.create(user)

            # Generate tokens after successful registration.
            access_token = create_access_token(identity=str(user.id))
            refresh_token = create_refresh_token(identity=str(user.id))

            # Store the refresh token for revocation and rotation.
            AuthService._store_refresh_token(refresh_token, user.id)
            db.session.commit()

        except IntegrityError as exc:
            db.session.rollback()
            raise AuthError("Email already registered.", 409) from exc
        except Exception:
            db.session.rollback()
            raise

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
            "expires_in": 900,
            "user": {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
        }

    @staticmethod
    def login(data: dict) -> dict:
        user = UserRepository.get_by_email(data["email"])

        if user is None or not user.check_password(data["password"]):
            raise AuthError("Invalid email or password.", 401)

        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        try:
            AuthService._store_refresh_token(refresh_token, user.id)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
            "expires_in": 900,
            "user": {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
        }

    @staticmethod
    def refresh(user_id: str, old_jti: str) -> dict:
        try:
            old_token = db.session.execute(
                db.select(RefreshToken).where(
                    RefreshToken.jti == old_jti,
                    RefreshToken.user_id == int(user_id),
                )
            ).scalar_one_or_none()

            if old_token is None or old_token.revoked:
                raise AuthError("Invalid or revoked refresh token.", 401)

            old_token.revoked = True

            access_token = create_access_token(identity=str(user_id))
            refresh_token = create_refresh_token(identity=str(user_id))

            AuthService._store_refresh_token(refresh_token, int(user_id))
            db.session.commit()

            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "Bearer",
                "expires_in": 900,
            }

        except Exception:
            db.session.rollback()
            raise

    @staticmethod
    def logout(jti: str, user_id: str) -> None:
        refresh_token = db.session.execute(
            db.select(RefreshToken).where(
                RefreshToken.jti == jti,
                RefreshToken.user_id == int(user_id),
            )
        ).scalar_one_or_none()

        if refresh_token is None or refresh_token.revoked:
            raise AuthError("Invalid or already revoked refresh token.", 401)

        refresh_token.revoked = True
        db.session.commit()
