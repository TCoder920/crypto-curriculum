"""Pytest configuration and fixtures"""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from app.backend.core.database import Base, get_db
from app.backend.main import app
from app.backend.models.user import User, UserRole
from app.backend.models.module import Module, Track
from app.backend.models.assessment import Assessment, QuestionType
from app.backend.core.security import create_access_token

# Use in-memory SQLite for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture
async def db_session():
    """Create a test database session"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with TestingSessionLocal() as session:
        yield session
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def test_user(db_session: AsyncSession):
    """Create a test user"""
    user = User(
        email="test@example.com",
        hashed_password="hashed_password",
        username="testuser",
        full_name="Test User",
        role=UserRole.STUDENT,
        is_active=True,
        is_verified=True,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
async def test_module(db_session: AsyncSession):
    """Create a test module"""
    module = Module(
        id=1,
        title="Test Module",
        description="Test description",
        track=Track.USER,
        order_index=1,
        duration_hours=2.0,
        is_active=True,
        is_published=True,
    )
    db_session.add(module)
    await db_session.commit()
    await db_session.refresh(module)
    return module


@pytest.fixture
async def test_assessment(db_session: AsyncSession, test_module: Module):
    """Create a test assessment"""
    assessment = Assessment(
        module_id=test_module.id,
        question_text="What is a test question?",
        question_type=QuestionType.MULTIPLE_CHOICE,
        order_index=1,
        points=10,
        options={"A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"},
        correct_answer="B",
        explanation="Test explanation",
        is_active=True,
    )
    db_session.add(assessment)
    await db_session.commit()
    await db_session.refresh(assessment)
    return assessment


@pytest.fixture
def test_token(test_user: User):
    """Create a test JWT token"""
    return create_access_token(data={"sub": str(test_user.id)})


@pytest.fixture
def override_get_db(db_session: AsyncSession):
    """Override get_db dependency"""
    async def _get_db():
        yield db_session
    return _get_db


@pytest.fixture
async def async_client():
    """Create an async HTTP client for testing"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

