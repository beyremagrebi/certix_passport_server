from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from PIL import Image, UnidentifiedImageError
from werkzeug.datastructures import FileStorage

from app.extensions import db
from app.repositories.user_repository import UserRepository


class ProfilePhotoError(ValueError):
    pass


class ProfilePhotoService:
    _extensions = {
        "JPEG": ".jpg",
        "PNG": ".png",
        "WEBP": ".webp",
    }

    @staticmethod
    def store(
        file: FileStorage,
        *,
        storage_dir: Path,
        allowed_formats: frozenset[str],
        max_bytes: int,
        max_width: int,
        max_height: int,
    ) -> str:
        if not file or not file.filename:
            raise ProfilePhotoError("A profile photo is required.")

        file.stream.seek(0, 2)
        file_size = file.stream.tell()
        file.stream.seek(0)
        if file_size > max_bytes:
            raise ProfilePhotoError("Profile photo exceeds the maximum file size.")

        try:
            with Image.open(file.stream) as image:
                image.verify()
                image_format = (image.format or "").upper()
                width, height = image.size
        except (UnidentifiedImageError, Image.DecompressionBombError, OSError):
            raise ProfilePhotoError("Profile photo content is not a valid image.") from None
        finally:
            file.stream.seek(0)

        if image_format not in allowed_formats or image_format not in ProfilePhotoService._extensions:
            raise ProfilePhotoError("Profile photo format is not supported.")
        if width > max_width or height > max_height:
            raise ProfilePhotoError("Profile photo dimensions exceed the configured limit.")

        asset_id = uuid4().hex
        asset_ref = f"profile-photo/{asset_id}"
        destination = storage_dir / f"{asset_id}{ProfilePhotoService._extensions[image_format]}"
        storage_dir.mkdir(parents=True, exist_ok=True)
        try:
            file.save(destination)
        except OSError:
            raise ProfilePhotoError("Profile photo could not be stored.") from None

        return asset_ref

    @staticmethod
    def upload(
        user_id: int,
        file: FileStorage,
        *,
        storage_dir: Path,
        allowed_formats: frozenset[str],
        max_bytes: int,
        max_width: int,
        max_height: int,
    ) -> str:
        user = UserRepository.get_by_id(user_id)
        if user is None:
            raise ProfilePhotoError("User not found.")

        asset_ref = ProfilePhotoService.store(
            file,
            storage_dir=storage_dir,
            allowed_formats=allowed_formats,
            max_bytes=max_bytes,
            max_width=max_width,
            max_height=max_height,
        )
        try:
            UserRepository.update_profile_photo(user, asset_ref)
        except Exception:
            db.session.rollback()
            raise

        return asset_ref
