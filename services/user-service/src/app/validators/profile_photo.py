
from werkzeug.datastructures import FileStorage
from PIL import Image, UnidentifiedImageError


class ProfilePhotoError(ValueError):
    pass


class ProfilePhotoValidator:
    @staticmethod
    def validate(
        file: FileStorage,
        *,
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
            raise ProfilePhotoError(
                "Profile photo exceeds the maximum file size."
            )

        try:
            with Image.open(file.stream) as image:
                image_format = (image.format or "").upper()
                width, height = image.size
                image.verify()
        except (
            UnidentifiedImageError,
            Image.DecompressionBombError,
            OSError,
            ValueError,
        ):
            raise ProfilePhotoError(
                "Profile photo content is not a valid image."
            ) from None
        finally:
            file.stream.seek(0)

        if image_format not in allowed_formats:
            raise ProfilePhotoError(
                "Profile photo format is not supported."
            )

        if width > max_width or height > max_height:
            raise ProfilePhotoError(
                "Profile photo dimensions exceed the configured limit."
            )

        return image_format
