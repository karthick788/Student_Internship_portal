from models.db import fetch_all, fetch_one


def list_linkedin():
    return fetch_all("SELECT * FROM linkedin_internships ORDER BY id DESC")


def get_linkedin(item_id):
    return fetch_one("SELECT * FROM linkedin_internships WHERE id = %s", (item_id,))
