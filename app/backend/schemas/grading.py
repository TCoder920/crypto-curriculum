"""Grading schemas"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.backend.models.progress import ReviewStatus


class GradingQueueItem(BaseModel):
    """Schema for grading queue item"""
    attempt_id: int
    user_id: int
    user_name: str
    user_email: str
    assessment_id: int
    question_text: str
    question_type: str
    user_answer: Optional[str]
    correct_answer: str
    module_id: int
    module_title: str
    attempted_at: datetime
    time_spent_seconds: Optional[int]
    
    class Config:
        from_attributes = True


class GradingQueueResponse(BaseModel):
    """Schema for grading queue response"""
    items: List[GradingQueueItem]
    total: int


class GradeSubmission(BaseModel):
    """Schema for submitting a grade"""
    is_correct: bool
    points_earned: int = Field(..., ge=0, description="Points awarded")
    feedback: Optional[str] = None
    partial_credit: bool = False


class GradedAttemptResponse(BaseModel):
    """Schema for graded attempt response"""
    id: int
    user_id: int
    assessment_id: int
    user_answer: Optional[str]
    is_correct: bool
    points_earned: int
    review_status: ReviewStatus
    graded_by: Optional[int]
    feedback: Optional[str]
    partial_credit: bool
    graded_at: Optional[datetime]
    attempted_at: datetime
    
    class Config:
        from_attributes = True


class GradingHistoryResponse(BaseModel):
    """Schema for grading history response"""
    items: List[GradedAttemptResponse]
    total: int

