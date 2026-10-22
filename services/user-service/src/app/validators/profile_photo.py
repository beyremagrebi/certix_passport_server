from werkzeug.datastructures import FileStorage


def validate_profile_photo(file: FileStorage | None) -> FileStorage:
    if file is None or not file.filename:
        raise ValueError("A profile photo is required.")

    return file
