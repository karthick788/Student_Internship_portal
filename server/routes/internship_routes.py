from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required, verify_jwt_in_request
from controllers.internship_controller import internship_details, run_sync, search_internships
from middleware.auth_middleware import current_user_id
from models.student_model import get_student_by_user_id

internship_bp = Blueprint("internships", __name__)


@internship_bp.get("")
def list_all():
    filters = {
        "search": request.args.get("search"),
        "location": request.args.get("location"),
        "skills": request.args.get("skills"),
        "work_mode": request.args.get("work_mode"),
        "duration": request.args.get("duration"),
        "stipend": request.args.get("stipend"),
    }
    page = max(1, int(request.args.get("page", 1)))
    per_page = min(max(1, int(request.args.get("per_page", 20))), 100)
    return jsonify(search_internships(filters, page, per_page))


@internship_bp.get("/<int:internship_id>")
def detail(internship_id):
    student_id = None
    verify_jwt_in_request(optional=True)
    identity = get_jwt_identity()
    if identity:
        student = get_student_by_user_id(int(identity))
        if student:
            student_id = student["id"]
    item = internship_details(internship_id, student_id)
    if not item:
        return jsonify({"error": "Internship not found"}), 404
    return jsonify(item)


@internship_bp.post("/sync")
@jwt_required()
def sync():
    student = get_student_by_user_id(current_user_id())
    if not student:
        return jsonify({"error": "Student profile not found"}), 404
    result = run_sync()
    return jsonify({"message": "Internship sync completed", **result})
