"""Progress tracking schemas"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.backend.models.progress import ProgressStatus


class ProgressBase(BaseModel):
    """Base progress schema"""
    status: ProgressStatus
    completion_percentage: float = Field(..., ge=0.0, le=100.0)


class ProgressCreate(ProgressBase):
    """Progress creation schema"""
    module_id: int


class ProgressUpdate(BaseModel):
    """Progress update schema"""
    status: Optional[ProgressStatus] = None
    completion_percentage: Optional[float] = Field(None, ge=0.0, le=100.0)


class ProgressResponse(ProgressBase):
    """Progress response schema"""
    id: int
    user_id: int
    module_id: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    last_accessed_at: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ProgressListResponse(BaseModel):
    """List of user progress"""
    progress: list[ProgressResponse]
    total: int

