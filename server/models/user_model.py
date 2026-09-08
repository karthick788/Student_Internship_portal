from models.db import execute, fetch_one


def create_user(email, password_hash):
    user_id, _ = execute(
        "INSERT INTO users (email, password_hash, role) VALUES (%s, %s, 'student')",
        (email, password_hash),
    )
    return user_id


def get_user_by_email(email):
    return fetch_one("SELECT * FROM users WHERE email = %s", (email,))


def get_user_by_id(user_id):
    return fetch_one("SELECT id, email, role, created_at FROM users WHERE id = %s", (user_id,))
