
from pathlib import Path
from uuid import uuid4

from werkzeug.datastructures import FileStorage

from app.validators.profile_photo import ProfilePhotoError


class ProfilePhotoStorage:
    EXTENSIONS = {
        "JPEG": ".jpg",
        "PNG": ".png",
        "WEBP": ".webp",
    }

    @classmethod
    def store(
        cls,
        file: FileStorage,
        *,
        storage_dir: Path,
        image_format: str,
    ) -> str:
        extension = cls.EXTENSIONS.get(image_format)

        if extension is None:
            raise ProfilePhotoError(
                "Profile photo format is not supported."
            )

        asset_id = uuid4().hex
        destination = storage_dir / f"{asset_id}{extension}"
        asset_ref = f"profile-photo/{asset_id}"

        try:
            storage_dir.mkdir(parents=True, exist_ok=True)
            file.save(destination)
        except OSError:
            raise ProfilePhotoError(
                "Profile photo could not be stored."
            ) from None

        return asset_ref
