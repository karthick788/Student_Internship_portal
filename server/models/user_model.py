from models.db import execute, fetch_all, fetch_one

_schema_ready = False


def ensure_user_auth_columns():
    """Add Google/auth columns on existing Aiven tables without wiping data."""
    global _schema_ready
    if _schema_ready:
        return
    rows = fetch_all("SHOW COLUMNS FROM users")
    names = {row["Field"] for row in rows}

    if "google_id" not in names:
        execute("ALTER TABLE users ADD COLUMN google_id VARCHAR(64) NULL UNIQUE")
    if "auth_provider" not in names:
        execute(
            "ALTER TABLE users ADD COLUMN auth_provider ENUM('password','google') NOT NULL DEFAULT 'password'"
        )
    if "last_login_at" not in names:
        execute("ALTER TABLE users ADD COLUMN last_login_at TIMESTAMP NULL")

    password_col = next((row for row in rows if row["Field"] == "password_hash"), None)
    if password_col and password_col.get("Null") == "NO":
        execute("ALTER TABLE users MODIFY password_hash VARCHAR(255) NULL")

    _schema_ready = True


def create_user(email, password_hash=None, google_id=None, auth_provider="password"):
    user_id, _ = execute(
        """
        INSERT INTO users (email, password_hash, google_id, auth_provider, role, last_login_at)
        VALUES (%s, %s, %s, %s, 'student', CURRENT_TIMESTAMP)
        """,
        (email, password_hash, google_id, auth_provider),
    )
    return user_id


def get_user_by_email(email):
    return fetch_one("SELECT * FROM users WHERE email = %s", (email,))


def get_user_by_google_id(google_id):
    return fetch_one("SELECT * FROM users WHERE google_id = %s", (google_id,))


def get_user_by_id(user_id):
    return fetch_one(
        "SELECT id, email, role, auth_provider, created_at, last_login_at FROM users WHERE id = %s",
        (user_id,),
    )


def link_google_id(user_id, google_id):
    execute("UPDATE users SET google_id = %s WHERE id = %s AND google_id IS NULL", (google_id, user_id))


def touch_last_login(user_id):
    execute("UPDATE users SET last_login_at = CURRENT_TIMESTAMP WHERE id = %s", (user_id,))
