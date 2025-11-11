"""Module and lesson schemas"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.backend.models.module import Track


class LessonResponse(BaseModel):
    """Lesson response schema"""
    id: int
    module_id: int
    title: str
    content: str
    order_index: int
    estimated_minutes: Optional[int]
    lesson_type: str
    
    class Config:
        from_attributes = True


class ModuleResponse(BaseModel):
    """Module response schema"""
    id: int
    title: str
    description: Optional[str]
    track: Track
    order_index: int
    duration_hours: float
    prerequisites: Optional[List[int]]
    learning_objectives: Optional[List[str]]
    is_published: bool
    
    class Config:
        from_attributes = True


class ModuleDetailResponse(BaseModel):
    """Module detail with lessons"""
    id: int
    title: str
    description: Optional[str]
    track: Track
    order_index: int
    duration_hours: float
    prerequisites: Optional[List[int]]
    learning_objectives: Optional[List[str]]
    lessons: List[LessonResponse]
    has_assessment: bool = False  # Whether module has assessments
    
    class Config:
        from_attributes = True


class ModuleListResponse(BaseModel):
    """List of modules"""
    modules: List[ModuleResponse]
    total: int


