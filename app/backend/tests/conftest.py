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
from app.backend.models.cohort import Cohort, CohortMember, CohortRole
from app.backend.models.progress import QuizAttempt, ReviewStatus
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
async def test_token(test_user: User):
    """Create a test JWT token"""
    # test_user is async, but pytest-asyncio will await it
    return create_access_token(data={"sub": str(test_user.id)})


@pytest.fixture
def override_get_db(db_session: AsyncSession):
    """Override get_db dependency"""
    async def _get_db():
        yield db_session
    return _get_db


@pytest.fixture
async def test_instructor(db_session: AsyncSession):
    """Create a test instructor user"""
    instructor = User(
        email="instructor@example.com",
        hashed_password="hashed_password",
        username="instructor",
        full_name="Test Instructor",
        role=UserRole.INSTRUCTOR,
        is_active=True,
        is_verified=True,
    )
    db_session.add(instructor)
    await db_session.commit()
    await db_session.refresh(instructor)
    return instructor


@pytest.fixture
async def test_instructor_token(test_instructor: User):
    """Create a test JWT token for instructor"""
    # test_instructor is async, but pytest-asyncio will await it
    return create_access_token(data={"sub": str(test_instructor.id)})


@pytest.fixture
async def test_cohort(db_session: AsyncSession, test_instructor: User):
    """Create a test cohort"""
    cohort = Cohort(
        name="Test Cohort",
        description="Test cohort description",
        is_active=True,
        created_by=test_instructor.id,
    )
    db_session.add(cohort)
    await db_session.commit()
    await db_session.refresh(cohort)
    
    # Add instructor as member
    member = CohortMember(
        cohort_id=cohort.id,
        user_id=test_instructor.id,
        role=CohortRole.INSTRUCTOR.value,
    )
    db_session.add(member)
    await db_session.commit()
    
    return cohort


@pytest.fixture
async def test_short_answer_assessment(db_session: AsyncSession, test_module: Module):
    """Create a short answer assessment for grading tests"""
    assessment = Assessment(
        module_id=test_module.id,
        question_text="Explain a concept in detail",
        question_type=QuestionType.SHORT_ANSWER,
        order_index=10,
        points=10,
        correct_answer="Expected answer",
        explanation="Instructor will review",
        is_active=True,
    )
    db_session.add(assessment)
    await db_session.commit()
    await db_session.refresh(assessment)
    return assessment


@pytest.fixture
async def test_quiz_attempt_pending(
    db_session: AsyncSession,
    test_user: User,
    test_short_answer_assessment: Assessment,
):
    """Create a quiz attempt that needs grading"""
    attempt = QuizAttempt(
        user_id=test_user.id,
        assessment_id=test_short_answer_assessment.id,
        user_answer="This is my detailed answer",
        is_correct=None,
        points_earned=None,
        review_status=ReviewStatus.NEEDS_REVIEW,
    )
    db_session.add(attempt)
    await db_session.commit()
    await db_session.refresh(attempt)
    return attempt


@pytest.fixture
async def async_client():
    """Create an async HTTP client for testing"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

