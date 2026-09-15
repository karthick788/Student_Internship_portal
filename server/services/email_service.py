import requests
from config.settings import Config
from utils.logger import get_logger

logger = get_logger("email")
EMAILJS_URL = "https://api.emailjs.com/api/v1.0/email/send"


def _configured():
    return bool(
        Config.EMAILJS_SERVICE_ID
        and Config.EMAILJS_TEMPLATE_ID
        and Config.EMAILJS_PUBLIC_KEY
    )


def send_email(to_email, to_name, subject, message, extra=None):
    if not _configured():
        return False, "not_configured"
    if not to_email:
        return False, "no_email"
    params = {
        "to_email": to_email,
        "email": to_email,
        "to_name": to_name or "Student",
        "name": to_name or "Student",
        "subject": subject,
        "title": subject,
        "message": message,
    }
    if extra:
        params.update(extra)
    payload = {
        "service_id": Config.EMAILJS_SERVICE_ID,
        "template_id": Config.EMAILJS_TEMPLATE_ID,
        "user_id": Config.EMAILJS_PUBLIC_KEY,
        "template_params": params,
    }
    if Config.EMAILJS_PRIVATE_KEY:
        payload["accessToken"] = Config.EMAILJS_PRIVATE_KEY
    try:
        response = requests.post(
            EMAILJS_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=15,
        )
        if response.ok:
            logger.info("EmailJS sent to %s", to_email)
            return True, "sent"
        error = (response.text or f"HTTP {response.status_code}")[:300]
        logger.warning("EmailJS send failed for %s: %s", to_email, error)
        if "non-browser" in error.lower():
            return False, "enable_non_browser_api"
        return False, "send_failed"
    except Exception:
        logger.exception("EmailJS send error")
        return False, "send_error"


def send_application_email(student, internship, application_code):
    title = (internship or {}).get("title") or "Internship"
    name = (student or {}).get("full_name") or "Student"
    email = (student or {}).get("email")
    message = (
        f"Hello {name},\n\n"
        f"You have successfully applied on InternHub.\n\n"
        f"Internship: {title}\n"
        f"Application ID: {application_code}\n\n"
        "We will email you when your application status changes.\n"
        "Thank you."
    )
    ok, reason = send_email(
        email,
        name,
        "InternHub application submitted",
        message,
        {"internship_title": title, "application_code": application_code or "", "status": "submitted"},
    )
    return {"sent": ok, "reason": None if ok else reason, "to": email}


def send_status_email(student, application_code, status):
    name = (student or {}).get("full_name") or "Student"
    email = (student or {}).get("email")
    label = (status or "").replace("_", " ").title()
    message = (
        f"Hello {name},\n\n"
        f"Your InternHub application was updated.\n\n"
        f"Application ID: {application_code}\n"
        f"Status: {label}\n\n"
        "Thank you."
    )
    return send_email(
        email,
        name,
        "InternHub application update",
        message,
        {"application_code": application_code or "", "status": label},
    )
