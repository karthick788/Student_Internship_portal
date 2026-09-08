from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from functools import wraps
from models.student_model import get_student_by_user_id


def current_user_id():
    identity = get_jwt_identity()
    return int(identity)


def student_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = current_user_id()
        student = get_student_by_user_id(user_id)
        if not student:
            return jsonify({"error": "Student profile not found"}), 404
        return fn(student, *args, **kwargs)

    return wrapper
