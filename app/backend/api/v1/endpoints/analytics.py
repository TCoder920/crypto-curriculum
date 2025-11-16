"""Analytics and reporting endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_, case
from typing import Dict, List, Optional
from pydantic import BaseModel
from datetime import datetime, timedelta

from app.backend.core.database import get_db
from app.backend.core.security import get_current_user
from app.backend.api.v1.endpoints.auth import require_role
from app.backend.models.user import User, UserRole
from app.backend.models.progress import UserProgress, QuizAttempt, ProgressStatus
from app.backend.models.assessment import Assessment
from app.backend.models.module import Module
from app.backend.models.cohort import Cohort, CohortMember
from app.backend.models.achievement import UserAchievement, Achievement

router = APIRouter()


class StudentAnalyticsResponse(BaseModel):
    """Student analytics response"""
    user_id: int
    total_modules_completed: int
    total_modules_started: int
    average_score: float
    total_attempts: int
    current_streak_days: int
    total_achievements: int
    total_points: int
    modules_by_status: Dict[str, int]
    scores_by_module: List[Dict]
    recent_activity: List[Dict]


class CohortAnalyticsResponse(BaseModel):
    """Cohort analytics response"""
    cohort_id: int
    cohort_name: str
    total_students: int
    active_students: int
    average_progress: float
    average_score: float
    completion_rate: float
    students_by_progress: Dict[str, int]
    top_performers: List[Dict]
    at_risk_students: List[Dict]


class PlatformAnalyticsResponse(BaseModel):
    """Platform-wide analytics (admin only)"""
    total_users: int
    total_students: int
    total_instructors: int
    total_modules: int
    total_assessments: int
    total_attempts: int
    average_completion_rate: float
    average_score: float
    active_users_last_30_days: int
    new_users_last_30_days: int
    modules_by_track: Dict[str, int]
    completion_by_track: Dict[str, float]


@router.get("/analytics/student/{user_id}", response_model=StudentAnalyticsResponse)
async def get_student_analytics(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get analytics for a specific student (own data or instructor/admin)"""
    # Check permissions
    if current_user.id != user_id and current_user.role not in [UserRole.INSTRUCTOR, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this student's analytics"
        )
    
    # Get user progress
    result = await db.execute(
        select(UserProgress).where(UserProgress.user_id == user_id)
    )
    all_progress = result.scalars().all()
    
    # Calculate statistics
    total_modules_completed = sum(1 for p in all_progress if p.status == ProgressStatus.COMPLETED)
    total_modules_started = sum(1 for p in all_progress if p.status != ProgressStatus.NOT_STARTED)
    
    modules_by_status = {
        "completed": sum(1 for p in all_progress if p.status == ProgressStatus.COMPLETED),
        "in_progress": sum(1 for p in all_progress if p.status == ProgressStatus.IN_PROGRESS),
        "not_started": sum(1 for p in all_progress if p.status == ProgressStatus.NOT_STARTED),
    }
    
    # Get quiz attempts
    result = await db.execute(
        select(QuizAttempt).where(QuizAttempt.user_id == user_id)
    )
    all_attempts = result.scalars().all()
    total_attempts = len(all_attempts)
    
    # Calculate average score
    scores = [a.score_percentage for a in all_attempts if a.score_percentage is not None]
    average_score = sum(scores) / len(scores) if scores else 0.0
    
    # Get scores by module
    result = await db.execute(
        select(
            Module.id,
            Module.title,
            func.max(QuizAttempt.score_percentage).label("best_score")
        )
        .join(QuizAttempt, QuizAttempt.assessment_id.in_(
            select(Assessment.id).where(Assessment.module_id == Module.id)
        ))
        .where(QuizAttempt.user_id == user_id)
        .group_by(Module.id, Module.title)
    )
    scores_by_module = [
        {"module_id": row[0], "module_title": row[1], "best_score": row[2] or 0.0}
        for row in result.all()
    ]
    
    # Calculate streak (simplified - based on recent activity)
    recent_progress = [p for p in all_progress if p.last_accessed_at]
    if recent_progress:
        recent_dates = sorted([p.last_accessed_at.date() for p in recent_progress], reverse=True)
        current_streak = 0
        check_date = datetime.now().date()
        for date in recent_dates:
            if date == check_date or date == check_date - timedelta(days=1):
                current_streak += 1
                check_date = date - timedelta(days=1)
            else:
                break
    else:
        current_streak = 0
    
    # Get achievements
    result = await db.execute(
        select(func.count(UserAchievement.achievement_id)).where(
            UserAchievement.user_id == user_id
        )
    )
    total_achievements = result.scalar() or 0
    
    result = await db.execute(
        select(func.sum(Achievement.points))
        .join(UserAchievement)
        .where(UserAchievement.user_id == user_id)
    )
    total_points = result.scalar() or 0
    
    # Recent activity (last 10 progress updates)
    recent_activity = [
        {
            "module_id": p.module_id,
            "module_title": "Module",  # Would need to join with Module
            "status": p.status.value,
            "updated_at": p.last_accessed_at.isoformat() if p.last_accessed_at else None
        }
        for p in sorted(all_progress, key=lambda x: x.last_accessed_at or datetime.min, reverse=True)[:10]
    ]
    
    return StudentAnalyticsResponse(
        user_id=user_id,
        total_modules_completed=total_modules_completed,
        total_modules_started=total_modules_started,
        average_score=round(average_score, 2),
        total_attempts=total_attempts,
        current_streak_days=current_streak,
        total_achievements=total_achievements,
        total_points=total_points,
        modules_by_status=modules_by_status,
        scores_by_module=scores_by_module,
        recent_activity=recent_activity
    )


