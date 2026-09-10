import uuid
from datetime import datetime
from models.db import execute, fetch_all, fetch_one


def create_application(student_id, internship_id, cover_note=None):
    app_id, _ = execute(
        """
        INSERT INTO applications (application_code, student_id, internship_id, status, cover_note)
        VALUES (%s, %s, %s, 'submitted', %s)
        """,
        (f"TEMP-{uuid.uuid4().hex[:8]}", student_id, internship_id, cover_note),
    )
    execute(
        "UPDATE applications SET application_code = %s WHERE id = %s",
        (f"APP-{datetime.now().year}-{app_id:06d}", app_id),
    )
    return get_application(app_id, student_id)


def get_existing_application(student_id, internship_id):
    return fetch_one(
        "SELECT * FROM applications WHERE student_id = %s AND internship_id = %s",
        (student_id, internship_id),
    )


def get_application(app_id, student_id):
    return fetch_one(
        """
        SELECT a.*, i.title, i.company_name, i.location, i.work_mode, i.application_method
        FROM applications a
        JOIN internships i ON i.id = a.internship_id
        WHERE a.id = %s AND a.student_id = %s
        """,
        (app_id, student_id),
    )


def list_applications(student_id):
    return fetch_all(
        """
        SELECT a.*, i.title, i.company_name, i.location, i.work_mode
        FROM applications a
        JOIN internships i ON i.id = a.internship_id
        WHERE a.student_id = %s
        ORDER BY a.created_at DESC
        """,
        (student_id,),
    )


def count_applications(student_id):
    row = fetch_one(
        "SELECT COUNT(*) AS total FROM applications WHERE student_id = %s",
        (student_id,),
    )
    return row["total"] if row else 0
