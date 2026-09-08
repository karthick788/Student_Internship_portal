from services.application_service import apply_to_internship
from models.application_model import get_application, list_applications


def submit_application(student, data):
    internship_id = data.get("internship_id")
    if not internship_id:
        return None, "internship_id is required", 400
    return apply_to_internship(student, int(internship_id), data.get("cover_note"))


def get_applications(student):
    return list_applications(student["id"])


def get_application_by_id(student, app_id):
    return get_application(app_id, student["id"])
