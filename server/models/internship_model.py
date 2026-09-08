from models.db import execute, fetch_all, fetch_one


def find_by_source_external(source, external_id):
    if not external_id:
        return None
    return fetch_one(
        "SELECT * FROM internships WHERE source = %s AND external_id = %s",
        (source, external_id),
    )


def upsert_internship(data):
    existing = find_by_source_external(data.get("source"), data.get("external_id"))
    fields = (
        data.get("title"),
        data.get("company_name"),
        data.get("description"),
        data.get("location"),
        data.get("work_mode") or "onsite",
        data.get("skills"),
        data.get("duration"),
        data.get("stipend"),
        data.get("eligibility"),
        data.get("deadline"),
        data.get("application_method") or "external",
        data.get("application_url"),
        data.get("source"),
        data.get("external_id"),
    )
    if existing:
        execute(
            """
            UPDATE internships
            SET title=%s, company_name=%s, description=%s, location=%s, work_mode=%s,
                skills=%s, duration=%s, stipend=%s, eligibility=%s, deadline=%s,
                application_method=%s, application_url=%s
            WHERE id=%s
            """,
            fields[:-2] + (existing["id"],),
        )
        return existing["id"], "updated"
    intern_id, _ = execute(
        """
        INSERT INTO internships
          (title, company_name, description, location, work_mode, skills, duration,
           stipend, eligibility, deadline, application_method, application_url, source, external_id)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        fields,
    )
    return intern_id, "inserted"


def list_internships(filters):
    clauses = ["1=1"]
    params = []
    search = (filters.get("search") or "").strip()
    if search:
        clauses.append(
            "(title LIKE %s OR company_name LIKE %s OR skills LIKE %s OR description LIKE %s)"
        )
        like = f"%{search}%"
        params.extend([like, like, like, like])
    if filters.get("location"):
        clauses.append("location LIKE %s")
        params.append(f"%{filters['location']}%")
    if filters.get("skills"):
        clauses.append("skills LIKE %s")
        params.append(f"%{filters['skills']}%")
    if filters.get("work_mode"):
        clauses.append("work_mode = %s")
        params.append(filters["work_mode"])
    if filters.get("duration"):
        clauses.append("duration LIKE %s")
        params.append(f"%{filters['duration']}%")
    if filters.get("stipend"):
        clauses.append("stipend LIKE %s")
        params.append(f"%{filters['stipend']}%")
    sql = f"SELECT * FROM internships WHERE {' AND '.join(clauses)} ORDER BY updated_at DESC, id DESC"
    return fetch_all(sql, tuple(params))


def get_internship(internship_id):
    return fetch_one("SELECT * FROM internships WHERE id = %s", (internship_id,))


def count_internships():
    row = fetch_one("SELECT COUNT(*) AS total FROM internships")
    return row["total"] if row else 0
