from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import jwt_required
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config.settings import Config
from controllers.auth_controller import login_student, me, register_student
from middleware.auth_middleware import current_user_id

auth_bp = Blueprint("auth", __name__)
limiter = Limiter(key_func=get_remote_address)


def _set_access_cookie(resp, token, max_age):
    resp.set_cookie(
        "access_token",
        token,
        httponly=True,
        samesite="Strict",
        secure=Config.JWT_COOKIE_SECURE,
        max_age=max_age,
    )
    return resp


@auth_bp.post("/register")
@limiter.limit("10 per hour")
def register():
    payload, message, status, token = register_student(request.get_json(silent=True) or {})
    if not payload:
        return jsonify({"error": message}), status
    resp = make_response(jsonify({"message": message, **payload}), status)
    return _set_access_cookie(resp, token, Config.JWT_ACCESS_TOKEN_EXPIRES_HOURS * 3600)


@auth_bp.post("/login")
@limiter.limit("5 per minute")
def login():
    payload, message, status, token = login_student(request.get_json(silent=True) or {})
    if not payload:
        return jsonify({"error": message}), status
    resp = make_response(jsonify({"message": message, **payload}), status)
    return _set_access_cookie(resp, token, Config.JWT_ACCESS_TOKEN_EXPIRES_HOURS * 3600)


@auth_bp.get("/me")
@jwt_required()
def current_user():
    data = me(current_user_id())
    return jsonify(data)


@auth_bp.post("/logout")
def logout():
    resp = make_response(jsonify({"message": "Logged out"}))
    return _set_access_cookie(resp, "", 0)
