from flask import current_app, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.services.profile_photo import ProfilePhotoError, ProfilePhotoService
from app.utils.api_response import error_response, success_response
from app.validators.profile_photo import validate_profile_photo


@jwt_required()
def upload_profile_photo():
    try:
        file = validate_profile_photo(request.files.get("photo"))
        asset_ref = ProfilePhotoService.upload(
            user_id=int(get_jwt_identity()),
            file=file,
            storage_dir=current_app.config["PROFILE_PHOTO_STORAGE_DIR"],
            allowed_formats=current_app.config["PROFILE_PHOTO_ALLOWED_FORMATS"],
            max_bytes=current_app.config["PROFILE_PHOTO_MAX_BYTES"],
            max_width=current_app.config["PROFILE_PHOTO_MAX_WIDTH"],
            max_height=current_app.config["PROFILE_PHOTO_MAX_HEIGHT"],
        )
    except ProfilePhotoError as exc:
        status_code = 404 if str(exc) == "User not found." else 400
        return error_response(
            message=str(exc),
            code="PROFILE_PHOTO_ERROR",
            status_code=status_code,
        )
    except ValueError as exc:
        return error_response(
            message=str(exc),
            code="VALIDATION_ERROR",
            status_code=400,
        )

    return success_response(
        message="Profile photo uploaded successfully.",
        data={"asset_ref": asset_ref},
    )
