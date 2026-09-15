import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app
from models.resume_model import latest_resume, save_resume
from utils.validators import clean_str
from config.mongodb import get_gridfs

ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}
ALLOWED_MIMES = {
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


def allowed_file(filename, mimetype):
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return ext in ALLOWED_EXTENSIONS and (not mimetype or mimetype in ALLOWED_MIMES)


def upload_resume(student, file):
    if not file or not file.filename:
        return None, "No file provided", 400
    if not allowed_file(file.filename, file.mimetype):
        return None, "Only PDF, DOC, and DOCX files are allowed", 400

    original = secure_filename(file.filename)
    ext = original.rsplit(".", 1)[-1].lower()
    stored = f"{student['id']}_{uuid.uuid4().hex}.{ext}"

    # Read the file data
    file_bytes = file.read()
    file_size = len(file_bytes)
    file_mimetype = file.mimetype or "application/octet-stream"

    try:
        fs = get_gridfs()
        gridfs_id = fs.put(
            file_bytes,
            filename=original,
            content_type=file_mimetype,
            student_id=student["id"],
        )
    except Exception:
        return None, "Resume storage is unavailable. Check MongoDB (MONGO_URI).", 503

    resume_id = save_resume(
        student["id"],
        stored,
        clean_str(original, 255),
        "gridfs",  # Set file_path to 'gridfs' as a placeholder
        file_mimetype,
        file_size,
        str(gridfs_id)
    )
    return {"id": resume_id, **latest_resume(student["id"])}, "Resume uploaded", 201


def get_resume(student):
    return latest_resume(student["id"])

