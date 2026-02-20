# Telegram Bot SaaS Starter

Production-minded MVP starter for building a multi-tenant Telegram bot SaaS.

## What is included
- FastAPI backend with modular route layout
- JWT auth (register/login/me)
- Tenant and bot management endpoints
- Telegram webhook ingestion endpoint with secret validation
- Billing-ready schema (`plans`, `subscriptions`)
- Admin overview metrics endpoint
- PostgreSQL + Redis support
- Docker + Docker Compose for local environments
- Pytest API tests

## Architecture
- `src/app/main.py`: app entrypoint + startup initialization
- `src/app/core/`: settings and auth security helpers
- `src/app/db/`: SQLAlchemy engine/session + DB initializer
- `src/app/models/`: ORM models for users, tenants, bots, billing, updates
- `src/app/api/routes/`: route modules by domain
- `src/app/schemas/`: request/response models
- `tests/`: API integration tests

## API surface (MVP)
- `GET /api/v1/health`
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- `POST /api/v1/tenants`
- `GET /api/v1/tenants`
- `POST /api/v1/bots`
- `GET /api/v1/bots`
- `POST /api/v1/telegram/{bot_token}/webhook`
- `GET /api/v1/admin/overview` (superuser only)

## Quick start (local Python)
```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload --app-dir src
```

Open docs: `http://localhost:8000/docs`

## Quick start (Docker)
```bash
Copy-Item .env.example .env
docker compose up --build
```

## Test
```bash
pytest -q
```

## Roadmap to portfolio-grade v1
- Add Alembic migrations
- Add payment provider integration (Stripe/LemonSqueezy)
- Add background jobs (Celery/RQ) for bot events
- Add tenant role-based access control
- Add CI workflow with lint + tests + image build