from flask import Blueprint, jsonify, request
from controllers.resume_controller import get_resume, upload_resume
from middleware.auth_middleware import student_required

resume_bp = Blueprint("resume", __name__)


@resume_bp.post("/resume")
@student_required
def upload(student):
    file = request.files.get("resume")
    payload, message, status = upload_resume(student, file)
    if not payload:
        return jsonify({"error": message}), status
    return jsonify({"message": message, "resume": payload}), status


@resume_bp.get("/resume")
@student_required
def latest(student):
    resume = get_resume(student)
    return jsonify(resume or {})
