from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.get("/")
def home():
    return jsonify({"message": "Server is running"})


@health_bp.get("/health")
def health():
    return jsonify({"status": "ok"})