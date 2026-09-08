from flask import Blueprint, jsonify, request
from controllers import student_controller as sc
from middleware.auth_middleware import student_required
from models.application_model import count_applications
from models.internship_model import count_internships
from models.saved_model import count_saved
from models.resume_model import latest_resume
from services.notification_service import get_student_notifications

student_bp = Blueprint("student", __name__)


@student_bp.get("/dashboard")
@student_required
def dashboard(student):
    notifs = get_student_notifications(student["id"])
    return jsonify(
        {
            "internships": count_internships(),
            "applications": count_applications(student["id"]),
            "saved": count_saved(student["id"]),
            "notifications_unread": notifs["unread"],
            "has_resume": bool(latest_resume(student["id"])),
        }
    )


@student_bp.get("/profile")
@student_required
def profile(student):
    return jsonify(sc.get_profile(student))


@student_bp.put("/profile")
@student_required
def update_profile(student):
    data = request.get_json(silent=True) or {}
    return jsonify(sc.save_profile(student, data))


@student_bp.get("/education")
@student_required
def education_list(student):
    return jsonify(sc.get_profile(student)["education"])


@student_bp.post("/education")
@student_required
def education_create(student):
    item, error = sc.create_education(student, request.get_json(silent=True) or {})
    if error:
        return jsonify({"error": error}), 400
    return jsonify(item), 201


@student_bp.put("/education/<int:edu_id>")
@student_required
def education_update(student, edu_id):
    item, error = sc.edit_education(student, edu_id, request.get_json(silent=True) or {})
    if error:
        return jsonify({"error": error}), 404 if "not found" in error.lower() else 400
    return jsonify(item)


@student_bp.delete("/education/<int:edu_id>")
@student_required
def education_delete(student, edu_id):
    if not sc.remove_education(student, edu_id):
        return jsonify({"error": "Education record not found"}), 404
    return jsonify({"message": "Deleted"})


@student_bp.get("/skills")
@student_required
def skills_list(student):
    return jsonify(sc.get_profile(student)["skills"])


@student_bp.post("/skills")
@student_required
def skills_create(student):
    items, error = sc.create_skill(student, request.get_json(silent=True) or {})
    if error:
        return jsonify({"error": error}), 400
    return jsonify(items), 201


@student_bp.delete("/skills/<int:skill_id>")
@student_required
def skills_delete(student, skill_id):
    if not sc.remove_skill(student, skill_id):
        return jsonify({"error": "Skill not found"}), 404
    return jsonify({"message": "Deleted"})
