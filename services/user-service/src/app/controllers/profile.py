from flask import request
from flask_jwt_extended import get_jwt_identity

from app.services.user import UserService
from app.services.profile_photo import (
    ProfilePhotoError,
    ProfilePhotoService,
)
from app.utils.api_response import error_response, success_response
from app.validators.profile import validate_profile_update


def upload_profile_photo():
    try:
        user_id = int(get_jwt_identity())
        file = request.files.get("photo")

        asset_ref = ProfilePhotoService.upload(
            user_id=user_id,
            file=file,
        )

    except ProfilePhotoError as exc:
        status_code = 404 if str(exc) == "User not found." else 400

        return error_response(
            message=str(exc),
            code="PROFILE_PHOTO_ERROR",
            status_code=status_code,
        )

    except (ValueError, TypeError):
        return error_response(
            message="Invalid user identity.",
            code="VALIDATION_ERROR",
            status_code=400,
        )

    return success_response(
        message="Profile photo uploaded successfully.",
        data={"asset_ref": asset_ref},
        status_code=200,
    )