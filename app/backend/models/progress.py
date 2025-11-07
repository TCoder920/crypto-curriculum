"""User progress and quiz attempt models"""
from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime, Float, Enum as SQLEnum, JSON, UniqueConstraint, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.backend.core.database import Base
import enum


class ProgressStatus(str, enum.Enum):
    """Progress status enumeration"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class ReviewStatus(str, enum.Enum):
    """Review status enumeration"""
    PENDING = "pending"
    GRADED = "graded"
    NEEDS_REVIEW = "needs_review"


class UserProgress(Base):
    """Track user progress through modules"""
    __tablename__ = "user_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    module_id = Column(Integer, ForeignKey("modules.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Progress
    status = Column(SQLEnum(ProgressStatus), default=ProgressStatus.NOT_STARTED, nullable=False, index=True)
    completion_percentage = Column(Float, default=0.0, nullable=False)  # 0-100
    
    # Timestamps
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    last_accessed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    # user = relationship("User", back_populates="progress")
    # module = relationship("Module", back_populates="user_progress")
    
    # Unique constraint
    __table_args__ = (
        UniqueConstraint('user_id', 'module_id', name='uq_user_module'),
    )
    
    def __repr__(self):
        return f"<UserProgress(user_id={self.user_id}, module_id={self.module_id}, status='{self.status}')>"


class QuizAttempt(Base):
    """Track quiz attempts and scores"""
    __tablename__ = "quiz_attempts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Results
    user_answer = Column(Text, nullable=True)
    is_correct = Column(Boolean, nullable=True)
    points_earned = Column(Integer, nullable=True)
    review_status = Column(SQLEnum(ReviewStatus), default=ReviewStatus.PENDING, nullable=False, index=True)
    
    # Grading (for manual grading)
    graded_by = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    feedback = Column(Text, nullable=True)
    partial_credit = Column(Boolean, default=False, nullable=False)
    graded_at = Column(DateTime(timezone=True), nullable=True)
    
    # Timing
    attempted_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    time_spent_seconds = Column(Integer, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    # user = relationship("User", back_populates="quiz_attempts", foreign_keys=[user_id])
    # assessment = relationship("Assessment", back_populates="quiz_attempts")
    # grader = relationship("User", foreign_keys=[graded_by])
    
    def __repr__(self):
        return f"<QuizAttempt(id={self.id}, user_id={self.user_id}, assessment_id={self.assessment_id}, score={self.points_earned})>"


