from flask import Blueprint, jsonify
from models.linkedin_model import get_linkedin, list_linkedin

linkedin_bp = Blueprint("linkedin", __name__)


@linkedin_bp.get("")
def list_all():
    return jsonify(list_linkedin())


@linkedin_bp.get("/<int:item_id>")
def detail(item_id):
    item = get_linkedin(item_id)
    if not item:
        return jsonify({"error": "LinkedIn internship not found"}), 404
    return jsonify(item)
