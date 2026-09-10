# InternHub — Aiven (Free) MySQL Setup Guide

## Why Aiven?

- ✅ **Truly free** — no credit card required for the free tier
- ✅ **Always-on** — does not sleep or delete data
- ✅ **Full MySQL 8.0** — FK constraints, all features supported
- ✅ **1 GB storage** — more than enough for a student portal
- ✅ **Managed** — automated backups, SSL by default
- ✅ **Use original `database.sql`** — no need for the PlanetScale FK-stripped version

---

## Step 1 — Create Aiven Account

1. Go to **[https://aiven.io](https://aiven.io)**
2. Click **"Sign up free"** — use GitHub, Google, or email
3. **No credit card required** for the free plan
4. Verify your email if prompted

---

## Step 2 — Create a Free MySQL Service

1. In Aiven Console → click **"+ Create service"**
2. Choose **MySQL**
3. **Cloud provider:** Any (recommend `AWS` → `ap-south-1` for India)
4. **Plan:** Select **"Free"** (shown as `Hobbyist` or `Free`)
   > If you see no "Free" tier listed, scroll to the very bottom of the plan list — it's the smallest option
5. **Service name:** `internhub-mysql` (or any name you like)
6. Click **"Create free service"**
7. Wait ~2 minutes for provisioning (status changes from "Rebuilding" to "Running")

---

## Step 3 — Download the SSL CA Certificate

Aiven **requires SSL** for all connections. You must download their CA cert.

1. Open your service → click **"Overview"** tab
2. Scroll down to **"Connection information"**
3. Click **"Download CA cert"** → saves as `ca.pem`
4. Move `ca.pem` to your project:
   ```
   d:\Dk\Karthi\Student_Internship_portal\server\ca.pem
   ```
   > ⚠️ This file is already in `.gitignore` (we'll add it). Do NOT commit it.

---

## Step 4 — Get Connection Details

On the service Overview page, find **"Connection information"** → **"MySQL"**:

| Field | Where to find it |
|---|---|
| `Host` | e.g. `mysql-internhub-xxxx.aivencloud.com` |
| `Port` | e.g. `12345` (NOT 3306 — Aiven uses a custom port) |
| `User` | `avnadmin` |
| `Password` | Click the eye icon to reveal |
| `Database` | `defaultdb` (rename it or use as-is) |

---

## Step 5 — Import the Schema

### Option A — Aiven Console (Recommended)

1. In Aiven dashboard → your service → **"Query editor"** tab
2. Open `database/database.sql` in a text editor
3. Copy all content, paste into the Query editor
4. Click **Run** — all tables and seed data will be created

> **Note:** You can use the original `database.sql` with Aiven — FK constraints are fully supported!

### Option B — MySQL CLI (if installed locally)

```bash
# Replace the placeholders with your actual values
mysql --host=mysql-internhub-xxxx.aivencloud.com \
      --port=12345 \
      --user=avnadmin \
      --password=YOUR_PASSWORD \
      --ssl-ca=server/ca.pem \
      defaultdb < database/database.sql
```

---

## Step 6 — Update Your `.env` File

Open `server/.env` and update:

```env
DB_HOST=mysql-internhub-xxxx.aivencloud.com    # your Aiven host
DB_PORT=12345                                   # your Aiven port (NOT 3306)
DB_USER=avnadmin
DB_PASSWORD=your_aiven_password
DB_NAME=defaultdb
DB_SSL_CA=ca.pem                                # relative path from server/ directory
DB_POOL_SIZE=5                                  # Aiven free tier: keep pool small
```

> **Important:** The `DB_SSL_CA` path is resolved relative to where you run `python app.py` (the `server/` directory). So `ca.pem` means `server/ca.pem`.

---

## Step 7 — Add ca.pem to .gitignore

Open `server/.gitignore` or the root `.gitignore` and add:

```
server/ca.pem
ca.pem
```

---

## Step 8 — Test the Connection

```bash
cd server
python -c "
from config.database import get_connection
conn = get_connection()
print('✅ Connected to Aiven MySQL successfully!')
conn.close()
"
```

You should see: `✅ Connected to Aiven MySQL successfully!`

Then start the server:
```bash
python app.py
```

Visit: `http://localhost:5000/api/internships` — you should see the 6 seeded internships.

---

## Free Tier Limits (Aiven Hobbyist/Free)

| Resource | Limit |
|---|---|
| Storage | 1 GB |
| RAM | 1 GB |
| CPU | 1 vCPU |
| Connections | ~20 simultaneous |
| Backups | Automatic daily |
| SSL | Always on (required) |

> **Pool size tip:** Set `DB_POOL_SIZE=5` in `.env` — the free tier supports ~20 connections maximum. Keep the pool small to avoid exhausting the limit.

---

## Phase 3 Schema Migration (Admin Role)

When you reach Phase 3, run this SQL in the Aiven Query Editor:

```sql
ALTER TABLE users MODIFY COLUMN role ENUM('student', 'admin') NOT NULL DEFAULT 'student';

INSERT INTO users (email, password_hash, role) VALUES
  ('admin@internhub.local', '$2b$12$REPLACE_WITH_ACTUAL_BCRYPT_HASH', 'admin');
```

---

## Troubleshooting

| Error | Fix |
|---|---|
| `SSL connection error` or `Certificate verify failed` | Check `DB_SSL_CA` path is correct; run from `server/` directory |
| `Access denied for user 'avnadmin'` | Double-check password — copy it fresh from Aiven dashboard |
| `Can't connect to MySQL server on host` | Verify `DB_HOST` and `DB_PORT` from Aiven → exactly match |
| `Pool size too large` | Reduce `DB_POOL_SIZE` to `5` in `.env` |
| Service shows "Rebuilding" | Wait 2–5 minutes for Aiven to finish provisioning |
| `defaultdb` not found | Use the exact database name shown in Aiven connection info |
