# Student Internship Management System

A student-focused internship discovery and management platform built with **HTML/CSS/JavaScript**, **Python Flask**, and **MySQL**.

Students can register, manage profiles, upload resumes, discover internships (from external APIs + seed data), save opportunities, apply internally or via external links, track applications, receive notifications, and open LinkedIn internship searches.

## Architecture

```text
External Internship API → Flask Backend → MySQL → REST API → Frontend (Fetch)
```

- **Frontend:** `http://localhost:5173` (Live Server / static server)
- **Backend:** `http://localhost:5000`
- **Database:** `internship_management` on MySQL (`localhost:3306`)

## Project Structure

```text
student-internship-management/
├── client/          # HTML, CSS, JavaScript frontend
├── server/          # Flask REST API
├── database/        # MySQL schema + seed data
└── README.md
```

## Prerequisites

- Python 3.10+
- MySQL 8+
- VS Code with Live Server (or any static file server)

## Setup

### 1. Create database

```sql
CREATE DATABASE internship_management;
```

Import schema and seed data:

```bash
mysql -u root -p internship_management < database/database.sql
```

### 2. Configure backend

```bash
cd server
copy .env.example .env
```

Edit `server/.env` and set your MySQL password and secret keys.

### 3. Install Python dependencies

```bash
cd server
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Start backend

```bash
python app.py
```

Health check: `http://localhost:5000/api/health`

### 5. Start frontend

Open the `client` folder in VS Code and run **Live Server** on `index.html`.

Open: `http://localhost:5173`

## End-to-end student flow

1. Register at `/register.html`
2. Login and open Dashboard
3. Update profile, education, skills, and upload resume
4. Browse internships, search/filter, view details
5. Save internships or apply
6. Internal apply generates `APP-YYYY-XXXXXX` and WhatsApp link
7. External apply opens the original application URL
8. Track applications and notifications
9. Use LinkedIn page for official LinkedIn job search links

## API sync

From the dashboard, click **Sync External Internships**.

- If `INTERNSHIP_API_URL` is set in `.env`, that API is used.
- Otherwise the backend uses the public **Remotive** jobs API (`search=intern`).

Protected endpoint: `POST /api/internships/sync` (JWT required)

## Security

- bcrypt password hashing
- JWT authentication
- Parameterized MySQL queries
- CORS restricted to frontend origin
- Resume upload validation (PDF/DOC/DOCX, 5 MB max)
- External URLs validated as HTTP/HTTPS
- API keys stored in `.env` only (never in frontend)

## Main API routes

| Method | Route | Description |
|--------|-------|-------------|
| POST | `/api/auth/register` | Student registration |
| POST | `/api/auth/login` | Login + JWT |
| GET | `/api/internships` | List/search internships |
| POST | `/api/internships/sync` | Sync external internships |
| POST | `/api/applications` | Apply for internship |
| POST | `/api/saved-internships/:id` | Save internship |
| GET | `/api/notifications` | Student notifications |
| GET | `/api/linkedin-internships` | LinkedIn search links |

## Testing checklist

- Register / login / logout
- Profile, education, skills CRUD
- Resume upload
- Internship search and filters
- Save / unsave internships
- Internal apply + application ID + WhatsApp
- External apply redirect
- Notifications
- LinkedIn links open correctly

## Notes

- Seed internships are inserted by `database/database.sql` for immediate testing without API sync.
- WhatsApp uses click-to-chat URL generation; Cloud API credentials are optional for future use.
- No LinkedIn scraping — only stored search URLs.
