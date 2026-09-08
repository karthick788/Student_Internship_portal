from contextlib import contextmanager
from mysql.connector import Error
from config.database import get_connection
from utils.helpers import row_to_dict, rows_to_list


@contextmanager
def db_cursor(commit=False):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        yield cursor
        if commit:
            conn.commit()
    except Error:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


def fetch_one(query, params=None):
    with db_cursor() as cursor:
        cursor.execute(query, params or ())
        return row_to_dict(cursor.fetchone())


def fetch_all(query, params=None):
    with db_cursor() as cursor:
        cursor.execute(query, params or ())
        return rows_to_list(cursor.fetchall())


def execute(query, params=None, commit=True):
    with db_cursor(commit=commit) as cursor:
        cursor.execute(query, params or ())
        return cursor.lastrowid, cursor.rowcount
