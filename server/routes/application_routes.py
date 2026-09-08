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
