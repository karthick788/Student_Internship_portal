from flask import Blueprint, jsonify, request
from middleware.auth_middleware import admin_required
from models.application_model import ALLOWED_STATUSES, list_all_applications, update_application_status
from models.db import fetch_all
from models.student_model import get_student_by_id
from services.email_service import send_status_email
from utils.logger import get_logger

admin_bp = Blueprint("admin", __name__)
logger = get_logger("admin")


@admin_bp.get("")
@admin_bp.get("/applications")
@admin_required
def list_applications(_user):
    try:
        apps = list_all_applications()
        return jsonify(apps)
    except Exception:
        logger.exception("Failed to list applications")
        return jsonify({"error": "Could not load applications"}), 500


@admin_bp.patch("/<int:app_id>/status")
@admin_bp.patch("/applications/<int:app_id>/status")
@admin_required
def patch_status(_user, app_id):
    data = request.get_json(silent=True) or {}
    status = (data.get("status") or "").strip()
    if status not in ALLOWED_STATUSES:
        return jsonify({"error": "Invalid status", "allowed": sorted(ALLOWED_STATUSES)}), 400
    try:
        result = update_application_status(app_id, status)
        if result is None:
            return jsonify({"error": "Application not found"}), 404
        try:
            student = get_student_by_id(result["student_id"])
            send_status_email(student, result.get("application_code"), status)
        except Exception:
            logger.exception("Status updated but email failed for application %s", app_id)
        return jsonify({"message": "Status updated", "application": result})
    except Exception:
        logger.exception("Failed to update application %s status", app_id)
        return jsonify({"error": "Could not update status"}), 500


@admin_bp.get("/students")
@admin_required
def list_students(_user):
    try:
        students = fetch_all(
            """
            SELECT s.id, s.full_name, s.college, u.email, s.created_at,
                   COUNT(a.id) AS application_count
            FROM students s
            JOIN users u ON u.id = s.user_id
            LEFT JOIN applications a ON a.student_id = s.id
            GROUP BY s.id
            ORDER BY s.created_at DESC
            """
        )
        return jsonify(students)
    except Exception:
        logger.exception("Failed to list students")
        return jsonify({"error": "Could not load students"}), 500
