"""Tests for grading endpoints"""
import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.backend.main import app
from app.backend.models.assessment import Assessment, QuestionType
from app.backend.models.progress import QuizAttempt, ReviewStatus
from app.backend.models.module import Module
from app.backend.core.database import get_db
from app.backend.tests.conftest import override_get_db


@pytest.mark.asyncio
async def test_get_grading_queue(
    async_client: AsyncClient,
    test_quiz_attempt_pending,
    test_short_answer_assessment,
    test_module,
    override_get_db,
    test_instructor_token,
):
    """Test getting grading queue"""
    app.dependency_overrides[get_db] = override_get_db
    
    response = await async_client.get(
        "/api/v1/grading/queue",
        headers={"Authorization": f"Bearer {test_instructor_token}"},
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert len(data["items"]) >= 1
    
    # Find our test attempt
    item = next(
        (i for i in data["items"] if i["attempt_id"] == test_quiz_attempt_pending.id),
        None
    )
    assert item is not None
    assert item["user_answer"] == test_quiz_attempt_pending.user_answer
    assert item["question_type"] == QuestionType.SHORT_ANSWER.value
    
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_grading_queue_student_forbidden(
    async_client: AsyncClient,
    override_get_db,
    test_token,
):
    """Test that students cannot access grading queue"""
    app.dependency_overrides[get_db] = override_get_db
    
    response = await async_client.get(
        "/api/v1/grading/queue",
        headers={"Authorization": f"Bearer {test_token}"},
    )
    
    assert response.status_code == 403
    
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_grading_queue_empty(
    async_client: AsyncClient,
    override_get_db,
    test_instructor_token,
    db_session: AsyncSession,
):
    """Test getting empty grading queue"""
    app.dependency_overrides[get_db] = override_get_db
    
    # Ensure no pending attempts exist
    # (This test assumes a clean database state)
    
    response = await async_client.get(
        "/api/v1/grading/queue",
        headers={"Authorization": f"Bearer {test_instructor_token}"},
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert len(data["items"]) == 0
    
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_grade_attempt(
    async_client: AsyncClient,
    test_quiz_attempt_pending,
    override_get_db,
    test_instructor_token,
    test_instructor,
):
    """Test grading an attempt"""
    app.dependency_overrides[get_db] = override_get_db
    
    response = await async_client.post(
        f"/api/v1/grading/{test_quiz_attempt_pending.id}",
        headers={"Authorization": f"Bearer {test_instructor_token}"},
        json={
            "is_correct": True,
            "points_earned": 8,
            "feedback": "Good answer, but could be more detailed.",
            "partial_credit": True,
        },
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_quiz_attempt_pending.id
    assert data["is_correct"] is True
    assert data["points_earned"] == 8
    assert data["review_status"] == ReviewStatus.GRADED.value
    assert data["graded_by"] == test_instructor.id
    assert data["feedback"] == "Good answer, but could be more detailed."
    assert data["partial_credit"] is True
    assert data["graded_at"] is not None
    
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_grade_attempt_full_credit(
    async_client: AsyncClient,
    test_quiz_attempt_pending,
    test_short_answer_assessment,
    override_get_db,
    test_instructor_token,
):
    """Test grading an attempt with full credit"""
    app.dependency_overrides[get_db] = override_get_db
    
    response = await async_client.post(
        f"/api/v1/grading/{test_quiz_attempt_pending.id}",
        headers={"Authorization": f"Bearer {test_instructor_token}"},
        json={
            "is_correct": True,
            "points_earned": test_short_answer_assessment.points,
            "feedback": "Excellent answer!",
            "partial_credit": False,
        },
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["is_correct"] is True
    assert data["points_earned"] == test_short_answer_assessment.points
    assert data["partial_credit"] is False
    
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_grade_attempt_incorrect(
    async_client: AsyncClient,
    test_quiz_attempt_pending,
    override_get_db,
    test_instructor_token,
):
    """Test grading an attempt as incorrect"""
    app.dependency_overrides[get_db] = override_get_db
    
    response = await async_client.post(
        f"/api/v1/grading/{test_quiz_attempt_pending.id}",
        headers={"Authorization": f"Bearer {test_instructor_token}"},
        json={
            "is_correct": False,
            "points_earned": 0,
            "feedback": "This answer is incorrect. Please review the material.",
            "partial_credit": False,
        },
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["is_correct"] is False
    assert data["points_earned"] == 0
    
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_grade_attempt_not_found(
    async_client: AsyncClient,
    override_get_db,
    test_instructor_token,
):
    """Test grading a non-existent attempt"""
    app.dependency_overrides[get_db] = override_get_db
    
    response = await async_client.post(
        "/api/v1/grading/999",
        headers={"Authorization": f"Bearer {test_instructor_token}"},
        json={
            "is_correct": True,
            "points_earned": 10,
        },
    )
    
    assert response.status_code == 404
    
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_grade_auto_graded_question_forbidden(
    async_client: AsyncClient,
    test_user,
    test_module,
    override_get_db,
    test_instructor_token,
    db_session: AsyncSession,
):
    """Test that auto-graded questions cannot be manually graded"""
    app.dependency_overrides[get_db] = override_get_db
    
    # Create a multiple-choice assessment
    mc_assessment = Assessment(
        module_id=test_module.id,
        question_text="Multiple choice question",
        question_type=QuestionType.MULTIPLE_CHOICE,
        order_index=1,
        points=10,
        options={"A": "Option A", "B": "Option B"},
        correct_answer="B",
        is_active=True,
    )
    db_session.add(mc_assessment)
    await db_session.commit()
    await db_session.refresh(mc_assessment)
    
    # Create an attempt (auto-graded)
    attempt = QuizAttempt(
        user_id=test_user.id,
        assessment_id=mc_assessment.id,
        user_answer="B",
        is_correct=True,
        points_earned=10,
        review_status=ReviewStatus.GRADED,
    )
    db_session.add(attempt)
    await db_session.commit()
    await db_session.refresh(attempt)
    
    # Try to grade it manually
    response = await async_client.post(
        f"/api/v1/grading/{attempt.id}",
        headers={"Authorization": f"Bearer {test_instructor_token}"},
        json={
            "is_correct": True,
            "points_earned": 10,
        },
    )
    
    assert response.status_code == 400
    assert "auto-graded" in response.json()["detail"].lower()
    
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_grade_already_graded_attempt(
    async_client: AsyncClient,
    test_quiz_attempt_pending,
    test_instructor,
    override_get_db,
    test_instructor_token,
    db_session: AsyncSession,
):
    """Test that already graded attempts cannot be re-graded"""
    app.dependency_overrides[get_db] = override_get_db
    
    # Grade the attempt first
    test_quiz_attempt_pending.is_correct = True
    test_quiz_attempt_pending.points_earned = 10
    test_quiz_attempt_pending.review_status = ReviewStatus.GRADED
    test_quiz_attempt_pending.graded_by = test_instructor.id
    test_quiz_attempt_pending.graded_at = datetime.now()
    await db_session.commit()
    
    # Try to grade again
    response = await async_client.post(
        f"/api/v1/grading/{test_quiz_attempt_pending.id}",
        headers={"Authorization": f"Bearer {test_instructor_token}"},
        json={
            "is_correct": True,
            "points_earned": 10,
        },
    )
    
    assert response.status_code == 400
    assert "already been graded" in response.json()["detail"].lower()
    
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_grading_history(
    async_client: AsyncClient,
    test_quiz_attempt_pending,
    test_instructor,
    override_get_db,
    test_instructor_token,
    db_session: AsyncSession,
):
    """Test getting grading history"""
    app.dependency_overrides[get_db] = override_get_db
    
    # Grade the attempt first
    test_quiz_attempt_pending.is_correct = True
    test_quiz_attempt_pending.points_earned = 8
    test_quiz_attempt_pending.review_status = ReviewStatus.GRADED
    test_quiz_attempt_pending.graded_by = test_instructor.id
    test_quiz_attempt_pending.graded_at = datetime.now()
    await db_session.commit()
    
    response = await async_client.get(
        "/api/v1/grading/history",
        headers={"Authorization": f"Bearer {test_instructor_token}"},
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    
    # Find our graded attempt
    item = next(
        (i for i in data["items"] if i["id"] == test_quiz_attempt_pending.id),
        None
    )
    assert item is not None
    assert item["review_status"] == ReviewStatus.GRADED.value
    assert item["graded_by"] == test_instructor.id
    
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_grading_history_filtered_by_user(
    async_client: AsyncClient,
    test_quiz_attempt_pending,
    test_user,
    test_instructor,
    override_get_db,
    test_instructor_token,
    db_session: AsyncSession,
):
    """Test getting grading history filtered by user"""
    app.dependency_overrides[get_db] = override_get_db
    
    # Grade the attempt
    test_quiz_attempt_pending.is_correct = True
    test_quiz_attempt_pending.points_earned = 8
    test_quiz_attempt_pending.review_status = ReviewStatus.GRADED
    test_quiz_attempt_pending.graded_by = test_instructor.id
    test_quiz_attempt_pending.graded_at = datetime.now()
    await db_session.commit()
    
    response = await async_client.get(
        f"/api/v1/grading/history?user_id={test_user.id}",
        headers={"Authorization": f"Bearer {test_instructor_token}"},
    )
    
    assert response.status_code == 200
    data = response.json()
    # Should include our test attempt
    assert any(i["user_id"] == test_user.id for i in data["items"])
    
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_grading_history_student_forbidden(
    async_client: AsyncClient,
    override_get_db,
    test_token,
):
    """Test that students cannot access grading history"""
    app.dependency_overrides[get_db] = override_get_db
    
    response = await async_client.get(
        "/api/v1/grading/history",
        headers={"Authorization": f"Bearer {test_token}"},
    )
    
    assert response.status_code == 403
    
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_unauthorized_grading_access(
    async_client: AsyncClient,
    test_quiz_attempt_pending,
):
    """Test that unauthenticated requests are rejected"""
    response = await async_client.get(
        "/api/v1/grading/queue",
    )
    
    assert response.status_code == 401

