import re
from urllib.parse import urlparse

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
NAME_RE = re.compile(r"^[A-Za-z][A-Za-z .'-]{1,79}$")
PHONE_RE = re.compile(r"^[0-9+\-() ]{10,20}$")
PASSWORD_RE = re.compile(r"^(?=.*[A-Za-z])(?=.*\d).{8,}$")


def is_valid_email(value):
    return bool(value and EMAIL_RE.match(value.strip()))


def is_valid_full_name(value):
    return bool(value and NAME_RE.match(value.strip()))


def is_valid_phone(value):
    if not value:
        return True
    digits = re.sub(r"\D", "", value)
    return 10 <= len(digits) <= 15 and bool(PHONE_RE.match(value.strip()))


def is_strong_password(value):
    return bool(value and PASSWORD_RE.match(value))


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
