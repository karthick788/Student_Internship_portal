from models.application_model import create_application, get_existing_application
from models.internship_model import get_internship
from models.notification_model import create_notification
from services.whatsapp_service import build_whatsapp_payload


def apply_to_internship(student, internship_id, cover_note=None):
    internship = get_internship(internship_id)
    if not internship:
        return None, "Internship not found", 404

    if internship.get("application_method") != "internal":
        return None, "This internship uses an external application page", 400

    existing = get_existing_application(student["id"], internship_id)
    if existing:
        return existing, "You have already applied for this internship", 409

    application = create_application(student["id"], internship_id, cover_note)
    create_notification(
        student["id"],
        "Application submitted",
        f"Your application {application['application_code']} for {internship['title']} was submitted.",
    )
    whatsapp = build_whatsapp_payload(student, internship, application["application_code"])
    return {**application, "whatsapp": whatsapp}, "Application submitted", 201
