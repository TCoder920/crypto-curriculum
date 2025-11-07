"""Assessment and Quiz models"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DateTime, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.backend.core.database import Base
import enum


class QuestionType(str, enum.Enum):
    """Question type enumeration"""
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"
    CODING_TASK = "coding_task"


class Assessment(Base):
    """Assessment/quiz question for a module"""
    __tablename__ = "assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Content
    question_text = Column(Text, nullable=False)
    question_type = Column(SQLEnum(QuestionType), nullable=False, index=True)
    order_index = Column(Integer, nullable=False)
    points = Column(Integer, default=10, nullable=False)
    
    # Options (for multiple choice)
    options = Column(JSON, nullable=True)  # {"A": "...", "B": "...", "C": "...", "D": "..."}
    correct_answer = Column(Text, nullable=False)  # "A" or full text answer
    explanation = Column(Text, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    module = relationship("Module", back_populates="assessments")
    # quiz_attempts = relationship("QuizAttempt", back_populates="assessment")
    
    def __repr__(self):
        return f"<Assessment(id={self.id}, type='{self.question_type}', module_id={self.module_id})>"


