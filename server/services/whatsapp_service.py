from urllib.parse import quote


def build_message(internship_title, application_code):
    return (
        "Hello,\n\n"
        "I have successfully applied for:\n\n"
        f"Internship: {internship_title}\n"
        f"Application ID: {application_code}\n\n"
        "Thank you."
    )


def build_whatsapp_payload(student, internship, application_code):
    message = build_message(internship.get("title"), application_code)
    phone = "".join(ch for ch in (student.get("phone") or "") if ch.isdigit())
    if phone.startswith("0"):
        phone = phone[1:]
    if len(phone) == 10:
        phone = "91" + phone
    base = f"https://wa.me/{phone}" if len(phone) >= 11 else "https://wa.me/"
    link = f"{base}?text={quote(message)}"
    return {
        "message": message,
        "click_to_chat_url": link,
        "cloud_api_ready": False,
    }
