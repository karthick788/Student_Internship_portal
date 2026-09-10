from models.notification_model import (
    create_notification,
    list_notifications,
    mark_all_read,
    mark_read,
    unread_count,
)


def get_student_notifications(student_id):
    return {
        "items": list_notifications(student_id),
        "unread": unread_count(student_id),
    }


def read_notification(notification_id, student_id):
    updated = mark_read(notification_id, student_id)
    return updated > 0


def read_all_notifications(student_id):
    return mark_all_read(student_id)


def notify(student_id, title, message):
    create_notification(student_id, title, message)
