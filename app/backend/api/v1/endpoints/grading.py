"""Grading endpoints for instructors"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from typing import List
from datetime import datetime

from app.backend.core.database import get_db
from app.backend.core.security import get_current_user
from app.backend.models.user import User, UserRole
from app.backend.models.assessment import Assessment, QuestionType
from app.backend.models.progress import QuizAttempt, ReviewStatus
from app.backend.models.module import Module
from app.backend.schemas.grading import (
    GradingQueueItem,
    GradingQueueResponse,
    GradeSubmission,
    GradedAttemptResponse,
    GradingHistoryResponse
)
from app.backend.api.v1.endpoints.auth import require_role

router = APIRouter()


@router.get("/grading/queue", response_model=GradingQueueResponse)
async def get_grading_queue(
    current_user: User = Depends(require_role([UserRole.INSTRUCTOR, UserRole.ADMIN])),
    db: AsyncSession = Depends(get_db),
    limit: int = 50,
    offset: int = 0
):
    """Get queue of assessments needing manual grading (instructor/admin only)"""
    # Get all attempts that need review
    # Note: Currently all questions are multiple-choice (auto-gradable),
    # but this endpoint is ready for when short-answer questions are added
    result = await db.execute(
        select(QuizAttempt)
        .join(Assessment)
        .join(Module)
        .join(User, QuizAttempt.user_id == User.id)
        .where(
            and_(
                QuizAttempt.review_status == ReviewStatus.NEEDS_REVIEW,
                Assessment.question_type.in_([QuestionType.SHORT_ANSWER, QuestionType.CODING_TASK])
            )
        )
        .order_by(QuizAttempt.attempted_at.asc())
        .limit(limit)
        .offset(offset)
    )
    attempts = result.scalars().all()
    
    # Get total count
    count_result = await db.execute(
        select(func.count(QuizAttempt.id))
        .join(Assessment)
        .where(
            and_(
                QuizAttempt.review_status == ReviewStatus.NEEDS_REVIEW,
                Assessment.question_type.in_([QuestionType.SHORT_ANSWER, QuestionType.CODING_TASK])
            )
        )
    )
    total = count_result.scalar() or 0
    
    # Build response items
    items = []
    for attempt in attempts:
        # Get assessment details
        assessment_result = await db.execute(
            select(Assessment).where(Assessment.id == attempt.assessment_id)
        )
        assessment = assessment_result.scalar_one_or_none()
        
        if not assessment:
            continue
        
        # Get module details
        module_result = await db.execute(
            select(Module).where(Module.id == assessment.module_id)
        )
        module = module_result.scalar_one_or_none()
        
        if not module:
            continue
        
        # Get user details
        user_result = await db.execute(
            select(User).where(User.id == attempt.user_id)
        )
        user = user_result.scalar_one_or_none()
        
        if not user:
            continue
        
        items.append(GradingQueueItem(
            attempt_id=attempt.id,
            user_id=attempt.user_id,
            user_name=user.full_name or user.username or user.email,
            user_email=user.email,
            assessment_id=assessment.id,
            question_text=assessment.question_text,
            question_type=assessment.question_type.value,
            user_answer=attempt.user_answer,
            correct_answer=assessment.correct_answer,
            module_id=module.id,
            module_title=module.title,
            attempted_at=attempt.attempted_at,
            time_spent_seconds=attempt.time_spent_seconds
        ))
    
    return GradingQueueResponse(items=items, total=total)


@router.post("/grading/{attempt_id}", response_model=GradedAttemptResponse)
async def grade_attempt(
    attempt_id: int,
    grade_data: GradeSubmission,
    current_user: User = Depends(require_role([UserRole.INSTRUCTOR, UserRole.ADMIN])),
    db: AsyncSession = Depends(get_db)
):
    """Grade a quiz attempt (instructor/admin only)"""
    # Get attempt
    result = await db.execute(
        select(QuizAttempt)
        .where(QuizAttempt.id == attempt_id)
    )
    attempt = result.scalar_one_or_none()
    
    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attempt not found"
        )
    
    # Get assessment to verify it needs manual grading
    assessment_result = await db.execute(
        select(Assessment).where(Assessment.id == attempt.assessment_id)
    )
    assessment = assessment_result.scalar_one_or_none()
    
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )
    
    # Verify this is a manual-grading question type
    if assessment.question_type not in [QuestionType.SHORT_ANSWER, QuestionType.CODING_TASK]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This assessment is auto-graded and does not require manual grading"
        )
    
    # Verify attempt needs grading
    if attempt.review_status == ReviewStatus.GRADED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This attempt has already been graded"
        )
    
    # Update attempt with grade
    attempt.is_correct = grade_data.is_correct
    attempt.points_earned = grade_data.points_earned
    attempt.review_status = ReviewStatus.GRADED
    attempt.graded_by = current_user.id
    attempt.feedback = grade_data.feedback
    attempt.partial_credit = grade_data.partial_credit
    attempt.graded_at = datetime.now()
    
    await db.commit()
    await db.refresh(attempt)
    
    return GradedAttemptResponse(
        id=attempt.id,
        user_id=attempt.user_id,
        assessment_id=attempt.assessment_id,
        user_answer=attempt.user_answer,
        is_correct=attempt.is_correct,
        points_earned=attempt.points_earned,
        review_status=attempt.review_status,
        graded_by=attempt.graded_by,
        feedback=attempt.feedback,
        partial_credit=attempt.partial_credit,
        graded_at=attempt.graded_at,
        attempted_at=attempt.attempted_at
    )


@router.get("/grading/history", response_model=GradingHistoryResponse)
async def get_grading_history(
    current_user: User = Depends(require_role([UserRole.INSTRUCTOR, UserRole.ADMIN])),
    db: AsyncSession = Depends(get_db),
    user_id: int = None,
    module_id: int = None,
    limit: int = 50,
    offset: int = 0
):
    """Get grading history (instructor/admin only)"""
    # Build query
    query = select(QuizAttempt).where(
        QuizAttempt.review_status == ReviewStatus.GRADED
    )
    
    # Filter by user if provided
    if user_id:
        query = query.where(QuizAttempt.user_id == user_id)
    
    # Filter by module if provided
    if module_id:
        query = query.join(Assessment).where(Assessment.module_id == module_id)
    
    # Order by graded_at descending (most recent first)
    query = query.order_by(QuizAttempt.graded_at.desc())
    
    # Get total count
    count_query = select(func.count(QuizAttempt.id)).where(
        QuizAttempt.review_status == ReviewStatus.GRADED
    )
    if user_id:
        count_query = count_query.where(QuizAttempt.user_id == user_id)
    if module_id:
        count_query = count_query.join(Assessment).where(Assessment.module_id == module_id)
    
    count_result = await db.execute(count_query)
    total = count_result.scalar() or 0
    
    # Get paginated results
    result = await db.execute(
        query.limit(limit).offset(offset)
    )
    attempts = result.scalars().all()
    
    items = [
        GradedAttemptResponse(
            id=attempt.id,
            user_id=attempt.user_id,
            assessment_id=attempt.assessment_id,
            user_answer=attempt.user_answer,
            is_correct=attempt.is_correct,
            points_earned=attempt.points_earned,
            review_status=attempt.review_status,
            graded_by=attempt.graded_by,
            feedback=attempt.feedback,
            partial_credit=attempt.partial_credit,
            graded_at=attempt.graded_at,
            attempted_at=attempt.attempted_at
        )
        for attempt in attempts
    ]
    
    return GradingHistoryResponse(items=items, total=total)

