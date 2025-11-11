"""Script to create database tables directly"""
import asyncio
import sys
import os

# Add project root to path
_backend_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(os.path.dirname(_backend_dir))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from app.backend.core.database import init_db, close_db
from app.backend.models import *  # Import all models to register them


async def main():
    """Create all database tables"""
    print("Creating database tables...")
    await init_db()
    print("Database tables created successfully!")
    await close_db()


if __name__ == "__main__":
    asyncio.run(main())


