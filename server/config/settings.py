import os
from dotenv import load_dotenv

_SERVER_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(_SERVER_DIR, ".env"), override=True)


class Config:
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret")
    JWT_ACCESS_TOKEN_EXPIRES_HOURS = int(os.getenv("JWT_EXPIRES_HOURS", "24"))
    JWT_COOKIE_SECURE = os.getenv("JWT_COOKIE_SECURE", "false").lower() == "true"

    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "internship_management")
    # Optional SSL CA cert path (required for Aiven; PlanetScale handles SSL automatically)
    DB_SSL_CA = os.getenv("DB_SSL_CA", "").strip()
    # Connection pool size — increase for cloud DBs with higher latency
    DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "10"))

    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads/resumes")
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", str(5 * 1024 * 1024)))

    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "").strip()
    MONGO_URI = os.getenv("MONGO_URI", "")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "internhub")

    INTERNSHIP_API_URL = os.getenv("INTERNSHIP_API_URL", "").strip()
    INTERNSHIP_API_KEY = os.getenv("INTERNSHIP_API_KEY", "").strip()
    ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID", "").strip()
    ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY", "").strip()

    EMAILJS_SERVICE_ID = os.getenv("EMAILJS_SERVICE_ID", "").strip()
    EMAILJS_TEMPLATE_ID = os.getenv("EMAILJS_TEMPLATE_ID", "").strip()
    EMAILJS_PUBLIC_KEY = os.getenv("EMAILJS_PUBLIC_KEY", "").strip()
    EMAILJS_PRIVATE_KEY = os.getenv("EMAILJS_PRIVATE_KEY", "").strip()  # EmailJS API private key

    CLIENT_ORIGIN = os.getenv("CLIENT_ORIGIN", "http://localhost:5173")
    CLIENT_ORIGINS = [
        origin.strip()
        for origin in os.getenv(
            "CLIENT_ORIGINS",
            ",".join(
                [
                    CLIENT_ORIGIN,
                    "http://127.0.0.1:5173",
                    "http://localhost:5500",
                    "http://127.0.0.1:5500",
                    "http://localhost:3000",
                    "http://127.0.0.1:3000",
                ]
            ),
        ).split(",")
        if origin.strip()
    ]


if Config.FLASK_ENV == "production":
    if Config.JWT_SECRET_KEY in ("dev-jwt-secret", "change_this_jwt_secret", ""):
        raise RuntimeError("JWT_SECRET_KEY must be set to a strong value in production")
    if Config.SECRET_KEY in ("dev-secret", "change_this_secret_key", ""):
        raise RuntimeError("SECRET_KEY must be set to a strong value in production")
