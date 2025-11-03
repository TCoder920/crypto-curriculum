# Scripts Directory

This directory contains all automation scripts, helper utilities, and operational tools. **All scripts should be placed here** unless they are component-specific build scripts.

## 📁 Purpose

Scripts in this directory automate:
- Project setup and initialization
- Development environment configuration
- Database operations
- Deployment procedures
- Testing automation
- Data migration
- Maintenance tasks

## 🔧 Recommended Scripts to Create

### Setup Scripts
- `setup-dev.sh` - Complete development environment setup
- `setup-frontend.sh` - Frontend-specific setup
- `setup-backend.sh` - Backend-specific setup
- `setup-db.sh` - Database initialization

### Database Scripts
- `init-db.sh` - Initialize database with schema
- `seed-db.sh` - Seed database with sample data
- `backup-db.sh` - Backup database
- `restore-db.sh` - Restore database from backup
- `reset-db.sh` - Reset database to clean state

### Deployment Scripts
- `deploy-dev.sh` - Deploy to development environment
- `deploy-staging.sh` - Deploy to staging
- `deploy-prod.sh` - Deploy to production
- `health-check.sh` - Check service health

### Maintenance Scripts
- `clean.sh` - Clean build artifacts and caches
- `update-deps.sh` - Update dependencies
- `run-tests.sh` - Run all tests
- `lint-all.sh` - Run all linters

## 📝 Script Guidelines

### Naming Conventions
- Use lowercase with hyphens: `setup-dev.sh`
- Use descriptive names: `seed-curriculum-data.sh`
- Add language extension: `.sh`, `.py`, `.js`

### File Structure
```bash
#!/bin/bash
# Script: setup-dev.sh
# Purpose: Set up development environment
# Usage: ./scripts/setup-dev.sh

set -e  # Exit on error

echo "Starting development setup..."

# Script logic here

echo "✅ Setup complete!"
```

### Best Practices

1. **Make scripts executable**
   ```bash
   chmod +x scripts/your-script.sh
   ```

2. **Add error handling**
   ```bash
   set -e  # Exit on error
   set -u  # Exit on undefined variable
   ```

3. **Add usage documentation**
   ```bash
   # Usage: ./scripts/deploy.sh [environment]
   # Example: ./scripts/deploy.sh production
   ```

4. **Use environment variables**
   ```bash
   DB_HOST=${DB_HOST:-localhost}
   DB_PORT=${DB_PORT:-5432}
   ```

5. **Add confirmation for destructive operations**
   ```bash
   read -p "This will delete the database. Continue? (y/n) " -n 1 -r
   if [[ ! $REPLY =~ ^[Yy]$ ]]; then exit 1; fi
   ```

## 🎯 Language Choice

| Task Type | Recommended Language | Why |
|-----------|---------------------|-----|
| **Setup & initialization** | Bash (.sh) | Simple, portable, system-level |
| **Database operations** | Python (.py) | SQLAlchemy integration, robust |
| **Data processing** | Python (.py) | Rich libraries, easy to maintain |
| **Build automation** | Bash or Node.js | Depends on ecosystem |
| **Git hooks** | Bash or Python | Fast execution, reliable |

## 📦 Example Scripts

### setup-dev.sh
```bash
#!/bin/bash
# Complete development environment setup

echo "🚀 Setting up development environment..."

# Frontend setup
cd app/frontend
npm install
cd ../..

# Backend setup  
cd app/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ../..

# Database setup
./scripts/init-db.sh

echo "✅ Development environment ready!"
```

### init-db.sh
```bash
#!/bin/bash
# Initialize database

echo "🗄️  Initializing database..."

# Create database if it doesn't exist
createdb crypto_curriculum 2>/dev/null || echo "Database already exists"

# Run migrations
cd app/backend
alembic upgrade head

echo "✅ Database initialized!"
```

## 🚫 What NOT to Put Here

- **Build scripts specific to components** → Keep in component directory (e.g., `app/frontend/package.json` scripts)
- **Application code** → Belongs in `app/`
- **Configuration files** → Belongs in component's config directory
- **Documentation** → Belongs in `docs/`

## 📖 Running Scripts

### From Project Root
```bash
./scripts/setup-dev.sh
```

### Make Script Executable
```bash
chmod +x scripts/setup-dev.sh
```

### With Arguments
```bash
./scripts/deploy.sh production
./scripts/seed-db.sh --sample-data
```

## 🧪 Database Seeding (`seed-db.py`)

### Prerequisites
- Python 3.11+
- Install dependencies inside your virtualenv:
  ```bash
  pip install sqlalchemy psycopg[binary]
  ```
- PostgreSQL instance accessible via `DATABASE_URL` (defaults to `postgresql+psycopg://postgres:postgres@localhost:5432/crypto_curriculum`)

### Usage
- Dry run (no database writes):
  ```bash
  python scripts/seed-db.py
  ```
- Seed database (truncate first and apply changes):
  ```bash
  DATABASE_URL=postgresql+psycopg://user:pass@localhost:5432/crypto_curriculum \
  python scripts/seed-db.py --reset --commit
  ```
- Additional flags:
  - `--reset` – Truncate tables before seeding (uses `CASCADE`)
  - `--commit` – Apply changes; omit for dry run previews
  - `--database-url` – Override connection string
  - `--verbose` – Enable debug logging for troubleshooting

### Data Coverage
- Imports modules and lessons directly from the curriculum markdown files
- Generates 170 assessment questions (10 per module) with mixed question types
- Seeds sample users (admin, instructors, students), cohorts, deadlines, announcements
- Populates progress, quiz attempts (auto and manual grading scenarios), notifications, chat transcripts, and leaderboards

### Cleanup & Resets
- Use `--reset` to clear existing seed data before generating a fresh dataset
- For production environments, run without `--reset` and target only new datasets as needed
- Review generated data via `SELECT COUNT(*)` checks after the script runs


---

**Remember:** Scripts should be reusable, well-documented, and safe to run. Always test scripts in a safe environment before using them in production.
