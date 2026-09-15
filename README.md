# Student Internship Portal

A student internship discovery and management platform built with **HTML/CSS/JavaScript**, **Python Flask**, and **MySQL**.

Students register, manage profiles, upload resumes, browse internships (seed data plus an optional external sync), save opportunities, apply internally or via external links, and track applications. Status changes and new applications send email through **EmailJS**. Staff use a separate **admin** login to review applications and students.

## Architecture

```text
External internship API → Flask backend → MySQL → REST API → Frontend (Fetch)
EmailJS (server-side)   ↗
```

- **Frontend:** `http://localhost:5173` (static server)
- **Backend:** `http://localhost:5000`
- **Database:** MySQL (`internship_management`), local or hosted (for example Aiven)

## Project structure

```text
Student_Internship_portal/
├── client/           # HTML, CSS, JavaScript frontend
│   ├── admin/        # Admin login and dashboard
│   ├── pages/        # Student app pages
│   └── js/           # API client and page scripts
├── server/           # Flask REST API
├── database/         # Schema, seed data, and migrations
└── README.md
```

## Prerequisites

- Python 3.10+
- MySQL 8+ (local or cloud)
- A static file server for `client/` (VS Code Live Server, or `python -m http.server`)

## Setup

### 1. Create the database

```sql
CREATE DATABASE internship_management;
```

Import schema and seed internships:

```bash
mysql -u root -p internship_management < database/database.sql
```

If the database already exists from an older schema, apply the admin-role migration:

```bash
mysql -u root -p internship_management < database/V2__admin_role.sql
```

### 2. Configure the backend

```bash
cd server
copy .env.example .env
```

Edit `server/.env`:

- MySQL host, port, user, password, and database name
- For **Aiven**, set `DB_SSL_CA` to the path of the downloaded `ca.pem`
- `SECRET_KEY` and `JWT_SECRET_KEY`
- EmailJS: `EMAILJS_SERVICE_ID`, `EMAILJS_TEMPLATE_ID`, `EMAILJS_PUBLIC_KEY`, `EMAILJS_PRIVATE_KEY`
- In EmailJS, allow **API access from non-browser environments** so Flask can send mail
- Template variables: `email`, `subject`, `name`, `message`, `internship_title`, `application_code`, `status`

Do not commit `server/.env`.

### 3. Install Python dependencies

```bash
cd server
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Start the backend

```bash
cd server
python app.py
```

Health check: `http://localhost:5000/api/health`

### 5. Start the frontend

From the `client` folder:

```bash
python -m http.server 5173
```

Open `http://localhost:5173`

## Accounts

**Student**

1. Register at `/register.html`
2. Log in at `/login.html`
3. Complete profile, education, skills, and resume
4. Browse internships, save, and apply
5. Track applications at **My Applications** (each student sees only their own)

Internal apply creates an `APP-YYYY-XXXXXX` code and sends a confirmation email. External apply opens the original application URL.

**Admin**

- URL: `http://localhost:5173/admin/login.html`
- Default (change after first login): `admin@internhub.local` / `Admin@1234`
- Dashboard lists all applications (status dropdown) and all students
- Changing status emails the student through EmailJS
- Admin sessions cannot use student API routes

## API sync

From the student dashboard, use **Sync External Internships**.

- If `INTERNSHIP_API_URL` is set, that API is used
- Otherwise the backend uses the public Remotive jobs API (`search=intern`)

Protected endpoint: `POST /api/internships/sync` (student JWT)

## Security

- bcrypt password hashing
- JWT authentication and role checks (`student` vs `admin`)
- Parameterized MySQL queries
- CORS limited to `CLIENT_ORIGINS`
- Resume upload validation (PDF/DOC/DOCX, 5 MB max)
- External URLs validated as HTTP/HTTPS
- Secrets stay in `.env` (EmailJS private key is never sent to the browser)

## Main API routes

| Method | Route | Description |
|--------|-------|-------------|
| POST | `/api/auth/register` | Student registration |
| POST | `/api/auth/login` | Login + JWT (`role` in payload) |
| GET | `/api/internships` | List/search internships |
| POST | `/api/internships/sync` | Sync external internships |
| POST | `/api/applications` | Apply (student) |
| GET | `/api/applications` | Current student’s applications |
| POST | `/api/saved-internships/:id` | Save internship |
| GET | `/api/admin/applications` | All applications (admin) |
| PATCH | `/api/admin/applications/:id/status` | Update application status (admin) |
| GET | `/api/admin/students` | All students (admin) |
| GET | `/api/linkedin-internships` | LinkedIn search links |

## Testing checklist

- Student register / login / logout
- Profile, education, skills, resume upload
- Internship search, filters, save/unsave
- Internal apply + application code + email
- External apply redirect
- Student sees only their applications
- Admin login; applications and students tables
- Admin status change + student email
- LinkedIn search links

## Notes

- Seed internships come from `database/database.sql` so you can test without API sync.
- Email is sent from Flask via EmailJS, not from the browser.
- There is no LinkedIn scraping — only stored search URLs.
