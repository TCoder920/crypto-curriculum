"""Module and Lesson schemas"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.backend.models.module import Track


class LessonBase(BaseModel):
    """Base lesson schema"""
    title: str = Field(..., max_length=255)
    content: str
    order_index: int
    estimated_minutes: Optional[int] = None
    lesson_type: str = Field(default="reading", max_length=50)
    media_url: Optional[str] = Field(None, max_length=500)
    is_active: bool = True


class LessonCreate(LessonBase):
    """Lesson creation schema"""
    module_id: int


class LessonUpdate(BaseModel):
    """Lesson update schema"""
    title: Optional[str] = Field(None, max_length=255)
    content: Optional[str] = None
    order_index: Optional[int] = None
    estimated_minutes: Optional[int] = None
    lesson_type: Optional[str] = Field(None, max_length=50)
    media_url: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None


class LessonResponse(LessonBase):
    """Lesson response schema"""
    id: int
    module_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ModuleBase(BaseModel):
    """Base module schema"""
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    track: Track
    order_index: int
    duration_hours: float
    prerequisites: Optional[List[int]] = None
    learning_objectives: Optional[List[str]] = None
    is_active: bool = True
    is_published: bool = False


class ModuleCreate(ModuleBase):
    """Module creation schema"""
    pass


class ModuleUpdate(BaseModel):
    """Module update schema"""
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    track: Optional[Track] = None
    order_index: Optional[int] = None
    duration_hours: Optional[float] = None
    prerequisites: Optional[List[int]] = None
    learning_objectives: Optional[List[str]] = None
    is_active: Optional[bool] = None
    is_published: Optional[bool] = None


class ModuleResponse(ModuleBase):
    """Module response schema"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ModuleDetailResponse(ModuleResponse):
    """Module detail response with lessons"""
    lessons: List[LessonResponse] = []
    can_access: Optional[bool] = None
    missing_prerequisites: Optional[List[int]] = None


class ModuleListResponse(BaseModel):
    """Module list response with pagination"""
    modules: List[dict]  # Can include extra fields like can_access, missing_prerequisites
    total: int
    page: int
    page_size: int
    total_pages: int

