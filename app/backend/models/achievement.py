"""Achievement and gamification models"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.backend.core.database import Base


class Achievement(Base):
    """Defines available badges and achievements"""
    __tablename__ = "achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Content
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String(50), nullable=True)
    category = Column(String(50), nullable=True)  # 'completion', 'score', 'engagement', 'helper'
    
    # Criteria and progress
    criteria = Column(JSON, nullable=True)  # Conditions to earn
    progress_tracking = Column(JSON, nullable=True)  # Multi-step progress template
    points = Column(Integer, default=0, nullable=False)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    
    def __repr__(self):
        return f"<Achievement(id={self.id}, name='{self.name}')>"


class UserAchievement(Base):
    """Tracks which achievements users have earned"""
    __tablename__ = "user_achievements"
    
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    achievement_id = Column(Integer, ForeignKey("achievements.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    
    # Progress (for multi-step achievements)
    progress = Column(JSON, nullable=True)
    
    # Timestamps
    earned_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    # user = relationship("User")
    # achievement = relationship("Achievement")
    
    def __repr__(self):
        return f"<UserAchievement(user_id={self.user_id}, achievement_id={self.achievement_id})>"


class Leaderboard(Base):
    """Stores opt-in leaderboard standings"""
    __tablename__ = "leaderboards"
    
    id = Column(Integer, primary_key=True, index=True)
    cohort_id = Column(Integer, ForeignKey("cohorts.id", ondelete="CASCADE"), nullable=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Content
    category = Column(String(50), nullable=False, index=True)  # 'progress', 'scores', 'engagement'
    score = Column(Integer, default=0, nullable=False)
    rank = Column(Integer, nullable=True)
    
    # Timestamps
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Unique constraint
    __table_args__ = (
        UniqueConstraint('cohort_id', 'user_id', 'category', name='uq_leaderboard_cohort_user_category'),
    )
    
    def __repr__(self):
        return f"<Leaderboard(user_id={self.user_id}, category='{self.category}', score={self.score})>"


