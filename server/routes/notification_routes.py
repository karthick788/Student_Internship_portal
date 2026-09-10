from flask import Blueprint, jsonify
from services.notification_service import get_student_notifications, read_all_notifications, read_notification
from middleware.auth_middleware import student_required

notification_bp = Blueprint("notifications", __name__)


@notification_bp.get("")
@student_required
def list_all(student):
    return jsonify(get_student_notifications(student["id"]))


@notification_bp.put("/<int:notification_id>/read")
@student_required
def mark(student, notification_id):
    if not read_notification(notification_id, student["id"]):
        return jsonify({"error": "Notification not found"}), 404
    return jsonify({"message": "Marked as read"})


@notification_bp.put("/read-all")
@student_required
def mark_all(student):
    count = read_all_notifications(student["id"])
    return jsonify({"message": f"Marked {count} notifications as read"})
