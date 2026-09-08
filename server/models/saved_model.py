from models.db import execute, fetch_all, fetch_one


def save_internship(student_id, internship_id):
    existing = fetch_one(
        "SELECT * FROM saved_internships WHERE student_id = %s AND internship_id = %s",
        (student_id, internship_id),
    )
    if existing:
        return existing
    execute(
        "INSERT INTO saved_internships (student_id, internship_id) VALUES (%s, %s)",
        (student_id, internship_id),
    )
    return fetch_one(
        "SELECT * FROM saved_internships WHERE student_id = %s AND internship_id = %s",
        (student_id, internship_id),
    )


def unsave_internship(student_id, internship_id):
    _, count = execute(
        "DELETE FROM saved_internships WHERE student_id = %s AND internship_id = %s",
        (student_id, internship_id),
    )
    return count


def list_saved(student_id):
    return fetch_all(
        """
        SELECT s.id AS saved_id, s.created_at AS saved_at, i.*
        FROM saved_internships s
        JOIN internships i ON i.id = s.internship_id
        WHERE s.student_id = %s
        ORDER BY s.created_at DESC
        """,
        (student_id,),
    )


def count_saved(student_id):
    row = fetch_one(
        "SELECT COUNT(*) AS total FROM saved_internships WHERE student_id = %s",
        (student_id,),
    )
    return row["total"] if row else 0


def is_saved(student_id, internship_id):
    row = fetch_one(
        "SELECT id FROM saved_internships WHERE student_id = %s AND internship_id = %s",
        (student_id, internship_id),
    )
    return bool(row)
