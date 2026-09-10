import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app
from models.resume_model import latest_resume, save_resume
from utils.validators import clean_str

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
    folder = current_app.config["UPLOAD_FOLDER"]
    path = os.path.join(folder, stored)
    file.save(path)

    resume_id = save_resume(
        student["id"],
        stored,
        clean_str(original, 255),
        stored,
        file.mimetype or "application/octet-stream",
        os.path.getsize(path),
    )
    return {"id": resume_id, **latest_resume(student["id"])}, "Resume uploaded", 201


def get_resume(student):
    return latest_resume(student["id"])
