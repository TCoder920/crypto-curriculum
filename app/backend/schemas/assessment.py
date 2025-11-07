"""Assessment schemas"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime
from app.backend.models.assessment import QuestionType
from app.backend.models.progress import ReviewStatus


class AssessmentResponse(BaseModel):
    """Assessment question response schema"""
    id: int
    module_id: int
    question_text: str
    question_type: QuestionType
    order_index: int
    points: int
    options: Optional[Dict[str, str]] = None  # For multiple choice
    explanation: Optional[str] = None
    
    class Config:
        from_attributes = True


class AssessmentSubmit(BaseModel):
    """Submit answer to assessment"""
    user_answer: str = Field(..., description="User's answer")
    time_spent_seconds: Optional[int] = Field(None, ge=0, description="Time spent on question in seconds")


class AssessmentSubmitResponse(BaseModel):
    """Response after submitting assessment answer"""
    attempt_id: int
    is_correct: Optional[bool] = None  # None for short answer until graded
    points_earned: Optional[int] = None
    review_status: ReviewStatus
    explanation: Optional[str] = None
    correct_answer: Optional[str] = None  # Only shown after grading or for auto-graded


class QuizAttemptResponse(BaseModel):
    """Individual quiz attempt response"""
    attempt_id: int
    assessment_id: int
    question_text: str
    question_type: QuestionType
    user_answer: Optional[str]
    is_correct: Optional[bool]
    points_earned: Optional[int]
    review_status: ReviewStatus
    feedback: Optional[str] = None
    attempted_at: datetime
    
    class Config:
        from_attributes = True


class ModuleResultsResponse(BaseModel):
    """Module assessment results summary"""
    module_id: int
    module_title: str
    total_questions: int
    attempted: int
    correct: int
    pending_review: int
    score_percent: float
    points_earned: int
    points_possible: int
    attempts: List[QuizAttemptResponse]
    can_progress: bool = Field(..., description="True if score >= 70% and all questions attempted")
    best_score_percent: Optional[float] = None
    attempt_count: int = Field(..., description="Number of times user has taken this assessment")


class AssessmentListResponse(BaseModel):
    """List of assessments for a module"""
    module_id: int
    module_title: str
    assessments: List[AssessmentResponse]
    total_points: int
    estimated_time_minutes: int = Field(default=30, description="Estimated time to complete")