@router.get("/analytics/cohort/{cohort_id}", response_model=CohortAnalyticsResponse)
async def get_cohort_analytics(
    cohort_id: int,
    current_user: User = Depends(require_role([UserRole.INSTRUCTOR, UserRole.ADMIN])),
    db: AsyncSession = Depends(get_db)
):
    """Get analytics for a cohort (instructor/admin only)"""
    # Verify cohort exists
    result = await db.execute(select(Cohort).where(Cohort.id == cohort_id))
    cohort = result.scalar_one_or_none()
    if not cohort:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cohort not found"
        )
    
    # Get cohort members
    result = await db.execute(
        select(CohortMember).where(CohortMember.cohort_id == cohort_id)
    )
    members = result.scalars().all()
    total_students = len(members)
    student_ids = [m.user_id for m in members]
    
    if not student_ids:
        return CohortAnalyticsResponse(
            cohort_id=cohort_id,
            cohort_name=cohort.name,
            total_students=0,
            active_students=0,
            average_progress=0.0,
            average_score=0.0,
            completion_rate=0.0,
            students_by_progress={},
            top_performers=[],
            at_risk_students=[]
        )
    
    # Get progress for all students
    result = await db.execute(
        select(UserProgress).where(UserProgress.user_id.in_(student_ids))
    )
    all_progress = result.scalars().all()
    
    # Calculate statistics
    total_modules = 17  # Total modules in curriculum
    completed_count = sum(1 for p in all_progress if p.status == ProgressStatus.COMPLETED)
    total_progress_records = len(all_progress)
    average_progress = (completed_count / (total_students * total_modules) * 100) if total_students > 0 else 0.0
    
    # Get quiz attempts
    result = await db.execute(
        select(QuizAttempt).where(QuizAttempt.user_id.in_(student_ids))
    )
    all_attempts = result.scalars().all()
    
    scores = [a.score_percentage for a in all_attempts if a.score_percentage is not None]
    average_score = sum(scores) / len(scores) if scores else 0.0
    
    # Active students (progress in last 7 days)
    seven_days_ago = datetime.now() - timedelta(days=7)
    active_students = len(set(
        p.user_id for p in all_progress
        if p.last_accessed_at and p.last_accessed_at >= seven_days_ago
    ))
    
    # Completion rate
    total_modules_completed = sum(1 for p in all_progress if p.status == ProgressStatus.COMPLETED)
    completion_rate = (total_modules_completed / (total_students * total_modules) * 100) if total_students > 0 else 0.0
    
    # Students by progress status
    students_by_progress = {
        "completed": len(set(p.user_id for p in all_progress if p.status == ProgressStatus.COMPLETED)),
        "in_progress": len(set(p.user_id for p in all_progress if p.status == ProgressStatus.IN_PROGRESS)),
        "not_started": total_students - len(set(p.user_id for p in all_progress)),
    }
    
    # Top performers (students with most completed modules)
    from collections import defaultdict
    completed_by_student = defaultdict(int)
    for p in all_progress:
        if p.status == ProgressStatus.COMPLETED:
            completed_by_student[p.user_id] += 1
    
    top_performers = sorted(
        [{"user_id": uid, "modules_completed": count} for uid, count in completed_by_student.items()],
        key=lambda x: x["modules_completed"],
        reverse=True
    )[:5]
    
    # At-risk students (no activity in 7 days or failing)
    at_risk = []
    for member in members:
        user_progress = [p for p in all_progress if p.user_id == member.user_id]
        if not user_progress:
            at_risk.append({"user_id": member.user_id, "reason": "No activity"})
        else:
            last_activity = max((p.last_accessed_at for p in user_progress if p.last_accessed_at), default=None)
            if last_activity and (datetime.now() - last_activity).days > 7:
                at_risk.append({"user_id": member.user_id, "reason": "Inactive >7 days"})
    
    return CohortAnalyticsResponse(
        cohort_id=cohort_id,
        cohort_name=cohort.name,
        total_students=total_students,
        active_students=active_students,
        average_progress=round(average_progress, 2),
        average_score=round(average_score, 2),
        completion_rate=round(completion_rate, 2),
        students_by_progress=students_by_progress,
        top_performers=top_performers,
        at_risk_students=at_risk
    )


