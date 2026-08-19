# SRM Valliammai CSE Blog

Secure Django admin and server-rendered site, paired with a read-oriented FastAPI public API. Django owns schema migrations and management writes; FastAPI shares PostgreSQL for public reads, API contact submissions, and integration tokens.

```
Browser ── Nginx ── Django :8000 ── PostgreSQL 16
             └── FastAPI :8001 ────────┘
Django/Celery ── Redis 7 ── SMTP
```

## Setup

### 1. Configuration
Copy `.env.example` to `.env` and replace every placeholder secret/password.

### 2. Running with Docker (Recommended)
1. Start the stack: `docker compose up --build`.
2. In a second terminal, create the schema: 
   `docker compose exec django python manage.py migrate`.
3. Create the first administrator: 
   `docker compose exec django python manage.py createsuperuser`.

### 3. Local Development (Non-Docker)
If you prefer running the project without Docker (e.g., for easier debugging):
1. **Create a virtual environment**:
   `python -m venv venv`
2. **Activate the environment**:
   - Windows: `.\venv\Scripts\activate`
   - Unix/macOS: `source venv/bin/activate`
3. **Install dependencies**:
   `pip install -r requirements/django.txt`
4. **Apply migrations**:
   `cd django_app && python manage.py migrate`
5. **Run the server**:
   `python manage.py runserver`

Open the site at `http://localhost:8000/`, admin login at `http://localhost:8000/admin/login/`, and API docs at `http://localhost:8001/api/v1/docs`.

## Tests

The project uses `pytest` for testing. To run the test suite:
1. Ensure you are in the virtual environment.
2. Run: `pytest`

The test settings use an isolated database; deployed environments use PostgreSQL from `.env`.

## Production notes

Set `DEBUG=False`, secure cookie values to `True`, configure HTTPS in Nginx, and run `collectstatic` and `migrate` before serving. Do not expose PostgreSQL or Redis publicly.
