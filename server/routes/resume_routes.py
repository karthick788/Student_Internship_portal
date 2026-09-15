from flask import Blueprint, current_app, jsonify, request, send_from_directory
from controllers.resume_controller import get_resume, upload_resume
from middleware.auth_middleware import student_required
from bson import ObjectId
from flask import Response
from config.mongodb import get_gridfs

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
    if not resume or not resume.get("gridfs_file_id"):
        return jsonify({"error": "No resume uploaded"}), 404

    fs = get_gridfs()
    try:
        grid_out = fs.get(ObjectId(resume["gridfs_file_id"]))
        return Response(
            grid_out.read(),
            mimetype=grid_out.content_type,
            headers={"Content-Disposition": f'attachment; filename="{resume["original_name"]}"'}
        )
    except Exception as e:
        return jsonify({"error": "Failed to retrieve resume file"}), 500


@resume_bp.get("/resume")
@student_required
def latest(student):
    resume = get_resume(student)
    return jsonify(resume or {})