@router.get("/analytics/platform", response_model=PlatformAnalyticsResponse)
async def get_platform_analytics(
    current_user: User = Depends(require_role([UserRole.ADMIN])),
    db: AsyncSession = Depends(get_db)
):
    """Get platform-wide analytics (admin only)"""
    # Total users
    result = await db.execute(select(func.count(User.id)))
    total_users = result.scalar()
    
    result = await db.execute(select(func.count(User.id)).where(User.role == UserRole.STUDENT))
    total_students = result.scalar()
    
    result = await db.execute(select(func.count(User.id)).where(User.role == UserRole.INSTRUCTOR))
    total_instructors = result.scalar()
    
    # Total modules and assessments
    result = await db.execute(select(func.count(Module.id)))
    total_modules = result.scalar()
    
    result = await db.execute(select(func.count(Assessment.id)))
    total_assessments = result.scalar()
    
    result = await db.execute(select(func.count(QuizAttempt.id)))
    total_attempts = result.scalar()
    
    # Average completion rate
    result = await db.execute(
        select(func.count(UserProgress.id)).where(
            UserProgress.status == ProgressStatus.COMPLETED
        )
    )
    completed_modules = result.scalar()
    
    result = await db.execute(select(func.count(UserProgress.id)))
    total_progress_records = result.scalar()
    average_completion_rate = (completed_modules / total_progress_records * 100) if total_progress_records > 0 else 0.0
    
    # Average score
    result = await db.execute(
        select(func.avg(QuizAttempt.score_percentage)).where(
            QuizAttempt.score_percentage.isnot(None)
        )
    )
    average_score = result.scalar() or 0.0
    
    # Active users (last 30 days)
    thirty_days_ago = datetime.now() - timedelta(days=30)
    result = await db.execute(
        select(func.count(func.distinct(UserProgress.user_id))).where(
            UserProgress.last_accessed_at >= thirty_days_ago
        )
    )
    active_users_last_30_days = result.scalar() or 0
    
    # New users (last 30 days)
    result = await db.execute(
        select(func.count(User.id)).where(User.created_at >= thirty_days_ago)
    )
    new_users_last_30_days = result.scalar() or 0
    
    # Modules by track
    result = await db.execute(
        select(Module.track, func.count(Module.id))
        .group_by(Module.track)
    )
    modules_by_track = {row[0]: row[1] for row in result.all() if row[0]}
    
    # Completion by track
    result = await db.execute(
        select(
            Module.track,
            func.count(case((UserProgress.status == ProgressStatus.COMPLETED, 1))).label("completed"),
            func.count(UserProgress.id).label("total")
        )
        .join(UserProgress, UserProgress.module_id == Module.id)
        .group_by(Module.track)
    )
    completion_by_track = {
        row[0]: round((row[1] / row[2] * 100) if row[2] > 0 else 0.0, 2)
        for row in result.all() if row[0]
    }
    
    return PlatformAnalyticsResponse(
        total_users=total_users,
        total_students=total_students,
        total_instructors=total_instructors,
        total_modules=total_modules,
        total_assessments=total_assessments,
        total_attempts=total_attempts,
        average_completion_rate=round(average_completion_rate, 2),
        average_score=round(average_score, 2),
        active_users_last_30_days=active_users_last_30_days,
        new_users_last_30_days=new_users_last_30_days,
        modules_by_track=modules_by_track,
        completion_by_track=completion_by_track
    )

