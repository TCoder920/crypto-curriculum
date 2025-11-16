"""Achievement checking and unlocking service"""
import json
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload

from app.backend.models.achievement import Achievement, UserAchievement
from app.backend.models.progress import UserProgress, QuizAttempt, ProgressStatus
from app.backend.models.assessment import Assessment
from app.backend.models.forum import ForumPost, ForumVote
from app.backend.models.module import Module
from app.backend.models.user import User
from app.backend.services.notification_service import create_notification

logger = logging.getLogger(__name__)


async def check_achievements(
    db: AsyncSession,
    user_id: int,
    event_type: str,
    event_data: Optional[Dict] = None
) -> List[Achievement]:
    """
    Check and unlock achievements based on user events.
    
    Args:
        db: Database session
        user_id: User ID to check achievements for
        event_type: Type of event ('module_completed', 'assessment_submitted', 'forum_post', etc.)
        event_data: Additional data about the event
        
    Returns:
        List of newly unlocked achievements
    """
    newly_unlocked = []
    
    # Get all active achievements
    result = await db.execute(
        select(Achievement).where(Achievement.is_active == True)
    )
    all_achievements = result.scalars().all()
    
    # Get user's existing achievements
    result = await db.execute(
        select(UserAchievement).where(UserAchievement.user_id == user_id)
    )
    user_achievements = {ua.achievement_id for ua in result.scalars().all()}
    
    for achievement in all_achievements:
        # Skip if already earned
        if achievement.id in user_achievements:
            continue
        
        # Check if achievement criteria matches event
        if not achievement.criteria:
            continue
        
        try:
            criteria = achievement.criteria if isinstance(achievement.criteria, dict) else json.loads(achievement.criteria)
        except (json.JSONDecodeError, TypeError):
            logger.warning(f"Achievement {achievement.id} has invalid criteria JSON")
            continue
        
        # Check if this achievement is relevant to the event
        if not _is_relevant_achievement(criteria, event_type):
            continue
        
        # Evaluate achievement criteria
        if await _evaluate_achievement(db, user_id, achievement, event_type, event_data):
            # Unlock achievement
            user_achievement = UserAchievement(
                user_id=user_id,
                achievement_id=achievement.id,
                earned_at=datetime.utcnow()
            )
            db.add(user_achievement)
            newly_unlocked.append(achievement)
            
            # Create notification
            await create_notification(
                db=db,
                user_id=user_id,
                notification_type="achievement_unlocked",
                title="Achievement Unlocked! 🏆",
                message=f"You've earned the '{achievement.name}' achievement!",
                link=f"/achievements"
            )
            
            logger.info(f"User {user_id} unlocked achievement: {achievement.name}")
    
    if newly_unlocked:
        await db.commit()
    
    return newly_unlocked


def _is_relevant_achievement(criteria: Dict, event_type: str) -> bool:
    """Check if achievement criteria is relevant to the event type"""
    if event_type == "module_completed":
        return "module_completion" in criteria or "track_completion" in criteria
    elif event_type == "assessment_submitted":
        return "perfect_score" in criteria or "score_threshold" in criteria
    elif event_type == "forum_post":
        return "forum_help" in criteria or "forum_engagement" in criteria
    elif event_type == "streak":
        return "streak" in criteria
    elif event_type == "track_completed":
        return "track_completion" in criteria
    return False


