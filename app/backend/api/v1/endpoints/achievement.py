"""Achievement endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict
from pydantic import BaseModel

from app.backend.core.database import get_db
from app.backend.core.security import get_current_user
from app.backend.api.v1.endpoints.auth import require_role
from app.backend.models.user import User, UserRole
from app.backend.services.achievement_service import (
    get_user_achievements,
    get_achievement_stats,
    check_achievements
)

router = APIRouter()


class AchievementResponse(BaseModel):
    """Achievement response model"""
    id: int
    name: str
    description: str | None
    icon: str | None
    category: str | None
    points: int
    earned: bool
    earned_at: str | None
    progress: Dict | None
    
    class Config:
        from_attributes = True


class AchievementStatsResponse(BaseModel):
    """Achievement statistics response"""
    total_achievements: int
    earned_count: int
    completion_percentage: float
    total_points: int
    by_category: Dict[str, int]


@router.get("/achievements", response_model=List[AchievementResponse])
async def list_achievements(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all achievements with user's earned status"""
    achievements = await get_user_achievements(db, current_user.id)
    return achievements


@router.get("/achievements/stats", response_model=AchievementStatsResponse)
async def get_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get achievement statistics for current user"""
    stats = await get_achievement_stats(db, current_user.id)
    return stats


@router.post("/achievements/check")
async def trigger_achievement_check(
    event_type: str,
    event_data: Dict | None = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Manually trigger achievement check (usually called automatically by other endpoints)
    This is useful for testing or manual triggers
    """
    newly_unlocked = await check_achievements(
        db=db,
        user_id=current_user.id,
        event_type=event_type,
        event_data=event_data
    )
    
    return {
        "unlocked_count": len(newly_unlocked),
        "unlocked_achievements": [
            {
                "id": ach.id,
                "name": ach.name,
                "description": ach.description,
                "icon": ach.icon
            }
            for ach in newly_unlocked
        ]
    }

