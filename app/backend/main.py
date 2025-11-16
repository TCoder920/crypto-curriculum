"""FastAPI application entry point"""
import sys
import os

# Add project root to path for proper module resolution when running via python main.py
# This allows imports like 'app.backend.core.config' to work
_backend_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.dirname(os.path.dirname(_backend_dir))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

from app.backend.core.config import settings
from app.backend.core.database import init_db, close_db

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting up Crypto Curriculum Platform...")
    # Note: Database tables should be created via Alembic migrations
    # await init_db()  # Only use if not using Alembic
    yield
    # Shutdown
    logger.info("Shutting down...")
    await close_db()


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Learning Management System for cryptocurrency and blockchain education",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=["*"],
    allow_headers=["*", "Authorization", "Content-Type"],
    expose_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint"""
    return JSONResponse(
        content={
            "message": "Crypto Curriculum Platform API",
            "version": "1.0.0",
            "status": "running"
        }
    )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse(
        content={
            "status": "healthy",
            "environment": settings.ENVIRONMENT
        }
    )


# Import and include routers
from app.backend.api.v1.endpoints import auth, assessment, module, cohort, grading, forum, notification, ai_assistant, achievement, analytics, learning_resource

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(assessment.router, prefix="/api/v1", tags=["assessments"])
app.include_router(module.router, prefix="/api/v1", tags=["modules"])
app.include_router(cohort.router, prefix="/api/v1", tags=["cohorts"])
app.include_router(grading.router, prefix="/api/v1", tags=["grading"])
app.include_router(forum.router, prefix="/api/v1", tags=["forums"])
app.include_router(notification.router, prefix="/api/v1", tags=["notifications"])
app.include_router(ai_assistant.router, prefix="/api/v1", tags=["ai-assistant"])
app.include_router(achievement.router, prefix="/api/v1", tags=["achievements"])
app.include_router(analytics.router, prefix="/api/v1", tags=["analytics"])
app.include_router(learning_resource.router, prefix="/api/v1", tags=["learning-resources"])


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.backend.main:app",
        host="0.0.0.0",  # Bind to all interfaces (works with both 127.0.0.1 and localhost)
        port=9000,  # Using port 9000 to avoid conflicts with other services
        reload=settings.DEBUG,
    )

