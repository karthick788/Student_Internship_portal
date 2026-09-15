from models.application_model import create_application, get_existing_application
from models.internship_model import get_internship
from models.student_model import get_student_by_id
from services.email_service import send_application_email


def apply_to_internship(student, internship_id, cover_note=None):
    internship = get_internship(internship_id)
    if not internship:
        return None, "Internship not found", 404

    existing = get_existing_application(student["id"], internship_id)
    if existing:
        return existing, "You have already applied for this internship", 409


    application = create_application(student["id"], internship_id, cover_note)
    fresh = get_student_by_id(student["id"]) or student
    email = send_application_email(fresh, internship, application["application_code"])
    return {**application, "email": email}, "Application submitted", 201
