from flask import Blueprint, jsonify, make_response, request
import os
from flask_jwt_extended import jwt_required, set_access_cookies, unset_jwt_cookies
from config.settings import Config
from controllers.auth_controller import login_student, login_with_google, me, register_student
from middleware.auth_middleware import current_user_id

auth_bp = Blueprint("auth", __name__)


def _auth_response(payload, message, status, token):
    body = {"message": message, **payload}
    if token:
        body["token"] = token
    resp = make_response(jsonify(body), status)
    if token:
        set_access_cookies(resp, token, max_age=Config.JWT_ACCESS_TOKEN_EXPIRES_HOURS * 3600)
    return resp


@auth_bp.get("/config")
def auth_config():
    client_id = (os.getenv("GOOGLE_CLIENT_ID") or Config.GOOGLE_CLIENT_ID or "").strip()
    return jsonify(
        {
            "google_client_id": client_id or None,
            "emailjs": {
                "service_id": Config.EMAILJS_SERVICE_ID or None,
                "template_id": Config.EMAILJS_TEMPLATE_ID or None,
                "public_key": Config.EMAILJS_PUBLIC_KEY or None,
            },
        }
    )


@auth_bp.post("/register")
def register():
    payload, message, status, token = register_student(request.get_json(silent=True) or {})
    if not payload:
        return jsonify({"error": message}), status
    return _auth_response(payload, message, status, token)


@auth_bp.post("/login")
def login():
    payload, message, status, token = login_student(request.get_json(silent=True) or {})
    if not payload:
        return jsonify({"error": message}), status
    return _auth_response(payload, message, status, token)


@auth_bp.post("/google")
def google_login():
    data = request.get_json(silent=True) or {}
    payload, message, status, token = login_with_google(data.get("credential"))
    if not payload:
        return jsonify({"error": message}), status
    return _auth_response(payload, message, status, token)


@auth_bp.get("/me")
@jwt_required()
def current_user():
    data = me(current_user_id())
    return jsonify(data)


@auth_bp.post("/logout")
def logout():
    resp = make_response(jsonify({"message": "Logged out"}))
    unset_jwt_cookies(resp)
    return resp
