"""Tests for assessment endpoints"""
import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.main import app
from app.backend.models.assessment import Assessment, QuestionType
from app.backend.models.progress import QuizAttempt, ReviewStatus
from app.backend.core.database import get_db
from app.backend.tests.conftest import override_get_db


@pytest.mark.asyncio
async def test_get_module_assessments(
    async_client: AsyncClient,
    test_user,
    test_module,
    test_assessment,
    override_get_db,
    test_token,
):
    """Test getting assessments for a module"""
    app.dependency_overrides[get_db] = override_get_db
    
    response = await async_client.get(
        f"/api/v1/modules/{test_module.id}/assessments",
        headers={"Authorization": f"Bearer {test_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["module_id"] == test_module.id
    assert len(data["assessments"]) == 1
    assert data["assessments"][0]["id"] == test_assessment.id
    assert data["assessments"][0]["question_text"] == test_assessment.question_text
    # Should not expose correct_answer
    assert "correct_answer" not in data["assessments"][0]
    
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_submit_multiple_choice_correct(
    async_client: AsyncClient,
    test_user,
    test_module,
    test_assessment,
    override_get_db,
    test_token,
):
    """Test submitting a correct multiple choice answer"""
    app.dependency_overrides[get_db] = override_get_db
    
    response = await async_client.post(
        f"/api/v1/assessments/{test_assessment.id}/submit",
        headers={"Authorization": f"Bearer {test_token}"},
        json={"user_answer": "B", "time_spent_seconds": 30}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["is_correct"] is True
    assert data["points_earned"] == 10
    assert data["review_status"] == "graded"
    assert data["correct_answer"] == "B"
    assert "explanation" in data
    
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_submit_multiple_choice_incorrect(
    async_client: AsyncClient,
    test_user,
    test_module,
    test_assessment,
    override_get_db,
    test_token,
):
    """Test submitting an incorrect multiple choice answer"""
    app.dependency_overrides[get_db] = override_get_db
    
    response = await async_client.post(
        f"/api/v1/assessments/{test_assessment.id}/submit",
        headers={"Authorization": f"Bearer {test_token}"},
        json={"user_answer": "A", "time_spent_seconds": 30}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["is_correct"] is False
    assert data["points_earned"] == 0
    assert data["review_status"] == "graded"
    assert data["correct_answer"] == "B"
    
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_submit_true_false(
    async_client: AsyncClient,
    test_user,
    test_module,
    override_get_db,
    test_token,
    db_session: AsyncSession,
):
    """Test submitting a true/false answer"""
    app.dependency_overrides[get_db] = override_get_db
    
    # Create a true/false assessment
    tf_assessment = Assessment(
        module_id=test_module.id,
        question_text="True or False: Test statement",
        question_type=QuestionType.TRUE_FALSE,
        order_index=2,
        points=10,
        correct_answer="True",
        explanation="Test explanation",
        is_active=True,
    )
    db_session.add(tf_assessment)
    await db_session.commit()
    await db_session.refresh(tf_assessment)
    
    response = await async_client.post(
        f"/api/v1/assessments/{tf_assessment.id}/submit",
        headers={"Authorization": f"Bearer {test_token}"},
        json={"user_answer": "True", "time_spent_seconds": 15}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["is_correct"] is True
    assert data["review_status"] == "graded"
    
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_submit_short_answer(
    async_client: AsyncClient,
    test_user,
    test_module,
    override_get_db,
    test_token,
    db_session: AsyncSession,
):
    """Test submitting a short answer (should be pending review)"""
    app.dependency_overrides[get_db] = override_get_db
    
    # Create a short answer assessment
    sa_assessment = Assessment(
        module_id=test_module.id,
        question_text="Explain a concept",
        question_type=QuestionType.SHORT_ANSWER,
        order_index=3,
        points=10,
        correct_answer="",
        explanation="Instructor will review",
        is_active=True,
    )
    db_session.add(sa_assessment)
    await db_session.commit()
    await db_session.refresh(sa_assessment)
    
    response = await async_client.post(
        f"/api/v1/assessments/{sa_assessment.id}/submit",
        headers={"Authorization": f"Bearer {test_token}"},
        json={"user_answer": "This is my answer", "time_spent_seconds": 60}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["is_correct"] is None  # Not graded yet
    assert data["points_earned"] is None
    assert data["review_status"] == "needs_review"
    
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_module_results(
    async_client: AsyncClient,
    test_user,
    test_module,
    test_assessment,
    override_get_db,
    test_token,
    db_session: AsyncSession,
):
    """Test getting module results"""
    app.dependency_overrides[get_db] = override_get_db
    
    # Create a quiz attempt
    attempt = QuizAttempt(
        user_id=test_user.id,
        assessment_id=test_assessment.id,
        user_answer="B",
        is_correct=True,
        points_earned=10,
        review_status=ReviewStatus.GRADED,
    )
    db_session.add(attempt)
    await db_session.commit()
    
    response = await async_client.get(
        f"/api/v1/assessments/results/{test_module.id}",
        headers={"Authorization": f"Bearer {test_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["module_id"] == test_module.id
    assert data["total_questions"] == 1
    assert data["attempted"] == 1
    assert data["correct"] == 1
    assert data["score_percent"] == 100.0
    assert data["points_earned"] == 10
    assert data["points_possible"] == 10
    assert data["can_progress"] is True  # 100% score >= 70%
    assert len(data["attempts"]) == 1
    
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_progression_blocking_low_score(
    async_client: AsyncClient,
    test_user,
    test_module,
    override_get_db,
    test_token,
    db_session: AsyncSession,
):
    """Test that progression is blocked when score < 70%"""
    app.dependency_overrides[get_db] = override_get_db
    
    # Create 10 assessments (100 points total)
    assessments = []
    for i in range(10):
        assessment = Assessment(
            module_id=test_module.id,
            question_text=f"Question {i+1}",
            question_type=QuestionType.MULTIPLE_CHOICE,
            order_index=i+1,
            points=10,
            options={"A": "Option A", "B": "Option B"},
            correct_answer="B",
            is_active=True,
        )
        db_session.add(assessment)
        assessments.append(assessment)
    await db_session.commit()
    
    # Create attempts with 60% score (6 correct out of 10)
    for i, assessment in enumerate(assessments):
        attempt = QuizAttempt(
            user_id=test_user.id,
            assessment_id=assessment.id,
            user_answer="B" if i < 6 else "A",  # First 6 correct, last 4 wrong
            is_correct=(i < 6),
            points_earned=10 if i < 6 else 0,
            review_status=ReviewStatus.GRADED,
        )
        db_session.add(attempt)
    await db_session.commit()
    
    response = await async_client.get(
        f"/api/v1/assessments/results/{test_module.id}",
        headers={"Authorization": f"Bearer {test_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["score_percent"] == 60.0
    assert data["can_progress"] is False  # 60% < 70%
    
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_unauthorized_access(
    async_client: AsyncClient,
    test_module,
):
    """Test that unauthenticated requests are rejected"""
    response = await async_client.get(
        f"/api/v1/modules/{test_module.id}/assessments"
    )
    
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_nonexistent_module(
    async_client: AsyncClient,
    test_token,
):
    """Test requesting assessments for non-existent module"""
    response = await async_client.get(
        "/api/v1/modules/999/assessments",
        headers={"Authorization": f"Bearer {test_token}"}
    )
    
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_nonexistent_assessment(
    async_client: AsyncClient,
    test_token,
):
    """Test submitting answer to non-existent assessment"""
    response = await async_client.post(
        "/api/v1/assessments/999/submit",
        headers={"Authorization": f"Bearer {test_token}"},
        json={"user_answer": "B", "time_spent_seconds": 30}
    )
    
    assert response.status_code == 404


