from models.internship_model import get_internship, list_internships
from models.saved_model import is_saved
from services.internship_api_service import sync_internships


def search_internships(filters, page=1, per_page=20):
    return list_internships(filters, page, per_page)


def internship_details(internship_id, student_id=None):
    item = get_internship(internship_id)
    if not item:
        return None
    if student_id:
        item["is_saved"] = is_saved(student_id, internship_id)
    return item


def run_sync():
    return sync_internships()
