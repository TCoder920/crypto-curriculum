"""Assessment endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload
from typing import List

from app.backend.core.database import get_db
from app.backend.core.security import get_current_user
from app.backend.models.user import User
from app.backend.models.assessment import Assessment, QuestionType
from app.backend.models.progress import QuizAttempt, ReviewStatus, UserProgress, ProgressStatus
from app.backend.models.module import Module
from datetime import datetime
from app.backend.schemas.assessment import (
    AssessmentResponse,
    AssessmentSubmit,
    AssessmentSubmitResponse,
    ModuleResultsResponse,
    QuizAttemptResponse,
    AssessmentListResponse,
)

router = APIRouter()


@router.get("/modules/{module_id}/assessments", response_model=AssessmentListResponse)
async def get_module_assessments(
    module_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all assessment questions for a module"""
    # Verify module exists
    result = await db.execute(select(Module).where(Module.id == module_id))
    module = result.scalar_one_or_none()
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module not found"
        )
    
    # Get all active assessments for this module, ordered by order_index
    result = await db.execute(
        select(Assessment)
        .where(
            and_(
                Assessment.module_id == module_id,
                Assessment.is_active == True
            )
        )
        .order_by(Assessment.order_index)
    )
    assessments = result.scalars().all()
    
    # Calculate total points
    total_points = sum(a.points for a in assessments)
    
    # Convert to response models (hide correct_answer from user)
    assessment_responses = [
        AssessmentResponse(
            id=a.id,
            module_id=a.module_id,
            question_text=a.question_text,
            question_type=a.question_type,
            order_index=a.order_index,
            points=a.points,
            options=a.options,
            explanation=None  # Don't show explanation until after submission
        )
        for a in assessments
    ]
    
    return AssessmentListResponse(
        module_id=module.id,
        module_title=module.title,
        assessments=assessment_responses,
        total_points=total_points,
        estimated_time_minutes=len(assessments) * 3  # 3 minutes per question estimate
    )


