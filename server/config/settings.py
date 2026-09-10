import os
from dotenv import load_dotenv

load_dotenv()


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

    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads/resumes")
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", str(5 * 1024 * 1024)))

    INTERNSHIP_API_URL = os.getenv("INTERNSHIP_API_URL", "").strip()
    INTERNSHIP_API_KEY = os.getenv("INTERNSHIP_API_KEY", "").strip()

    WHATSAPP_API_TOKEN = os.getenv("WHATSAPP_API_TOKEN", "").strip()
    WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "").strip()

    CLIENT_ORIGIN = os.getenv("CLIENT_ORIGIN", "http://localhost:5173")


if Config.FLASK_ENV == "production":
    if Config.JWT_SECRET_KEY in ("dev-jwt-secret", "change_this_jwt_secret", ""):
        raise RuntimeError("JWT_SECRET_KEY must be set to a strong value in production")
    if Config.SECRET_KEY in ("dev-secret", "change_this_secret_key", ""):
        raise RuntimeError("SECRET_KEY must be set to a strong value in production")
