
from werkzeug.datastructures import FileStorage

from app.config import Config
from app.extensions import db
from app.repositories.user_repository import UserRepository
from app.storage.profile_photo import ProfilePhotoStorage
from app.validators.profile_photo import (
    ProfilePhotoError,
    ProfilePhotoValidator,
)


class ProfilePhotoService:

    @staticmethod
    def upload(user_id: int, file: FileStorage) -> str:
        user = UserRepository.get_by_id(user_id)

        if user is None:
            raise ProfilePhotoError("User not found.")

        image_format = ProfilePhotoValidator.validate(
            file,
            allowed_formats=Config.PROFILE_PHOTO_ALLOWED_FORMATS,
            max_bytes=Config.PROFILE_PHOTO_MAX_BYTES,
            max_width=Config.PROFILE_PHOTO_MAX_WIDTH,
            max_height=Config.PROFILE_PHOTO_MAX_HEIGHT,
        )

        asset_ref = ProfilePhotoStorage.store(
            file,
            storage_dir=Config.PROFILE_PHOTO_STORAGE_DIR,
            image_format=image_format,
        )

        try:
            UserRepository.update_profile_photo(user, asset_ref)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

        return asset_ref