async def _evaluate_achievement(
    db: AsyncSession,
    user_id: int,
    achievement: Achievement,
    event_type: str,
    event_data: Optional[Dict]
) -> bool:
    """Evaluate if user meets achievement criteria"""
    try:
        criteria = achievement.criteria if isinstance(achievement.criteria, dict) else json.loads(achievement.criteria)
    except (json.JSONDecodeError, TypeError):
        return False
    
    # Module completion achievements
    if "module_completion" in criteria:
        module_criteria = criteria["module_completion"]
        if "module_id" in module_criteria:
            # Specific module completion
            module_id = module_criteria["module_id"]
            result = await db.execute(
                select(UserProgress).where(
                    and_(
                        UserProgress.user_id == user_id,
                        UserProgress.module_id == module_id,
                        UserProgress.status == ProgressStatus.COMPLETED
                    )
                )
            )
            return result.scalar_one_or_none() is not None
        elif "any_module" in module_criteria:
            # Any module completion
            result = await db.execute(
                select(func.count(UserProgress.id)).where(
                    and_(
                        UserProgress.user_id == user_id,
                        UserProgress.status == ProgressStatus.COMPLETED
                    )
                )
            )
            count = result.scalar()
            return count > 0
    
    # Perfect score achievements
    if "perfect_score" in criteria:
        perfect_criteria = criteria["perfect_score"]
        if "any_assessment" in perfect_criteria:
            # Check for any 100% score
            result = await db.execute(
                select(QuizAttempt).where(
                    and_(
                        QuizAttempt.user_id == user_id,
                        QuizAttempt.score_percentage == 100.0
                    )
                )
            )
            return result.scalar_one_or_none() is not None
        elif "module_id" in perfect_criteria:
            # Perfect score on specific module
            module_id = perfect_criteria["module_id"]
            result = await db.execute(
                select(QuizAttempt)
                .join(Assessment)
                .where(
                    and_(
                        QuizAttempt.user_id == user_id,
                        Assessment.module_id == module_id,
                        QuizAttempt.score_percentage == 100.0
                    )
                )
            )
            return result.scalar_one_or_none() is not None
    
    # Score threshold achievements
    if "score_threshold" in criteria:
        threshold_criteria = criteria["score_threshold"]
        threshold = threshold_criteria.get("min_score", 70)
        result = await db.execute(
            select(func.max(QuizAttempt.score_percentage)).where(
                QuizAttempt.user_id == user_id
            )
        )
        max_score = result.scalar()
        return max_score is not None and max_score >= threshold
    
    # Forum help achievements
    if "forum_help" in criteria:
        help_criteria = criteria["forum_help"]
        target_posts = help_criteria.get("posts", 10)
        
        # Count helpful posts (posts with upvotes or marked as solved)
        result = await db.execute(
            select(func.count(ForumPost.id)).where(
                and_(
                    ForumPost.user_id == user_id,
                    or_(
                        ForumPost.is_solved == True,
                        ForumPost.id.in_(
                            select(ForumVote.post_id).where(
                                and_(
                                    ForumVote.post_id == ForumPost.id,
                                    ForumVote.vote_type == "upvote"
                                )
                            )
                        )
                    )
                )
            )
        )
        helpful_posts = result.scalar()
        return helpful_posts >= target_posts
    
    # Track completion achievements
    if "track_completion" in criteria:
        track_criteria = criteria["track_completion"]
        if "track_name" in track_criteria:
            track_name = track_criteria["track_name"]
            # Get all modules in track
            result = await db.execute(
                select(Module).where(Module.track == track_name)
            )
            track_modules = result.scalars().all()
            track_module_ids = [m.id for m in track_modules]
            
            if not track_module_ids:
                return False
            
            # Check if all modules in track are completed
            result = await db.execute(
                select(func.count(UserProgress.id)).where(
                    and_(
                        UserProgress.user_id == user_id,
                        UserProgress.module_id.in_(track_module_ids),
                        UserProgress.status == ProgressStatus.COMPLETED
                    )
                )
            )
            completed_count = result.scalar()
            return completed_count == len(track_module_ids)
        elif "all_tracks" in track_criteria:
            # Master certificate - all 4 tracks completed
            tracks = ["beginner", "power_user", "developer", "architect"]
            all_completed = True
            
            for track_name in tracks:
                result = await db.execute(
                    select(Module).where(Module.track == track_name)
                )
                track_modules = result.scalars().all()
                track_module_ids = [m.id for m in track_modules]
                
                if not track_module_ids:
                    continue
                
                result = await db.execute(
                    select(func.count(UserProgress.id)).where(
                        and_(
                            UserProgress.user_id == user_id,
                            UserProgress.module_id.in_(track_module_ids),
                            UserProgress.status == ProgressStatus.COMPLETED
                        )
                    )
                )
                completed_count = result.scalar()
                if completed_count < len(track_module_ids):
                    all_completed = False
                    break
            
            return all_completed
    
    # Streak achievements
    if "streak" in criteria:
        streak_criteria = criteria["streak"]
        target_days = streak_criteria.get("days", 7)
        
        # Get user's last activity dates from progress updates
        result = await db.execute(
            select(UserProgress.updated_at)
            .where(UserProgress.user_id == user_id)
            .order_by(UserProgress.updated_at.desc())
            .limit(target_days)
        )
        activity_dates = [row[0] for row in result.all() if row[0]]
        
        if len(activity_dates) < target_days:
            return False
        
        # Check for consecutive days
        today = datetime.utcnow().date()
        consecutive_days = 0
        check_date = today
        
        for i in range(target_days):
            if any(act_date.date() == check_date for act_date in activity_dates if act_date):
                consecutive_days += 1
                check_date -= timedelta(days=1)
            else:
                break
        
        return consecutive_days >= target_days
    
    return False


async def get_user_achievements(
    db: AsyncSession,
    user_id: int
) -> List[Dict]:
    """Get all achievements for a user with progress information"""
    # Get all achievements
    result = await db.execute(select(Achievement).where(Achievement.is_active == True))
    all_achievements = result.scalars().all()
    
    # Get user's earned achievements
    result = await db.execute(
        select(UserAchievement).where(UserAchievement.user_id == user_id)
    )
    user_achievements = {ua.achievement_id: ua for ua in result.scalars().all()}
    
    achievements_list = []
    for achievement in all_achievements:
        user_achievement = user_achievements.get(achievement.id)
        
        achievements_list.append({
            "id": achievement.id,
            "name": achievement.name,
            "description": achievement.description,
            "icon": achievement.icon,
            "category": achievement.category,
            "points": achievement.points,
            "earned": user_achievement is not None,
            "earned_at": user_achievement.earned_at.isoformat() if user_achievement else None,
            "progress": user_achievement.progress if user_achievement else None,
        })
    
    return achievements_list


async def get_achievement_stats(
    db: AsyncSession,
    user_id: int
) -> Dict:
    """Get achievement statistics for a user"""
    # Total achievements
    result = await db.execute(
        select(func.count(Achievement.id)).where(Achievement.is_active == True)
    )
    total_achievements = result.scalar()
    
    # Earned achievements
    result = await db.execute(
        select(func.count(UserAchievement.achievement_id)).where(
            UserAchievement.user_id == user_id
        )
    )
    earned_count = result.scalar()
    
    # Total points
    result = await db.execute(
        select(func.sum(Achievement.points))
        .join(UserAchievement)
        .where(UserAchievement.user_id == user_id)
    )
    total_points = result.scalar() or 0
    
    # Achievements by category
    result = await db.execute(
        select(Achievement.category, func.count(UserAchievement.achievement_id))
        .join(UserAchievement)
        .where(UserAchievement.user_id == user_id)
        .group_by(Achievement.category)
    )
    by_category = {row[0]: row[1] for row in result.all() if row[0]}
    
    return {
        "total_achievements": total_achievements,
        "earned_count": earned_count,
        "completion_percentage": round((earned_count / total_achievements * 100) if total_achievements > 0 else 0, 1),
        "total_points": total_points,
        "by_category": by_category,
    }

