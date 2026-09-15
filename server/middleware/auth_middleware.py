from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from functools import wraps
from models.student_model import ensure_student_for_user, get_student_by_user_id
from models.user_model import get_user_by_id


def current_user_id():
    identity = get_jwt_identity()
    return int(identity)


def student_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = current_user_id()
        user = get_user_by_id(user_id)
        if user and user.get("role") == "admin":
            return jsonify({"error": "Student access required"}), 403
        student = get_student_by_user_id(user_id)
        if not student:
            student = ensure_student_for_user(user_id, "Student")
        if not student:
            return jsonify({"error": "Student profile not found"}), 404
        return fn(student, *args, **kwargs)

    return wrapper


def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user = get_user_by_id(current_user_id())
        if not user or user.get("role") != "admin":
            return jsonify({"error": "Admin access required"}), 403
        return fn(user, *args, **kwargs)

    return wrapper