@router.post("/assessments/{assessment_id}/submit", response_model=AssessmentSubmitResponse)
async def submit_assessment_answer(
    assessment_id: int,
    submission: AssessmentSubmit,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Submit an answer to an assessment question"""
    # Get assessment
    result = await db.execute(select(Assessment).where(Assessment.id == assessment_id))
    assessment = result.scalar_one_or_none()
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )
    
    if not assessment.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assessment is not active"
        )
    
    # Determine if auto-grading is possible
    is_auto_gradable = assessment.question_type in [QuestionType.MULTIPLE_CHOICE, QuestionType.TRUE_FALSE]
    
    # Auto-grade if possible
    is_correct = None
    points_earned = None
    review_status = ReviewStatus.PENDING
    
    if is_auto_gradable:
        # Normalize answers for comparison
        user_answer_normalized = submission.user_answer.strip().upper()
        correct_answer_normalized = assessment.correct_answer.strip().upper()
        
        is_correct = user_answer_normalized == correct_answer_normalized
        points_earned = assessment.points if is_correct else 0
        review_status = ReviewStatus.GRADED
    else:
        # Short answer or coding task - needs manual grading
        review_status = ReviewStatus.NEEDS_REVIEW
        points_earned = None
    
    # Create quiz attempt record
    quiz_attempt = QuizAttempt(
        user_id=current_user.id,
        assessment_id=assessment_id,
        user_answer=submission.user_answer,
        is_correct=is_correct,
        points_earned=points_earned,
        review_status=review_status,
        time_spent_seconds=submission.time_spent_seconds
    )
    
    db.add(quiz_attempt)
    await db.commit()
    await db.refresh(quiz_attempt)
    
    # Prepare response
    response = AssessmentSubmitResponse(
        attempt_id=quiz_attempt.id,
        is_correct=is_correct,
        points_earned=points_earned,
        review_status=review_status,
        explanation=assessment.explanation if is_auto_gradable else None,
        correct_answer=assessment.correct_answer if is_auto_gradable else None
    )
    
    return response


@router.get("/assessments/results/{module_id}", response_model=ModuleResultsResponse)
async def get_module_results(
    module_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user's assessment results for a module"""
    # Verify module exists
    result = await db.execute(select(Module).where(Module.id == module_id))
    module = result.scalar_one_or_none()
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module not found"
        )
    
    # Get all assessments for this module
    result = await db.execute(
        select(Assessment)
        .where(
            and_(
                Assessment.module_id == module_id,
                Assessment.is_active == True
            )
        )
    )
    assessments = result.scalars().all()
    total_questions = len(assessments)
    
    if total_questions == 0:
        return ModuleResultsResponse(
            module_id=module_id,
            module_title=module.title,
            total_questions=0,
            attempted=0,
            correct=0,
            pending_review=0,
            score_percent=0.0,
            points_earned=0,
            points_possible=0,
            attempts=[],
            can_progress=False,
            attempt_count=0
        )
    
    # Get all attempts for this user and module
    assessment_ids = [a.id for a in assessments]
    result = await db.execute(
        select(QuizAttempt)
        .join(Assessment)
        .where(
            and_(
                QuizAttempt.user_id == current_user.id,
                QuizAttempt.assessment_id.in_(assessment_ids)
            )
        )
        .order_by(QuizAttempt.attempted_at.desc())
    )
    all_attempts = result.scalars().all()
    
    # Get the most recent attempt for each assessment
    latest_attempts = {}
    for attempt in all_attempts:
        if attempt.assessment_id not in latest_attempts:
            latest_attempts[attempt.assessment_id] = attempt
    
    # Calculate statistics
    attempted = len(latest_attempts)
    correct = sum(1 for a in latest_attempts.values() if a.is_correct is True)
    pending_review = sum(
        1 for a in latest_attempts.values()
        if a.review_status == ReviewStatus.NEEDS_REVIEW or a.review_status == ReviewStatus.PENDING
    )
    
    # Calculate points
    points_possible = sum(a.points for a in assessments)
    points_earned = sum(
        a.points_earned or 0 for a in latest_attempts.values()
    )
    
    # Calculate score percentage
    if points_possible > 0:
        score_percent = (points_earned / points_possible) * 100
    else:
        score_percent = 0.0
    
    # Check if user can progress (>= 70% and all questions attempted)
    can_progress = score_percent >= 70.0 and attempted == total_questions and pending_review == 0
    
    # Get best score (highest score from any attempt)
    best_score = 0.0
    if all_attempts:
        # Group attempts by assessment and find best score for each
        best_scores_by_assessment = {}
        for attempt in all_attempts:
            if attempt.assessment_id not in best_scores_by_assessment:
                best_scores_by_assessment[attempt.assessment_id] = attempt.points_earned or 0
            else:
                current_best = best_scores_by_assessment[attempt.assessment_id]
                attempt_points = attempt.points_earned or 0
                if attempt_points > current_best:
                    best_scores_by_assessment[attempt.assessment_id] = attempt_points
        
        best_points = sum(best_scores_by_assessment.values())
        if points_possible > 0:
            best_score = (best_points / points_possible) * 100
    
    # Count total attempts (how many times user has taken the assessment)
    attempt_count = len(set(
        (a.assessment_id, a.attempted_at.date())
        for a in all_attempts
    ))
    
    # Build attempt responses - need to join with Assessment to get question details
    # Create a mapping of assessment_id to Assessment object
    assessment_map = {a.id: a for a in assessments}
    
    attempt_responses = []
    for assessment_id, attempt in latest_attempts.items():
        assessment = assessment_map.get(assessment_id)
        if assessment:
            attempt_responses.append(
                QuizAttemptResponse(
                    attempt_id=attempt.id,
                    assessment_id=assessment.id,
                    question_text=assessment.question_text,
                    question_type=assessment.question_type,
                    user_answer=attempt.user_answer,
                    is_correct=attempt.is_correct,
                    points_earned=attempt.points_earned,
                    review_status=attempt.review_status,
                    feedback=attempt.feedback,
                    attempted_at=attempt.attempted_at
                )
            )
    
    # Sort by assessment order_index
    attempt_responses.sort(key=lambda x: next(
        a.order_index for a in assessments if a.id == x.assessment_id
    ))
    
    # If user can progress, mark module as completed in UserProgress
    if can_progress:
        # Check if UserProgress exists
        result = await db.execute(
            select(UserProgress)
            .where(
                and_(
                    UserProgress.user_id == current_user.id,
                    UserProgress.module_id == module_id
                )
            )
        )
        user_progress = result.scalar_one_or_none()
        
        if user_progress:
            # Update existing progress
            user_progress.status = ProgressStatus.COMPLETED
            user_progress.completion_percentage = 100.0
            user_progress.completed_at = datetime.now()
            user_progress.last_accessed_at = datetime.now()
        else:
            # Create new progress record
            user_progress = UserProgress(
                user_id=current_user.id,
                module_id=module_id,
                status=ProgressStatus.COMPLETED,
                completion_percentage=100.0,
                started_at=datetime.now(),
                completed_at=datetime.now(),
                last_accessed_at=datetime.now()
            )
            db.add(user_progress)
        
        await db.commit()
    
    return ModuleResultsResponse(
        module_id=module_id,
        module_title=module.title,
        total_questions=total_questions,
        attempted=attempted,
        correct=correct,
        pending_review=pending_review,
        score_percent=round(score_percent, 2),
        points_earned=points_earned,
        points_possible=points_possible,
        attempts=attempt_responses,
        can_progress=can_progress,
        best_score_percent=round(best_score, 2) if best_score > 0 else None,
        attempt_count=attempt_count
    )

