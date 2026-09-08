from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from controllers.auth_controller import login_student, me, register_student
from middleware.auth_middleware import current_user_id

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register():
    payload, message, status = register_student(request.get_json(silent=True) or {})
    if not payload:
        return jsonify({"error": message}), status
    return jsonify({"message": message, **payload}), status


@auth_bp.post("/login")
def login():
    payload, message, status = login_student(request.get_json(silent=True) or {})
    if not payload:
        return jsonify({"error": message}), status
    return jsonify({"message": message, **payload}), status


@auth_bp.get("/me")
@jwt_required()
def current_user():
    data = me(current_user_id())
    return jsonify(data)
