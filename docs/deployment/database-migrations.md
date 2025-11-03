# Database Migrations

This guide documents how to manage PostgreSQL schema changes with Alembic for the Crypto Curriculum Platform.

## Alembic Setup
- Install dependencies: `pip install alembic psycopg[binary]`
- Initialize Alembic in the backend application directory: `alembic init alembic`
- Update `alembic.ini` with your database URL (use environment variables for local vs production)
- Configure `env.py` to import your SQLAlchemy `metadata` object
- Commit the generated Alembic scaffolding to version control

## Migration Workflow
1. Verify that models reflect the desired schema changes
2. Create a new migration revision:
   ```bash
   alembic revision --autogenerate -m "short description"
   ```
3. Review the generated migration for accuracy, paying attention to:
   - Correct table/column names
   - Appropriate constraints and indexes
   - Safe defaults for new non-nullable columns
4. Apply the migration locally: `alembic upgrade head`
5. Run automated tests or smoke tests to validate the change
6. Share the migration with the team via pull request
7. Apply to staging/production environments once approved

## Generating the Initial Migration
- Ensure all SQLAlchemy models are defined
- Run `alembic revision --autogenerate -m "Initial schema"`
- Inspect the migration to confirm all tables (16 core tables) are created
- Apply locally with `alembic upgrade head` and verify the schema against documentation

## Best Practices
- Use descriptive migration messages (e.g., `"add notifications table"`)
- Prefer additive changes; avoid dropping columns without backups
- Keep migration logic idempotent and forward-compatible
- For data migrations, encapsulate SQL in helper functions and include `downgrade` logic
- Test downgrade paths (`alembic downgrade -1`) when feasible
- Keep migrations in chronological order and avoid editing previous revisions once merged

**Last Updated:** 2025-02-15

