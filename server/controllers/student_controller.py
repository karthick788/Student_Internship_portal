from models.student_model import (
    add_education,
    add_student_skill,
    delete_education,
    delete_student_skill,
    get_education,
    get_student_by_user_id,
    list_education,
    list_student_skills,
    update_education,
    update_student,
)
from utils.validators import is_valid_full_name, is_valid_phone, require_fields


def get_profile(student):
    return {
        **student,
        "education": list_education(student["id"]),
        "skills": list_student_skills(student["id"]),
    }


def save_profile(student, data):
    data = data or {}
    if data.get("full_name") and not is_valid_full_name(data.get("full_name")):
        return None, "Enter a valid full name (letters only, at least 2 characters)"
    if "phone" in data and not is_valid_phone(data.get("phone")):
        return None, "Enter a valid phone number (10–15 digits)"
    update_student(student["id"], data)
    return get_profile(get_student_by_user_id(student["user_id"])), None


def create_education(student, data):
    missing = require_fields(data, ["institution", "degree"])
    if missing:
        return None, f"Missing fields: {', '.join(missing)}"
    edu_id = add_education(student["id"], data)
    return get_education(edu_id, student["id"]), None


def edit_education(student, edu_id, data):
    existing = get_education(edu_id, student["id"])
    if not existing:
        return None, "Education record not found"
    missing = require_fields(data, ["institution", "degree"])
    if missing:
        return None, f"Missing fields: {', '.join(missing)}"
    update_education(edu_id, student["id"], data)
    return get_education(edu_id, student["id"]), None


def remove_education(student, edu_id):
    count = delete_education(edu_id, student["id"])
    return count > 0


def create_skill(student, data):
    name = (data.get("name") or "").strip()
    if not name:
        return None, "Skill name is required"
    add_student_skill(student["id"], name)
    return list_student_skills(student["id"]), None


def remove_skill(student, skill_link_id):
    count = delete_student_skill(skill_link_id, student["id"])
    return count > 0
