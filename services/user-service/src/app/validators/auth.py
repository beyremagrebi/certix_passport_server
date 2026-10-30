
from email_validator import EmailNotValidError, validate_email


def validate_registration(data: object) -> dict:
    if not isinstance(data, dict):
        raise ValueError("Request body must be a JSON object.")

    required = ("email", "first_name", "last_name", "password")

    for field in required:
        if not isinstance(data.get(field), str) or not data[field].strip():
            raise ValueError(f"{field} is required.")

    try:
        email = validate_email(
            data["email"].strip(),
            check_deliverability=False,
        ).normalized
    except EmailNotValidError as exc:
        raise ValueError("Invalid email address.") from exc

    first_name = data["first_name"].strip()
    last_name = data["last_name"].strip()
    password = data["password"]

    if len(first_name) > 100 or len(last_name) > 100:
        raise ValueError("Names must not exceed 100 characters.")

    if len(password) < 8:
        raise ValueError("Password must contain at least 8 characters.")

    if len(password) > 128:
        raise ValueError("Password must not exceed 128 characters.")

    return {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "password": password,
    }


def validate_login(data: object) -> dict:
    if not isinstance(data, dict):
        raise ValueError("Request body must be a JSON object.")

    email = data.get("email")
    password = data.get("password")

    if not isinstance(email, str) or not email.strip():
        raise ValueError("Email is required.")

    if not isinstance(password, str) or not password:
        raise ValueError("Password is required.")

    try:
        email = validate_email(
            email.strip(),
            check_deliverability=False,
        ).normalized
    except EmailNotValidError as exc:
        raise ValueError("Invalid email address.") from exc

    if len(password) > 128:
        raise ValueError("Invalid credentials.")

    return {"email": email, "password": password}


def validate_password_reset_request(data: object) -> dict[str, str]:
    if not isinstance(data, dict):
        raise ValueError("Request body must be a JSON object.")

    email = data.get("email")
    if not isinstance(email, str) or not email.strip():
        raise ValueError("Email is required.")

    try:
        normalized_email = validate_email(
            email.strip(),
            check_deliverability=False,
        ).normalized
    except EmailNotValidError as exc:
        raise ValueError("Invalid email address.") from exc

    return {"email": normalized_email}


def validate_password_reset(data: object) -> dict[str, str]:
    if not isinstance(data, dict):
        raise ValueError("Request body must be a JSON object.")

    token = data.get("token")
    new_password = data.get("new_password")
    if not isinstance(token, str) or not token.strip():
        raise ValueError("Reset token is required.")
    if not isinstance(new_password, str) or not new_password:
        raise ValueError("New password is required.")
    if len(new_password) < 8:
        raise ValueError("Password must contain at least 8 characters.")
    if len(new_password) > 128:
        raise ValueError("Password must not exceed 128 characters.")

    return {"token": token.strip(), "new_password": new_password}
