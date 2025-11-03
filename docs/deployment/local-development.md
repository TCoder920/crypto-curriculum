# Local Development Guide

Phase 2 focuses on delivering a complete LMS experience running locally. Use this checklist to configure and validate the development environment before tackling cloud deployment in Phase 3.

## 1. Prerequisites
- macOS or Linux (Windows with WSL2 works as well)
- Homebrew or equivalent package manager
- Node.js 18+ and npm or yarn
- Python 3.11+
- PostgreSQL 15+ (native install or Docker)
- Git

## 2. Environment Setup
1. Clone the repository and checkout `development`.
2. Copy environment templates:
   ```bash
   cp docs/templates/frontend.env.example app/frontend/.env.local
   cp docs/templates/backend.env.example app/backend/.env
   ```
3. Update local URLs and credentials in the copied files:
   - `VITE_API_URL=http://localhost:8000`
   - `DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/crypto_curriculum`
   - Generate a local `JWT_SECRET_KEY`.
4. (Optional) Create a Python virtual environment in `app/backend`: `python -m venv venv`.

## 3. Database Workflow
1. Start PostgreSQL locally or with Docker:
   ```bash
   docker run --name crypto-postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:15
   ```
2. Apply migrations:
   ```bash
   cd app/backend
   source venv/bin/activate  # if using venv
   alembic upgrade head
   ```
3. Seed sample data (dry run first):
   ```bash
   python scripts/seed-db.py --verbose
   python scripts/seed-db.py --reset --commit
   ```
4. Verify data with `psql` or your preferred client.

## 4. Backend
1. Install dependencies:
   ```bash
   cd app/backend
   pip install -r requirements.txt
   ```
2. Run the API:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
3. Confirm health at `http://localhost:8000/docs`.

## 5. Frontend
1. Install dependencies:
   ```bash
   cd app/frontend
   npm install
   ```
2. Start the dev server:
   ```bash
   npm run dev -- --host
   ```
3. Visit `http://localhost:5173` and confirm the UI connects to the local API.

## 6. Local QA
- Run backend tests: `pytest`
- Run frontend lint/tests (if configured) e.g., `npm run lint`
- Execute a smoke test:
  - Login/register via API
  - Browse modules/lessons
  - Submit assessments
  - Inspect notifications and grading queues

## 7. Optional Docker Compose
- Create a `docker-compose.yml` to orchestrate API, frontend, Postgres, and MailHog locally.
- Ensure environment variables mirror `.env` files.

## 8. Preparing for Phase 3
- Document any local overrides needed during development.
- Capture issues to address before cloud deployment (performance, migrations, data volumes).
- When Phase 2 milestones are complete, follow the [Google Cloud Setup Guide](docs/deployment/google-cloud-setup.md) to promote the application.

**Last Updated:** 2025-02-15

