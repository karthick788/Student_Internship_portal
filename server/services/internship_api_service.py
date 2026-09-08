import requests
from config.settings import Config
from models.internship_model import upsert_internship
from utils.validators import is_safe_http_url, clean_str

REMOTIVE_URL = "https://remotive.com/api/remote-jobs"


def _map_work_mode(text):
    value = (text or "").lower()
    if "remote" in value:
        return "remote"
    if "hybrid" in value:
        return "hybrid"
    return "onsite"


def _normalize_generic(item, source):
    url = item.get("application_url") or item.get("url") or item.get("job_url")
    if url and not is_safe_http_url(url):
        url = None
    title = clean_str(item.get("title") or item.get("job_title"), 255) or "Internship"
    company = clean_str(item.get("company_name") or item.get("company") or item.get("company_name"), 200) or "Unknown"
    tags = item.get("tags") or item.get("skills") or []
    if isinstance(tags, list):
        skills = ", ".join(str(t) for t in tags[:12])
    else:
        skills = clean_str(tags, 500)
    return {
        "external_id": str(item.get("id") or item.get("external_id") or title + company)[:180],
        "source": source,
        "title": title,
        "company_name": company,
        "description": item.get("description") or item.get("job_description") or "",
        "location": clean_str(item.get("candidate_required_location") or item.get("location") or "Remote", 150),
        "work_mode": _map_work_mode(item.get("job_type") or item.get("work_mode") or item.get("candidate_required_location")),
        "skills": skills,
        "duration": clean_str(item.get("duration") or "Not specified", 80),
        "stipend": clean_str(item.get("stipend") or item.get("salary") or "See listing", 80),
        "eligibility": clean_str(item.get("eligibility") or "See original listing", 500),
        "deadline": None,
        "application_method": "external" if url else "internal",
        "application_url": url,
    }


def fetch_from_remotive():
    response = requests.get(REMOTIVE_URL, params={"search": "intern"}, timeout=25)
    response.raise_for_status()
    payload = response.json()
    jobs = payload.get("jobs") or []
    mapped = []
    for job in jobs:
        title = (job.get("title") or "").lower()
        if "intern" not in title and "internship" not in title:
            continue
        mapped.append(_normalize_generic(job, "remotive"))
        if len(mapped) >= 40:
            break
    if not mapped:
        for job in jobs[:20]:
            mapped.append(_normalize_generic(job, "remotive"))
    return mapped


def fetch_from_configured_api():
    headers = {}
    if Config.INTERNSHIP_API_KEY:
        headers["Authorization"] = f"Bearer {Config.INTERNSHIP_API_KEY}"
        headers["X-API-Key"] = Config.INTERNSHIP_API_KEY
    response = requests.get(Config.INTERNSHIP_API_URL, headers=headers, timeout=25)
    response.raise_for_status()
    payload = response.json()
    if isinstance(payload, dict):
        items = payload.get("jobs") or payload.get("data") or payload.get("results") or payload.get("internships") or []
    else:
        items = payload
    return [_normalize_generic(item, "configured") for item in items]


def sync_internships():
    if Config.INTERNSHIP_API_URL:
        listings = fetch_from_configured_api()
    else:
        listings = fetch_from_remotive()

    inserted = 0
    updated = 0
    for listing in listings:
        _, action = upsert_internship(listing)
        if action == "inserted":
            inserted += 1
        else:
            updated += 1
    return {"fetched": len(listings), "inserted": inserted, "updated": updated}
