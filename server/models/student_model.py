from models.db import execute, fetch_all, fetch_one


def create_student(user_id, full_name, phone=None, college=None):
    student_id, _ = execute(
        """
        INSERT INTO students (user_id, full_name, phone, college)
        VALUES (%s, %s, %s, %s)
        """,
        (user_id, full_name, phone, college),
    )
    return student_id


def get_student_by_user_id(user_id):
    return fetch_one(
        """
        SELECT s.*, u.email, u.role
        FROM students s
        JOIN users u ON u.id = s.user_id
        WHERE s.user_id = %s
        """,
        (user_id,),
    )


def ensure_student_for_user(user_id, full_name="Student"):
    existing = get_student_by_user_id(user_id)
    if existing:
        return existing
    name = (full_name or "Student").strip() or "Student"
    create_student(user_id, name[:150], None, None)
    return get_student_by_user_id(user_id)


def get_student_by_id(student_id):
    return fetch_one(
        """
        SELECT s.*, u.email, u.role
        FROM students s
        JOIN users u ON u.id = s.user_id
        WHERE s.id = %s
        """,
        (student_id,),
    )


def update_student(student_id, fields):
    allowed = {
        "full_name",
        "phone",
        "college",
        "course",
        "year_of_study",
        "city",
        "bio",
        "date_of_birth",
    }
    sets = []
    values = []
    for key, value in fields.items():
        if key in allowed:
            sets.append(f"{key} = %s")
            values.append(value if value != "" else None)
    if not sets:
        return
    values.append(student_id)
    execute(f"UPDATE students SET {', '.join(sets)} WHERE id = %s", tuple(values))


def list_education(student_id):
    return fetch_all(
        "SELECT * FROM education WHERE student_id = %s ORDER BY end_year DESC, id DESC",
        (student_id,),
    )


def get_education(edu_id, student_id):
    return fetch_one(
        "SELECT * FROM education WHERE id = %s AND student_id = %s",
        (edu_id, student_id),
    )


def add_education(student_id, data):
    edu_id, _ = execute(
        """
        INSERT INTO education
          (student_id, institution, degree, field_of_study, start_year, end_year, grade)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (
            student_id,
            data.get("institution"),
            data.get("degree"),
            data.get("field_of_study"),
            data.get("start_year") or None,
            data.get("end_year") or None,
            data.get("grade"),
        ),
    )
    return edu_id


def update_education(edu_id, student_id, data):
    execute(
        """
        UPDATE education
        SET institution = %s, degree = %s, field_of_study = %s,
            start_year = %s, end_year = %s, grade = %s
        WHERE id = %s AND student_id = %s
        """,
        (
            data.get("institution"),
            data.get("degree"),
            data.get("field_of_study"),
            data.get("start_year") or None,
            data.get("end_year") or None,
            data.get("grade"),
            edu_id,
            student_id,
        ),
    )


def delete_education(edu_id, student_id):
    _, count = execute(
        "DELETE FROM education WHERE id = %s AND student_id = %s",
        (edu_id, student_id),
    )
    return count


def list_student_skills(student_id):
    return fetch_all(
        """
        SELECT ss.id, s.name
        FROM student_skills ss
        JOIN skills s ON s.id = ss.skill_id
        WHERE ss.student_id = %s
        ORDER BY s.name
        """,
        (student_id,),
    )


def add_student_skill(student_id, name):
    existing = fetch_one("SELECT id FROM skills WHERE name = %s", (name,))
    if existing:
        skill_id = existing["id"]
    else:
        skill_id, _ = execute("INSERT INTO skills (name) VALUES (%s)", (name,))
    link = fetch_one(
        "SELECT id FROM student_skills WHERE student_id = %s AND skill_id = %s",
        (student_id, skill_id),
    )
    if link:
        return link["id"]
    link_id, _ = execute(
        "INSERT INTO student_skills (student_id, skill_id) VALUES (%s, %s)",
        (student_id, skill_id),
    )
    return link_id


def delete_student_skill(link_id, student_id):
    _, count = execute(
        "DELETE FROM student_skills WHERE id = %s AND student_id = %s",
        (link_id, student_id),
    )
    return count
