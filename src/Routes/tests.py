from flask import Blueprint, jsonify

test_bp = Blueprint("test", __name__)


@test_bp.route("/test", methods=["GET"])
def test():
    """Test endpoint to verify API is working"""
    return jsonify({"status": "success", "message": "API is working correctly"}), 200


@test_bp.route("/ping", methods=["GET"])
def ping():
    """Health check endpoint"""
    return jsonify({"status": "success", "message": "pong"}), 200
