import bcrypt
from flask_jwt_extended import create_access_token
from models.student_model import create_student, get_student_by_user_id
from models.user_model import create_user, get_user_by_email, get_user_by_id
from utils.validators import is_valid_email, require_fields


def register_student(data):
    missing = require_fields(data, ["full_name", "email", "password"])
    if missing:
        return None, f"Missing fields: {', '.join(missing)}", 400
    email = data["email"].strip().lower()
    if not is_valid_email(email):
        return None, "Invalid email address", 400
    if len(data["password"]) < 6:
        return None, "Password must be at least 6 characters", 400
    if get_user_by_email(email):
        return None, "An account with this email already exists", 409

    password_hash = bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    user_id = create_user(email, password_hash)
    create_student(
        user_id,
        data["full_name"].strip(),
        data.get("phone"),
        data.get("college"),
    )
    token = create_access_token(identity=str(user_id))
    student = get_student_by_user_id(user_id)
    return {"token": token, "student": student}, "Registered successfully", 201


def login_student(data):
    missing = require_fields(data, ["email", "password"])
    if missing:
        return None, f"Missing fields: {', '.join(missing)}", 400
    user = get_user_by_email(data["email"].strip().lower())
    if not user:
        return None, "Invalid email or password", 401
    stored = user["password_hash"].encode("utf-8")
    if not bcrypt.checkpw(data["password"].encode("utf-8"), stored):
        return None, "Invalid email or password", 401
    token = create_access_token(identity=str(user["id"]))
    student = get_student_by_user_id(user["id"])
    return {"token": token, "student": student}, "Login successful", 200


def me(user_id):
    user = get_user_by_id(user_id)
    student = get_student_by_user_id(user_id)
    return {"user": user, "student": student}
