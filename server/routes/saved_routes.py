from flask import Blueprint, jsonify
from models.internship_model import get_internship
from models.saved_model import list_saved, save_internship, unsave_internship
from middleware.auth_middleware import student_required

saved_bp = Blueprint("saved", __name__)


@saved_bp.get("")
@student_required
def list_all(student):
    return jsonify(list_saved(student["id"]))


@saved_bp.post("/<int:internship_id>")
@student_required
def save(student, internship_id):
    if not get_internship(internship_id):
        return jsonify({"error": "Internship not found"}), 404
    item = save_internship(student["id"], internship_id)
    return jsonify({"message": "Internship saved", "saved": item}), 201


@saved_bp.delete("/<int:internship_id>")
@student_required
def remove(student, internship_id):
    if not unsave_internship(student["id"], internship_id):
        return jsonify({"error": "Saved internship not found"}), 404
    return jsonify({"message": "Removed from saved internships"})
