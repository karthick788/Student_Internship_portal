from flask import Blueprint, current_app, jsonify, request, send_from_directory
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


@resume_bp.get("/resume/file")
@student_required
def download(student):
    resume = get_resume(student)
    if not resume:
        return jsonify({"error": "No resume uploaded"}), 404
    return send_from_directory(
        current_app.config["UPLOAD_FOLDER"],
        resume["stored_name"],
        as_attachment=True,
        download_name=resume["original_name"],
        mimetype=resume.get("mime_type", "application/octet-stream"),
    )


@resume_bp.get("/resume")
@student_required
def latest(student):
    resume = get_resume(student)
    return jsonify(resume or {})
