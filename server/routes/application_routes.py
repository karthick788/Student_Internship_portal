from flask import Blueprint, jsonify, request
from controllers.application_controller import get_application_by_id, get_applications, submit_application
from middleware.auth_middleware import student_required

application_bp = Blueprint("applications", __name__)


@application_bp.post("")
@student_required
def create(student):
    payload, message, status = submit_application(student, request.get_json(silent=True) or {})
    if not payload:
        return jsonify({"error": message}), status
    return jsonify({"message": message, "application": payload}), status


@application_bp.get("")
@student_required
def list_all(student):
    return jsonify(get_applications(student))


@application_bp.get("/<int:app_id>")
@student_required
def detail(student, app_id):
    item = get_application_by_id(student, app_id)
    if not item:
        return jsonify({"error": "Application not found"}), 404
    return jsonify(item)

@application_bp.patch("/<int:app_id>/status")
@student_required
def update_status(student, app_id):
    data = request.get_json(silent=True) or {}
    status = data.get("status")
    
    if status not in ["student_selected_next_round", "student_rejected", "student_applied"]:
        return jsonify({"error": "Invalid status update"}), 400
        
    item = get_application_by_id(student, app_id)
    if not item:
        return jsonify({"error": "Application not found"}), 404
        
    from models.application_model import update_application_status
    updated = update_application_status(app_id, status)
    return jsonify({"message": "Status updated", "application": updated})
