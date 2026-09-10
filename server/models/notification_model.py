from models.db import execute, fetch_all, fetch_one


def create_notification(student_id, title, message):
    execute(
        "INSERT INTO notifications (student_id, title, message) VALUES (%s, %s, %s)",
        (student_id, title, message),
    )


def list_notifications(student_id):
    return fetch_all(
        "SELECT * FROM notifications WHERE student_id = %s ORDER BY created_at DESC, id DESC",
        (student_id,),
    )


def mark_read(notification_id, student_id):
    _, count = execute(
        "UPDATE notifications SET is_read = 1 WHERE id = %s AND student_id = %s",
        (notification_id, student_id),
    )
    return count


def mark_all_read(student_id):
    _, count = execute(
        "UPDATE notifications SET is_read = 1 WHERE student_id = %s AND is_read = 0",
        (student_id,),
    )
    return count


def unread_count(student_id):
    row = fetch_one(
        "SELECT COUNT(*) AS total FROM notifications WHERE student_id = %s AND is_read = 0",
        (student_id,),
    )
    return row["total"] if row else 0
