"""Standard JSON response helpers for the Flask API."""

from typing import Any

from flask import jsonify


def success_response(
    message: str,
    data: Any = None,
    status_code: int = 200,
):
    """Return a consistent successful API response."""
    response = {
        "success": True,
        "message": message,
        "data": data,
        "error": None,
    }
    return jsonify(response), status_code


def error_response(
    message: str,
    code: str,
    status_code: int,
    *,
    details: Any = None,
):
    """Return a consistent error API response."""
    response = {
        "success": False,
        "message": message,
        "data": None,
        "error": {
            "code": code,
            "message": message,
        },
    }

    if details is not None:
        response["error"]["details"] = details

    return jsonify(response), status_code
