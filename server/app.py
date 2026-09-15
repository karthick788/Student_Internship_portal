import os
from datetime import timedelta
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config.settings import Config
from utils.logger import get_logger
from utils.rate_limit import limiter


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = Config.SECRET_KEY
    app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=Config.JWT_ACCESS_TOKEN_EXPIRES_HOURS)
    app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token"
    app.config["JWT_ACCESS_COOKIE_PATH"] = "/"
    app.config["JWT_COOKIE_SAMESITE"] = "Lax"
    app.config["JWT_COOKIE_SECURE"] = Config.JWT_COOKIE_SECURE
    app.config["MAX_CONTENT_LENGTH"] = Config.MAX_CONTENT_LENGTH

    upload_dir = os.path.join(os.path.dirname(__file__), Config.UPLOAD_FOLDER)
    os.makedirs(upload_dir, exist_ok=True)
    app.config["UPLOAD_FOLDER"] = upload_dir

    CORS(
        app,
        resources={r"/api/*": {"origins": Config.CLIENT_ORIGINS}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        expose_headers=["Content-Type"],
    )
    JWTManager(app)
    limiter.init_app(app)

    from models.user_model import ensure_user_auth_columns
    try:
        ensure_user_auth_columns()
    except Exception:
        get_logger("app").exception("Could not ensure user auth columns")

    @app.errorhandler(400)
    def bad_request(_error):
        return jsonify({"error": "Bad request", "status": 400}), 400

    @app.errorhandler(401)
    def unauthorised(_error):
        return jsonify({"error": "Unauthorised", "status": 401}), 401

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"error": "Not found", "status": 404}), 404

    @app.errorhandler(500)
    def internal_server_error(_error):
        get_logger("app").exception("Unhandled error")
        return jsonify({"error": "Internal server error", "status": 500}), 500

    from routes.auth_routes import auth_bp
    from routes.student_routes import student_bp
    from routes.internship_routes import internship_bp
    from routes.application_routes import application_bp
    from routes.saved_routes import saved_bp
    from routes.notification_routes import notification_bp
    from routes.resume_routes import resume_bp
    from routes.linkedin_routes import linkedin_bp
    from routes.admin_routes import admin_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(student_bp, url_prefix="/api/student")
    app.register_blueprint(internship_bp, url_prefix="/api/internships")
    app.register_blueprint(application_bp, url_prefix="/api/applications")
    app.register_blueprint(saved_bp, url_prefix="/api/saved-internships")
    app.register_blueprint(notification_bp, url_prefix="/api/notifications")
    app.register_blueprint(resume_bp, url_prefix="/api/student")
    app.register_blueprint(linkedin_bp, url_prefix="/api/linkedin-internships")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    @app.get("/api/health")
    def health():
        return {"ok": True, "service": "student-internship-api", "env": Config.FLASK_ENV}

    return app


if __name__ == "__main__":
    application = create_app()
    debug = Config.FLASK_ENV == "development"
    application.run(host="0.0.0.0", port=5000, debug=debug)
