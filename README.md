# 🎓 SRM VEC - CSE Department & Technical Portal

[![Python](https://img.shields.io/badge/Python-3.12-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2_LTS-092E20.svg?style=flat&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D.svg?style=flat&logo=redis&logoColor=white)](https://redis.io/)
[![Celery](https://img.shields.io/badge/Celery-5.3-37814A.svg?style=flat&logo=celery&logoColor=white)](https://docs.celeryq.dev/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![Pytest](https://img.shields.io/badge/Tests-Pytest-0A9EDC.svg?style=flat&logo=pytest&logoColor=white)](https://docs.pytest.org/)

An enterprise-grade web platform and technical publishing engine for the **Department of Computer Science and Engineering** at **SRM Valliammai Engineering College** (An Autonomous Institution, NAAC 'A' Grade, NBA Accredited).

This repository integrates server-rendered **Django 4.2 LTS** web applications, a high-performance **FastAPI** read/integration microservice, **Celery & Redis** asynchronous workers, a cryptographic **WebPush Notification** pipeline, and a dedicated **Student Portal** with a multi-stage **Editorial Review System**.

---

## 🏛️ System Architecture

```
                                  ┌───────────────────────────┐
                                  │      Nginx / Ingress      │
                                  └─────────────┬─────────────┘
                                                │
                     ┌──────────────────────────┴──────────────────────────┐
                     │ (Port 8000)                                         │ (Port 8001)
                     ▼                                                     ▼
      ┌─────────────────────────────┐                       ┌─────────────────────────────┐
      │     Django 4.2 Web App      │                       │     FastAPI Microservice    │
      │  - Server-Rendered UI       │                       │  - High-Speed Read APIs     │
      │  - Student Portal & Auth    │                       │  - Swagger / OpenAPI Docs   │
      │  - Admin Control Panel      │                       │  - Token Integrations       │
      │  - Schema & Migrations      │                       │  - Shared DB Access         │
      └──────────────┬──────────────┘                       └──────────────┬──────────────┘
                     │                                                     │
                     │                 ┌────────────────────┐              │
                     ├─────────────────┤   PostgreSQL 16    ├──────────────┘
                     │                 │ (Shared Datastore) │
                     │                 └────────────────────┘
                     ▼
      ┌─────────────────────────────┐                       ┌─────────────────────────────┐
      │     Redis 7 Message Bus     ├──────────────────────►│    Celery Async Worker      │
      │   (Broker & Result Cache)   │                       │  - WebPush Broadcasts       │
      └─────────────────────────────┘                       │  - Email Notifications      │
                                                            │  - Background Tasks         │
                                                            └──────────────┬──────────────┘
                                                                           │
                                                                           ▼
                                                            ┌─────────────────────────────┐
                                                            │   Browser WebPush Clients   │
                                                            │  (VAPID / Service Worker)   │
                                                            └─────────────────────────────┘
```

---

## ✨ Key Features & Modules

### 1. 🌐 Public Department Portal
- **Cyber IDE Hero Section**: Interactive simulated Python IDE, animated terminal outputs, and live metric feeds.
- **Continuous Tech Marquee**: Dynamic scrolling banner highlighting department technology stacks and competencies.
- **Technical Knowledge Hub**: Published student and faculty engineering articles, categorized by tech domain (AI/ML, Cloud, CyberSec, Web3, Systems).
- **Live Circulars & Notice Board**: Real-time academic notices, placement drive alerts, exam timetables, and hackathon announcements.
- **Academic Calendar**: Monthly calendar interface with category filtering (Internal Assessments, University Exams, Symposia, Holidays).
- **Institutional Archive**: Downloadable PDF publication lists (Scopus/WoS indexed), laboratory infrastructure guides, placement track records (800+ placed), and SHIMMER alumni portal.

### 2. 🎓 Student Writing Portal
- **Student Registration & Auth**: Dedicated student accounts (`/student/register/` and `/student/login/`).
- **Student Dashboard (`/blogs/my/`)**: Personal workspace for authoring blogs with Rich Text (CKEditor).
- **Draft & Revision Control**: Save drafts, update content, and submit articles for review.
- **Review Status Tracking**: Real-time status indicators (**Draft** $\rightarrow$ **Pending** $\rightarrow$ **Approved** / **Rejected** $\rightarrow$ **Published**).
- **Faculty Feedback Viewer**: View detailed rejection feedback and improvement suggestions from faculty reviewers.

### 3. 🛡️ Faculty & Admin Panel
- **Role-Based Permissions**: Granular roles (`SuperAdmin`, `Admin`, `Editor`, `Faculty`).
- **Editorial Review System (`/admin/blog/review/`)**: One-click approve, reject (with mandatory reason), publish, and unpublish actions.
- **Department Infrastructure CRUD**: Manage Computing Laboratories, equipment specifications, and hardware inventories.
- **Placement Records CRUD**: Manage yearly placement metrics, top recruitments, and recruiter portfolios.
- **Instant News Broadcasts**: Dispatch one-click WebPush alerts to all active browser subscribers.

### 4. 🔔 Real-Time WebPush Notifications
- **VAPID Cryptography**: RFC 8292 standard public-key authenticated push notifications.
- **Root-Scoped Service Worker (`/sw.js`)**: Background notification handler with auto-focus and deep-linking on click.
- **Client Controller (`push-notifications.js`)**: Interactive permission prompt, subscription management, and auto-sync.
- **Asynchronous Delivery**: Celery worker handles multi-subscriber broadcast distribution with auto-pruning of expired endpoints (HTTP 410/404).

### 5. ⚡ FastAPI Microservice
- **High-Performance Read Endpoints**: Read blogs, news, events, and faculty directly via SQLAlchemy.
- **Interactive Documentation**: Auto-generated Swagger UI (`/api/v1/docs`) and ReDoc (`/api/v1/redoc`).
- **Shared PostgreSQL Model Alignment**: Seamlessly reads models managed by Django migrations.

---

## 📁 Project Directory Structure

```text
├── django_app/                     # Main Django Application
│   ├── apps/
│   │   ├── accounts/               # Auth, AdminUser, Student Roles, Permissions
│   │   ├── blog/                   # Blog Models, Review Workflow, Student Views
│   │   ├── contact/                # Contact Inquiries & Grievances
│   │   ├── core/                   # Home, Labs, Placements, Milestones, Search
│   │   ├── events/                 # Academic Calendar & Event Management
│   │   ├── faculty/                # Faculty Profiles & Designations
│   │   └── news/                   # Circulars, Push Subscriptions, Celery Tasks
│   ├── config/
│   │   ├── settings/               # Base, Local, Test, & Prod Django Settings
│   │   ├── urls.py                 # Root URL routing & Service Worker Mount
│   │   └── wsgi.py / asgi.py
│   ├── static/                     # CSS, JS, Images, Service Worker (sw.js)
│   └── templates/                  # Jinja2 / Django HTML Templates
│       ├── admin_panel/            # Admin Dashboard & Management Views
│       ├── public/                 # Public Facing Web Pages
│       └── student/                # Student Portal & Blog Dashboard
├── fastapi_app/                    # Read-Optimized FastAPI Microservice
│   ├── models/                     # SQLAlchemy Table Declarations
│   ├── routers/                    # API Endpoints (Blogs, News, Events, Faculty)
│   ├── schemas/                    # Pydantic Schemas for Validation & Serialization
│   └── main.py                     # FastAPI Application Factory
├── requirements/                   # Pip Dependency Manifests
│   ├── django.txt                  # Django, Celery, PyWebPush, PostgreSQL libs
│   └── fastapi.txt                 # FastAPI, Uvicorn, SQLAlchemy libs
├── docker-compose.yml              # Multi-container orchestration specification
├── Dockerfile.django               # Production Django Container Image
├── Dockerfile.fastapi              # Production FastAPI Container Image
├── pytest.ini                      # Pytest Configuration
└── .env.example                    # Environment variable template
```

---

## 🛠️ Prerequisites

Choose one of the following methods to run the stack:

| Requirement | Docker (Recommended) | Bare-Metal / Local |
| :--- | :--- | :--- |
| **Operating System** | Windows, Linux, or macOS | Windows, Linux, or macOS |
| **Container Engine** | Docker Engine & Docker Compose | N/A |
| **Python** | Bundled in Docker (3.12) | Python 3.12+ installed |
| **Database** | Bundled in Docker (PostgreSQL 16) | PostgreSQL 16 server running |
| **Message Broker** | Bundled in Docker (Redis 7) | Redis 7 server running |

---

## ⚙️ Environment Configuration

1. Create your local environment file by copying `.env.example`:
   ```bash
   cp .env.example .env
   ```

2. Fill in the required environment variables in `.env`:

| Variable | Description | Example / Default |
| :--- | :--- | :--- |
| `SECRET_KEY` | Django cryptographic secret key | *Random 64-char string* |
| `DEBUG` | Debug mode (`True` for dev, `False` for prod) | `True` |
| `ALLOWED_HOSTS` | Comma-separated allowed hostnames | `localhost,127.0.0.1` |
| `DB_NAME` | PostgreSQL database name | `cseblog_db` |
| `DB_USER` | PostgreSQL username | `cseblog_user` |
| `DB_PASSWORD` | PostgreSQL password | `your_secure_password` |
| `DB_HOST` | Database host (`postgres` for Docker, `localhost` for local) | `postgres` |
| `DB_PORT` | Database port | `5432` |
| `DATABASE_URL` | SQLAlchemy URL for FastAPI | `postgresql://user:pass@postgres:5432/db` |
| `REDIS_URL` | Redis broker and cache connection URI | `redis://redis:6379/0` |
| `VAPID_PUBLIC_KEY` | Public key for WebPush browser registration | *Base64 URL-safe key* |
| `VAPID_PRIVATE_KEY` | Private key for Celery push encryption | *Base64 URL-safe key* |
| `VAPID_ADMIN_EMAIL` | Contact email included in VAPID claims | `mailto:admin@valliammai.ac.in` |

### 🔑 Generating VAPID Keys for WebPush
If you need fresh VAPID keys, run:
```bash
python -c "from pywebpush import WebPusher; import json; from cryptography.hazmat.primitives.asymmetric import ec; from cryptography.hazmat.primitives import serialization; import base64; pk = ec.generate_private_key(ec.SECP256R1()); print('VAPID_PRIVATE_KEY=' + base64.urlsafe_b64encode(pk.private_numbers().private_value.to_bytes(32, 'big')).decode('utf-8').rstrip('=')); print('VAPID_PUBLIC_KEY=' + base64.urlsafe_b64encode(pk.public_key().public_bytes(serialization.Encoding.X962, serialization.PublicFormat.UncompressedPoint)).decode('utf-8').rstrip('='))"
```

---

## 🚀 Setup & Execution Guide

### Option A: Running with Docker (Recommended)

1. **Build and start all 5 containers** (Django, FastAPI, Celery, PostgreSQL, Redis):
   ```bash
   docker compose up --build -d
   ```

2. **Apply database schema migrations**:
   ```bash
   docker compose exec django python manage.py migrate
   ```

3. **Seed initial department data and academic calendar**:
   ```bash
   docker compose exec django python manage.py seed_department_data
   docker compose exec django python manage.py seed_academic_calendar
   docker compose exec django python manage.py seed_faculty_profiles
   ```

4. **Create the initial SuperAdmin account**:
   ```bash
   docker compose exec django python manage.py createsuperuser
   ```

5. **View live services**:
   - 🌐 **Public Website**: [http://localhost:8000/](http://localhost:8000/)
   - 🎓 **Student Portal**: [http://localhost:8000/student/login/](http://localhost:8000/student/login/)
   - 🛡️ **Admin Panel**: [http://localhost:8000/admin/login/](http://localhost:8000/admin/login/)
   - ⚡ **FastAPI Swagger Docs**: [http://localhost:8001/api/v1/docs](http://localhost:8001/api/v1/docs)

---

### Option B: Local / Bare-Metal Setup (Without Docker)

1. **Clone the repository and create a Python virtual environment**:
   ```bash
   git clone https://github.com/vedasm/CSE-Blog.git
   cd CSE-Blog
   python -m venv venv
   ```

2. **Activate the virtual environment**:
   - **Windows (PowerShell)**: `.\venv\Scripts\Activate.ps1`
   - **Linux / macOS**: `source venv/bin/activate`

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements/django.txt
   pip install -r requirements/fastapi.txt
   ```

4. **Configure your local PostgreSQL and Redis servers**, and ensure `.env` points to `localhost`:
   ```ini
   DB_HOST=localhost
   REDIS_URL=redis://localhost:6379/0
   ```

5. **Apply migrations and seed initial data**:
   ```bash
   cd django_app
   python manage.py migrate
   python manage.py seed_department_data
   python manage.py seed_academic_calendar
   python manage.py seed_faculty_profiles
   python manage.py createsuperuser
   ```

6. **Start the development servers**:
   - **Terminal 1 (Django Web)**:
     ```bash
     python manage.py runserver 0.0.0.0:8000
     ```
   - **Terminal 2 (Celery Worker)**:
     ```bash
     celery -A config worker -l info
     ```
   - **Terminal 3 (FastAPI Microservice)**:
     ```bash
     cd ../fastapi_app
     uvicorn main:app --host 0.0.0.0 --port 8001 --reload
     ```

---

## 🧪 Automated Testing

The project uses `pytest` and `pytest-django` for complete automated testing across all Django apps.

To run the entire test suite inside Docker:
```bash
docker compose exec django pytest
```

To run tests in a local virtual environment:
```bash
cd django_app
pytest
```

**Test Coverage Summary:**
- `accounts`: User roles, permissions (`StudentRequiredMixin`, `EditorRequiredMixin`), student registration, login, logout.
- `blog`: Article model, slugification, student blog submissions, review lifecycle, approval/rejection.
- `news`: WebPush subscription storage, VAPID key distribution, unsubscription, Celery push tasks.
- `events`: Academic calendar query filters, monthly view.
- `faculty`: Directory listings, profile links.
- `contact`: Inquiry submissions and validations.
- `core`: Public homepage, laboratory directory, placement metrics.

---

## 📌 Route & URL Reference

| Section | URL Path | Method | Description |
| :--- | :--- | :--- | :--- |
| **Home** | `/` | `GET` | Main public department landing page |
| **News** | `/news/` | `GET` | Public circulars and notice board |
| **Push API** | `/news/api/push/vapid-key/` | `GET` | Fetches VAPID public key for WebPush |
| **Push API** | `/news/api/push/subscribe/` | `POST` | Registers a browser push subscription |
| **Service Worker**| `/sw.js` | `GET` | Root-scoped WebPush service worker |
| **Student** | `/student/login/` | `GET, POST` | Student authentication portal |
| **Student** | `/student/register/` | `GET, POST` | Student account registration |
| **Student** | `/blogs/my/` | `GET` | Student blog dashboard & draft management |
| **Student** | `/blogs/create/` | `GET, POST` | Author new tech article |
| **Admin** | `/admin/login/` | `GET, POST` | Admin & Faculty login portal |
| **Admin** | `/admin/blog/review/` | `GET, POST` | Editorial blog review queue |
| **Admin** | `/admin/news/` | `GET` | Manage circulars and trigger instant push |
| **FastAPI** | `http://localhost:8001/api/v1/docs` | `GET` | Swagger OpenAPI documentation |

---

## 🔒 Production Deployment Checklist

Before deploying to production:
1. Set `DEBUG=False` in `.env`.
2. Generate unique, cryptographically strong `SECRET_KEY` and `JWT_SECRET_KEY`.
3. Set `SESSION_COOKIE_SECURE=True` and `CSRF_COOKIE_SECURE=True`.
4. Run `python manage.py collectstatic --noinput` to compile static assets.
5. Configure reverse proxy (Nginx or Caddy) with valid SSL/TLS certificates (Let's Encrypt).
6. Ensure PostgreSQL (port 5432) and Redis (port 6379) are not exposed directly to the public internet.

---

## 📄 License & Attribution

Developed for the **Department of Computer Science and Engineering**, **SRM Valliammai Engineering College**.  
All rights reserved.
