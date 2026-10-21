
def validate_user_id(user_id):
    try:
        validated_id = int(user_id)
    except (TypeError, ValueError):
        raise ValueError("Invalid user ID.")

    if validated_id <= 0:
        raise ValueError("Invalid user ID.")

    return validated_id
