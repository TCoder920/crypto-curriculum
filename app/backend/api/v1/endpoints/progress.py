"""Progress tracking endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from datetime import datetime

from app.backend.core.database import get_db
from app.backend.api.v1.endpoints.auth import get_current_active_user
from app.backend.models.user import User
from app.backend.models.module import Module
from app.backend.models.progress import UserProgress, ProgressStatus
from app.backend.schemas.progress import (
    ProgressResponse,
    ProgressUpdate,
    ProgressListResponse,
)

router = APIRouter()


@router.get("/", response_model=ProgressListResponse)
async def get_user_progress(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all progress for current user"""
    result = await db.execute(
        select(UserProgress).where(UserProgress.user_id == current_user.id)
    )
    progress_records = result.scalars().all()
    
    return ProgressListResponse(
        progress=[ProgressResponse.model_validate(p) for p in progress_records],
        total=len(progress_records)
    )


@router.get("/{module_id}", response_model=ProgressResponse)
async def get_module_progress(
    module_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get progress for a specific module (returns 404 if not found)"""
    result = await db.execute(
        select(UserProgress).where(
            and_(
                UserProgress.user_id == current_user.id,
                UserProgress.module_id == module_id
            )
        )
    )
    progress = result.scalar_one_or_none()
    
    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Progress not found for module {module_id}"
        )
    
    return ProgressResponse.model_validate(progress)


@router.post("/start/{module_id}", response_model=ProgressResponse)
async def start_module(
    module_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Mark a module as started"""
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
    
    # Check if progress already exists
    result = await db.execute(
        select(UserProgress).where(
            and_(
                UserProgress.user_id == current_user.id,
                UserProgress.module_id == module_id
            )
        )
    )
    progress = result.scalar_one_or_none()
    
    if progress:
        # Update existing progress
        if progress.status == ProgressStatus.NOT_STARTED:
            progress.status = ProgressStatus.IN_PROGRESS
            progress.started_at = datetime.utcnow()
        progress.last_accessed_at = datetime.utcnow()
    else:
        # Create new progress
        progress = UserProgress(
            user_id=current_user.id,
            module_id=module_id,
            status=ProgressStatus.IN_PROGRESS,
            completion_percentage=0.0,
            started_at=datetime.utcnow(),
            last_accessed_at=datetime.utcnow(),
        )
        db.add(progress)
    
    await db.commit()
    await db.refresh(progress)
    
    return ProgressResponse.model_validate(progress)


@router.post("/complete/{module_id}", response_model=ProgressResponse)
async def complete_module(
    module_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Mark a module as completed"""
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
    
    # Get or create progress
    result = await db.execute(
        select(UserProgress).where(
            and_(
                UserProgress.user_id == current_user.id,
                UserProgress.module_id == module_id
            )
        )
    )
    progress = result.scalar_one_or_none()
    
    if progress:
        # Update existing progress
        progress.status = ProgressStatus.COMPLETED
        progress.completion_percentage = 100.0
        if not progress.started_at:
            progress.started_at = datetime.utcnow()
        progress.completed_at = datetime.utcnow()
        progress.last_accessed_at = datetime.utcnow()
    else:
        # Create new progress as completed
        progress = UserProgress(
            user_id=current_user.id,
            module_id=module_id,
            status=ProgressStatus.COMPLETED,
            completion_percentage=100.0,
            started_at=datetime.utcnow(),
            completed_at=datetime.utcnow(),
            last_accessed_at=datetime.utcnow(),
        )
        db.add(progress)
    
    await db.commit()
    await db.refresh(progress)
    
    return ProgressResponse.model_validate(progress)


@router.patch("/{module_id}", response_model=ProgressResponse)
async def update_progress(
    module_id: int,
    progress_update: ProgressUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update progress for a module"""
    result = await db.execute(
        select(UserProgress).where(
            and_(
                UserProgress.user_id == current_user.id,
                UserProgress.module_id == module_id
            )
        )
    )
    progress = result.scalar_one_or_none()
    
    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Progress not found for module {module_id}"
        )
    
    # Update fields
    if progress_update.status is not None:
        progress.status = progress_update.status
        if progress_update.status == ProgressStatus.COMPLETED and not progress.completed_at:
            progress.completed_at = datetime.utcnow()
            progress.completion_percentage = 100.0
        elif progress_update.status == ProgressStatus.IN_PROGRESS and not progress.started_at:
            progress.started_at = datetime.utcnow()
    
    if progress_update.completion_percentage is not None:
        progress.completion_percentage = progress_update.completion_percentage
        if progress.completion_percentage >= 100.0:
            progress.status = ProgressStatus.COMPLETED
            if not progress.completed_at:
                progress.completed_at = datetime.utcnow()
    
    progress.last_accessed_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(progress)
    
    return ProgressResponse.model_validate(progress)

