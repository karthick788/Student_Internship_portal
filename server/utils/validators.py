import re
from urllib.parse import urlparse

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_valid_email(value):
    return bool(value and EMAIL_RE.match(value.strip()))


def require_fields(data, fields):
    missing = [f for f in fields if not str(data.get(f, "")).strip()]
    return missing


def is_safe_http_url(value):
    if not value:
        return False
    parsed = urlparse(value.strip())
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


def clean_str(value, max_len=255):
    if value is None:
        return None
    text = str(value).strip()
    return text[:max_len] if text else None
