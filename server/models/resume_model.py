from models.db import execute, fetch_all, fetch_one


def save_resume(student_id, stored_name, original_name, file_path, mime_type, file_size, gridfs_file_id):
    resume_id, _ = execute(
        """
        INSERT INTO resumes (student_id, stored_name, original_name, file_path, mime_type, file_size, gridfs_file_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (student_id, stored_name, original_name, file_path, mime_type, file_size, gridfs_file_id),
    )
    return resume_id


def latest_resume(student_id):
    return fetch_one(
        "SELECT * FROM resumes WHERE student_id = %s ORDER BY uploaded_at DESC, id DESC LIMIT 1",
        (student_id,),
    )


def list_resumes(student_id):
    return fetch_all(
        "SELECT id, original_name, mime_type, file_size, uploaded_at, gridfs_file_id FROM resumes WHERE student_id = %s ORDER BY uploaded_at DESC",
        (student_id,),
    )

