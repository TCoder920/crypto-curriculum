"""Module and lesson endpoints"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.backend.core.database import get_db
from app.backend.core.security import get_current_user
from app.backend.models.user import User
from app.backend.models.module import Module, Lesson
from app.backend.models.assessment import Assessment
from app.backend.schemas.module import (
    ModuleResponse,
    ModuleDetailResponse,
    ModuleListResponse,
    LessonResponse,
)

router = APIRouter()


@router.get("/modules", response_model=ModuleListResponse)
async def get_modules(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all published modules"""
    result = await db.execute(
        select(Module)
        .where(
            Module.is_published == True,
            Module.is_active == True
        )
        .order_by(Module.order_index)
    )
    modules = result.scalars().all()
    
    module_responses = [
        ModuleResponse(
            id=m.id,
            title=m.title,
            description=m.description,
            track=m.track,
            order_index=m.order_index,
            duration_hours=m.duration_hours,
            prerequisites=m.prerequisites,
            learning_objectives=m.learning_objectives,
            is_published=m.is_published,
        )
        for m in modules
    ]
    
    return ModuleListResponse(
        modules=module_responses,
        total=len(module_responses)
    )


@router.get("/modules/{module_id}", response_model=ModuleDetailResponse)
async def get_module_detail(
    module_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get module details with lessons"""
    result = await db.execute(
        select(Module)
        .options(selectinload(Module.lessons))
        .where(Module.id == module_id)
    )
    module = result.scalar_one_or_none()
    
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module not found"
        )
    
    if not module.is_published:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Module is not published"
        )
    
    # Check if module has assessments
    assessment_result = await db.execute(
        select(func.count(Assessment.id))
        .where(
            Assessment.module_id == module_id,
            Assessment.is_active == True
        )
    )
    has_assessment = assessment_result.scalar() > 0
    
    # Get lessons ordered by order_index
    lessons = sorted(module.lessons, key=lambda l: l.order_index)
    
    lesson_responses = [
        LessonResponse(
            id=lesson.id,
            module_id=lesson.module_id,
            title=lesson.title,
            content=lesson.content,
            order_index=lesson.order_index,
            estimated_minutes=lesson.estimated_minutes,
            lesson_type=lesson.lesson_type,
        )
        for lesson in lessons
        if lesson.is_active
    ]
    
    return ModuleDetailResponse(
        id=module.id,
        title=module.title,
        description=module.description,
        track=module.track,
        order_index=module.order_index,
        duration_hours=module.duration_hours,
        prerequisites=module.prerequisites,
        learning_objectives=module.learning_objectives,
        lessons=lesson_responses,
        has_assessment=has_assessment,
    )


@router.get("/modules/{module_id}/lessons", response_model=List[LessonResponse])
async def get_module_lessons(
    module_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all lessons for a module"""
    # Verify module exists and is published
    result = await db.execute(select(Module).where(Module.id == module_id))
    module = result.scalar_one_or_none()
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module not found"
        )
    
    if not module.is_published:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Module is not published"
        )
    
    # Get lessons
    result = await db.execute(
        select(Lesson)
        .where(
            Lesson.module_id == module_id,
            Lesson.is_active == True
        )
        .order_by(Lesson.order_index)
    )
    lessons = result.scalars().all()
    
    return [
        LessonResponse(
            id=lesson.id,
            module_id=lesson.module_id,
            title=lesson.title,
            content=lesson.content,
            order_index=lesson.order_index,
            estimated_minutes=lesson.estimated_minutes,
            lesson_type=lesson.lesson_type,
        )
        for lesson in lessons
    ]


@router.get("/lessons/{lesson_id}", response_model=LessonResponse)
async def get_lesson(
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific lesson"""
    result = await db.execute(
        select(Lesson)
        .where(Lesson.id == lesson_id)
    )
    lesson = result.scalar_one_or_none()
    
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )
    
    if not lesson.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson is not active"
        )
    
    return LessonResponse(
        id=lesson.id,
        module_id=lesson.module_id,
        title=lesson.title,
        content=lesson.content,
        order_index=lesson.order_index,
        estimated_minutes=lesson.estimated_minutes,
        lesson_type=lesson.lesson_type,
    )


