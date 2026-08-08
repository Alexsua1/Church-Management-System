# Church Management System
### The Church of Pentecost — Oforikrom Central

A full-featured church management system built with **Django (Python)**, **Bootstrap 5**,
and **PostgreSQL**, matching the specification you provided.

---

## ✅ Tech stack

| Component        | Technology              |
|-------------------|--------------------------|
| Front end          | HTML, CSS, JavaScript |
| UI framework        | Bootstrap 5 |
| Back end           | Django (Python) |
| Database           | PostgreSQL (SQLite fallback for quick local testing) |
| Authentication      | Django Authentication (custom `User` model + role-based access) |
| Cloud storage       | Firebase Storage (config placeholders included — see below) |
| Deployment          | Windows-friendly (works with `runserver`, or IIS + waitress / gunicorn+nginx) |

## ✅ What's included

- **9 Django apps** under `backend/`: `accounts`, `members`, `attendance`, `finance`,
  `departments`, `events`, `inventory`, `reports`, `dashboard`.
- **Custom `User` model** with roles: Administrator, Pastor, Secretary, Finance Officer, Member —
  each redirected to its own dashboard on login.
- **Multi-branch support** via a `Branch` model (Oforikrom Central is pre-configured; add more
  branches from Django admin).
- **Public site**: Home, About, Contact, Events, Online Donation (Paystack-ready).
- **Member management**: register/update/delete members, auto-generated **QR code** per member
  for QR-code attendance.
- **Attendance**: create a session, take attendance manually, or let members self check-in by
  scanning a QR code linked to `/attendance/checkin/<token>/`.
- **Finance**: record tithes/offerings/donations and expenses, approve expenses, running balance.
- **Departments, Events & Announcements** (with SMS/WhatsApp send flags ready to wire to a provider).
- **Inventory** tracking.
- **Reports**: export Members & Attendance to **Excel**, Finance to **PDF** — all working out of the box.
- **Dark mode** toggle (saved in the browser).
- Branding uses your church logo (`static/images/church_logo.jpg`) and navy/gold color scheme.

## 🧩 Features that are scaffolded (need a provider API key to go live)

These are wired into settings/models/forms but need real credentials to fully function:
- **SMS notifications** — set `SMS_PROVIDER_API_KEY` in `.env` and call your provider inside
  `backend/events/views.py::announcement_create` (marked with a `TODO`).
- **WhatsApp notifications** — same pattern, `WHATSAPP_PROVIDER_API_KEY`.
- **Online payments** — `backend/accounts/views_public.py::donate` currently records the donation
  directly; swap in a Paystack checkout session + webhook using `PAYSTACK_SECRET_KEY`.
- **Firebase Storage** — `USE_FIREBASE_STORAGE` + `FIREBASE_*` keys in `.env`. By default the app
  stores uploaded photos/receipts locally in `/media`. To use Firebase, install
  `firebase-admin` (already in `requirements.txt`) and add a custom Django storage backend.
- **Data backup** — use `python manage.py dumpdata` on a schedule (e.g. Windows Task Scheduler)
  or `pg_dump` for PostgreSQL.

---

## 🚀 Setup on Windows

### 1. Prerequisites
- Python 3.11+ ([python.org](https://www.python.org/downloads/))
- PostgreSQL 14+ ([postgresql.org](https://www.postgresql.org/download/windows/)) — optional if
  you just want to try it out with SQLite first
- Git (optional)

### 2. Get the project running

Open **PowerShell** or **Command Prompt** in the project folder:

```powershell
# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
```

Edit `.env` with Notepad. For the fastest way to try the system out, keep:
```
USE_SQLITE=True
```
This skips PostgreSQL entirely and uses a local `database/db.sqlite3` file.

To use PostgreSQL instead: create a database in pgAdmin (e.g. `church_management_db`), set
`USE_SQLITE=False`, and fill in `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`.

### 3. Initialize the database

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

When creating the superuser, Django will only ask for username/email/password — after that,
log into `/admin/` and set that user's **Role** to `Administrator` and assign a **Branch**
(create "Oforikrom Central" first under Branches if it isn't there).

### 4. Run the server

```powershell
python manage.py runserver
```

Visit:
- Public site: http://127.0.0.1:8000/
- Staff login: http://127.0.0.1:8000/accounts/login/
- Django admin: http://127.0.0.1:8000/admin/

### 5. Collect static files (for production only)

```powershell
python manage.py collectstatic
```

---

## 👤 User roles & where they land after login

| Role | Dashboard | Typical tasks |
|------|-----------|----------------|
| Administrator | Full dashboard | Everything — user management, all modules |
| Pastor | Pastor dashboard | Member info, attendance records, announcements, reports |
| Secretary | Secretary dashboard | Register members, update info, generate reports |
| Finance Officer | Finance dashboard | Record tithes/offerings, expenses, generate financial reports |
| Member | Member dashboard | View own info, upcoming events |

Create staff accounts from **Dashboard → User Management** (Administrator only) or via
`/admin/`.

## 📁 Project structure

```
church-management-system/
├── backend/
│   ├── accounts/        # Custom User, Branch, roles, login/logout, public pages
│   ├── members/         # Member registration, QR codes
│   ├── attendance/      # Sessions, manual + QR check-in
│   ├── finance/         # Offerings/tithes, expenses
│   ├── departments/     # Departments/ministries
│   ├── events/          # Events + announcements
│   ├── inventory/       # Church assets
│   ├── reports/         # Excel/PDF report generation
│   └── dashboard/       # Role-aware dashboard router
├── templates/           # Bootstrap templates (public/, dashboard/, per-module)
├── static/               # css/, js/, images/ (church logo + branding)
├── database/             # sqlite file lives here when USE_SQLITE=True
├── churchms/              # Django project settings/urls
├── requirements.txt
├── .env.example
└── manage.py
```

## 🔒 Security notes before going live

- Set `DEBUG=False` and a strong random `SECRET_KEY` in production.
- Set `ALLOWED_HOSTS` to your real domain.
- Serve static files via `whitenoise` (already included) or a proper web server.
- Put PostgreSQL credentials only in `.env` — never commit `.env` to version control.
echo "# Church-Management-System" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/Alexsua1/Church-Management-System.git
git push -u origin main