"""Module and Lesson endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload
from typing import List, Optional
from math import ceil

from app.backend.core.database import get_db
from app.backend.api.v1.endpoints.auth import get_current_active_user
from app.backend.models.module import Module, Lesson
from app.backend.models.user import User
from app.backend.models.progress import UserProgress, ProgressStatus
from app.backend.schemas.module import (
    ModuleResponse,
    ModuleDetailResponse,
    ModuleListResponse,
    LessonResponse,
)

router = APIRouter()


async def check_prerequisites(
    module: Module,
    user_id: int,
    db: AsyncSession
) -> tuple[bool, List[int]]:
    """Check if user has completed prerequisites for a module"""
    if not module.prerequisites:
        return True, []
    
    # Get user's completed modules
    result = await db.execute(
        select(UserProgress.module_id).where(
            and_(
                UserProgress.user_id == user_id,
                UserProgress.status == ProgressStatus.COMPLETED
            )
        )
    )
    completed_module_ids = {row[0] for row in result.all()}
    
    # Check if all prerequisites are completed
    missing_prerequisites = [
        prereq_id for prereq_id in module.prerequisites
        if prereq_id not in completed_module_ids
    ]
    
    return len(missing_prerequisites) == 0, missing_prerequisites


@router.get("/", response_model=ModuleListResponse)
async def list_modules(
    track: Optional[str] = Query(None, description="Filter by track"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """List all modules with optional filtering"""
    # Build query
    query = select(Module).where(Module.is_active == True)
    
    if track:
        query = query.where(Module.track == track)
    
    # Get total count
    count_query = select(func.count()).select_from(Module).where(Module.is_active == True)
    if track:
        count_query = count_query.where(Module.track == track)
    
    total_result = await db.execute(count_query)
    total = total_result.scalar_one()
    
    # Apply pagination
    offset = (page - 1) * page_size
    query = query.order_by(Module.order_index).offset(offset).limit(page_size)
    
    # Execute query
    result = await db.execute(query)
    modules = result.scalars().all()
    
    # Check prerequisites for each module
    modules_with_prereqs = []
    for module in modules:
        can_access, missing = await check_prerequisites(module, current_user.id, db)
        module_dict = {
            **ModuleResponse.model_validate(module).model_dump(),
            "can_access": can_access,
            "missing_prerequisites": missing if not can_access else []
        }
        modules_with_prereqs.append(module_dict)
    
    total_pages = ceil(total / page_size) if total > 0 else 0
    
    return {
        "modules": modules_with_prereqs,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }


@router.get("/{module_id}", response_model=ModuleDetailResponse)
async def get_module(
    module_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get module details with lessons"""
    # Get module with lessons
    result = await db.execute(
        select(Module)
        .options(selectinload(Module.lessons))
        .where(and_(Module.id == module_id, Module.is_active == True))
    )
    module = result.scalar_one_or_none()
    
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Module {module_id} not found"
        )
    
    # Check prerequisites
    can_access, missing_prereqs = await check_prerequisites(module, current_user.id, db)
    
    # Get lessons (sorted by order_index)
    lessons = sorted(module.lessons, key=lambda l: l.order_index) if module.lessons else []
    
    # Build response
    module_data = ModuleDetailResponse.model_validate(module)
    module_data.lessons = [LessonResponse.model_validate(lesson) for lesson in lessons]
    
    # Add prerequisite info
    response_dict = module_data.model_dump()
    response_dict["can_access"] = can_access
    response_dict["missing_prerequisites"] = missing_prereqs if not can_access else []
    
    return response_dict


@router.get("/{module_id}/lessons", response_model=List[LessonResponse])
async def get_module_lessons(
    module_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all lessons for a module"""
    # Verify module exists
    result = await db.execute(
        select(Module).where(and_(Module.id == module_id, Module.is_active == True))
    )
    module = result.scalar_one_or_none()
    
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Module {module_id} not found"
        )
    
    # Check prerequisites
    can_access, missing_prereqs = await check_prerequisites(module, current_user.id, db)
    
    if not can_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Module {module_id} requires completion of modules: {missing_prereqs}"
        )
    
    # Get lessons
    result = await db.execute(
        select(Lesson)
        .where(and_(Lesson.module_id == module_id, Lesson.is_active == True))
        .order_by(Lesson.order_index)
    )
    lessons = result.scalars().all()
    
    return [LessonResponse.model_validate(lesson) for lesson in lessons]


@router.get("/lessons/{lesson_id}", response_model=LessonResponse)
async def get_lesson(
    lesson_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get lesson content"""
    # Get lesson with module
    result = await db.execute(
        select(Lesson)
        .options(selectinload(Lesson.module))
        .where(and_(Lesson.id == lesson_id, Lesson.is_active == True))
    )
    lesson = result.scalar_one_or_none()
    
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lesson {lesson_id} not found"
        )
    
    # Check module prerequisites
    can_access, missing_prereqs = await check_prerequisites(lesson.module, current_user.id, db)
    
    if not can_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Module {lesson.module_id} requires completion of modules: {missing_prereqs}"
        )
    
    return LessonResponse.model_validate(lesson)

