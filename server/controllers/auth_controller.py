import bcrypt
from mysql.connector.errors import IntegrityError
from flask_jwt_extended import create_access_token
from config.settings import Config
from models.student_model import create_student, ensure_student_for_user, get_student_by_user_id
from models.user_model import (
    create_user,
    get_user_by_email,
    get_user_by_google_id,
    get_user_by_id,
    link_google_id,
    touch_last_login,
)
from utils.validators import (
    clean_str,
    is_strong_password,
    is_valid_email,
    is_valid_full_name,
    is_valid_phone,
    require_fields,
)


def _profile_incomplete(student):
    if not student:
        return True
    return not all(str(student.get(field) or "").strip() for field in ("full_name", "phone", "college"))


def _issue_session(user_id, full_name="Student"):
    touch_last_login(user_id)
    user = get_user_by_id(user_id)
    if user and user.get("role") == "admin":
        token = create_access_token(identity=str(user_id))
        return {
            "student": {
                "email": user.get("email"),
                "role": "admin",
                "full_name": "Administrator",
            },
            "needs_profile": False,
        }, token
    student = ensure_student_for_user(user_id, full_name)
    token = create_access_token(identity=str(user_id))
    return {"student": student, "needs_profile": _profile_incomplete(student)}, token


def register_student(data):
    missing = require_fields(data, ["full_name", "email", "password"])
    if missing:
        return None, f"Missing fields: {', '.join(missing)}", 400, None

    full_name = clean_str(data.get("full_name"), 150)
    email = (data.get("email") or "").strip().lower()
    phone = clean_str(data.get("phone"), 20)
    college = clean_str(data.get("college"), 200)
    password = data.get("password") or ""

    if not is_valid_full_name(full_name):
        return None, "Enter a valid full name (letters only, at least 2 characters)", 400, None
    if not is_valid_email(email):
        return None, "Enter a valid email address", 400, None
    if not is_valid_phone(phone):
        return None, "Enter a valid phone number (10–15 digits)", 400, None
    if not is_strong_password(password):
        return None, "Password must be at least 8 characters and include a letter and a number", 400, None
    if get_user_by_email(email):
        return None, "An account with this email already exists", 409, None

    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode("utf-8")

    try:
        user_id = create_user(email, password_hash, auth_provider="password")
    except IntegrityError:
        return None, "An account with this email already exists", 409, None
    except Exception:
        return None, "Registration failed. Please try again.", 500, None

    try:
        create_student(user_id, full_name, phone, college)
    except Exception:
        ensure_student_for_user(user_id, full_name)

    payload, token = _issue_session(user_id, full_name)
    return payload, "Registered successfully", 201, token


def login_student(data):
    missing = require_fields(data, ["email", "password"])
    if missing:
        return None, f"Missing fields: {', '.join(missing)}", 400, None
    email = (data.get("email") or "").strip().lower()
    if not is_valid_email(email):
        return None, "Enter a valid email address", 400, None

    user = get_user_by_email(email)
    if not user:
        return None, "Invalid email or password", 401, None
    if not user.get("password_hash"):
        return None, "This account uses Google. Click Continue with Google.", 401, None
    stored = user["password_hash"].encode("utf-8")
    if not bcrypt.checkpw((data.get("password") or "").encode("utf-8"), stored):
        return None, "Invalid email or password", 401, None

    payload, token = _issue_session(user["id"])
    return payload, "Login successful", 200, token


def login_with_google(id_token_str):
    if not Config.GOOGLE_CLIENT_ID:
        return None, "Google sign-in is not configured on the server", 503, None
    if not id_token_str:
        return None, "Missing Google credential", 400, None

    try:
        from google.oauth2 import id_token as google_id_token
        from google.auth.transport import requests as google_requests

        info = google_id_token.verify_oauth2_token(
            id_token_str,
            google_requests.Request(),
            Config.GOOGLE_CLIENT_ID,
        )
    except Exception:
        return None, "Google sign-in failed. Try again.", 401, None

    google_sub = info.get("sub")
    email = (info.get("email") or "").strip().lower()
    name = clean_str(info.get("name") or email.split("@")[0], 150)
    if not google_sub or not email or not info.get("email_verified"):
        return None, "Google account email is not verified", 401, None

    user = get_user_by_google_id(google_sub) or get_user_by_email(email)
    display_name = name or (email.split("@")[0] if email else "Student")
    if user:
        if not user.get("google_id"):
            link_google_id(user["id"], google_sub)
        payload, token = _issue_session(user["id"], display_name)
        status = 200
        message = "Complete your profile" if payload.get("needs_profile") else "Login successful"
        return payload, message, status, token

    try:
        user_id = create_user(email, None, google_id=google_sub, auth_provider="google")
        ensure_student_for_user(user_id, display_name)
    except IntegrityError:
        user = get_user_by_email(email)
        if not user:
            return None, "Could not create Google account", 500, None
        link_google_id(user["id"], google_sub)
        payload, token = _issue_session(user["id"], display_name)
        return payload, "Login successful", 200, token

    payload, token = _issue_session(user_id, display_name)
    return payload, "Signed in with Google", 200, token


def me(user_id):
    user = get_user_by_id(user_id)
    student = get_student_by_user_id(user_id)
    return {"user": user, "student": student}
