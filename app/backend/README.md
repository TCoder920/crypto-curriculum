# Crypto Curriculum Platform - Backend

FastAPI backend for the Learning Management System.

## Setup Instructions

### 1. Prerequisites
- Python 3.11+
- PostgreSQL 15+ (or Docker)
- pip

### 2. Environment Setup

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy environment template:
```bash
cp ../../docs/templates/backend.env.example .env
```

4. Edit `.env` with your database credentials:
```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/crypto_curriculum
SECRET_KEY=<generate-a-secure-secret-key>
```

### 3. Database Setup

1. Create the database:
```bash
createdb crypto_curriculum
# Or using PostgreSQL client:
# psql -U postgres -c "CREATE DATABASE crypto_curriculum;"
```

2. Run migrations:
```bash
alembic upgrade head
```

3. (Optional) Seed initial data:
```bash
python ../../scripts/seed-db.py --reset --commit
```

### 4. Run the Server

```bash
python main.py
```

The API will be available at:
- API: http://localhost:9000
- API Docs: http://localhost:9000/docs
- ReDoc: http://localhost:9000/redoc

## Project Structure

```
app/backend/
├── api/              # API routes
│   └── v1/
│       └── endpoints/
├── core/             # Core configuration
│   ├── config.py     # Settings
│   ├── database.py   # Database connection
│   └── security.py   # Auth utilities
├── models/           # SQLAlchemy models
├── schemas/           # Pydantic schemas
├── services/          # Business logic
├── alembic/           # Database migrations
├── main.py            # FastAPI app entry
└── requirements.txt   # Dependencies
```

## Database Models

16 core tables:
- Users, Modules, Lessons, Assessments
- UserProgress, QuizAttempts
- Cohorts, CohortMembers, CohortDeadlines
- Announcements, ForumPosts, ForumVotes
- Achievements, UserAchievements, Leaderboards
- Notifications, ChatMessages, LearningResources

## Development

### Create a Migration

```bash
alembic revision --autogenerate -m "description of changes"
alembic upgrade head
```

### Run Tests

```bash
pytest
```

## Environment Variables

See `docs/templates/backend.env.example` for all available environment variables.


