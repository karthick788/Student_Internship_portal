from datetime import date, datetime
from decimal import Decimal


def row_to_dict(row):
    if row is None:
        return None
    result = {}
    for key, value in row.items():
        if isinstance(value, datetime):
            result[key] = value.isoformat(sep=" ", timespec="seconds")
        elif isinstance(value, date):
            result[key] = value.isoformat()
        elif isinstance(value, Decimal):
            result[key] = str(value)
        elif isinstance(value, bytes):
            result[key] = value.decode("utf-8", errors="ignore")
        else:
            result[key] = value
    return result


def rows_to_list(rows):
    return [row_to_dict(r) for r in rows]
