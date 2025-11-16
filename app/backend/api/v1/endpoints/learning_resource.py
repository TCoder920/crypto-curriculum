"""Learning resource endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import List, Optional
from pydantic import BaseModel, HttpUrl

from app.backend.core.database import get_db
from app.backend.core.security import get_current_user
from app.backend.api.v1.endpoints.auth import require_role
from app.backend.models.user import User, UserRole
from app.backend.models.notification import LearningResource
from app.backend.models.module import Module

router = APIRouter()


class LearningResourceCreate(BaseModel):
    """Create learning resource request"""
    title: str
    url: str
    resource_type: Optional[str] = None  # 'video', 'article', 'tutorial', 'documentation'
    difficulty: Optional[str] = None  # 'beginner', 'intermediate', 'advanced'
    module_id: Optional[int] = None


class LearningResourceResponse(BaseModel):
    """Learning resource response"""
    id: int
    title: str
    url: str
    resource_type: Optional[str]
    difficulty: Optional[str]
    upvotes: int
    module_id: Optional[int]
    module_title: Optional[str] = None
    added_by: Optional[int]
    created_at: str
    
    class Config:
        from_attributes = True


class LearningResourceUpdate(BaseModel):
    """Update learning resource request"""
    title: Optional[str] = None
    url: Optional[str] = None
    resource_type: Optional[str] = None
    difficulty: Optional[str] = None


@router.get("/learning-resources", response_model=List[LearningResourceResponse])
async def list_learning_resources(
    module_id: Optional[int] = None,
    resource_type: Optional[str] = None,
    difficulty: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List learning resources with optional filters"""
    query = select(LearningResource)
    
    if module_id:
        query = query.where(LearningResource.module_id == module_id)
    if resource_type:
        query = query.where(LearningResource.resource_type == resource_type)
    if difficulty:
        query = query.where(LearningResource.difficulty == difficulty)
    
    query = query.order_by(LearningResource.upvotes.desc(), LearningResource.created_at.desc())
    
    result = await db.execute(query)
    resources = result.scalars().all()
    
    # Get module titles for resources with module_id
    module_ids = {r.module_id for r in resources if r.module_id}
    module_titles = {}
    if module_ids:
        result = await db.execute(select(Module.id, Module.title).where(Module.id.in_(module_ids)))
        module_titles = {row[0]: row[1] for row in result.all()}
    
    return [
        LearningResourceResponse(
            id=r.id,
            title=r.title,
            url=r.url,
            resource_type=r.resource_type,
            difficulty=r.difficulty,
            upvotes=r.upvotes,
            module_id=r.module_id,
            module_title=module_titles.get(r.module_id) if r.module_id else None,
            added_by=r.added_by,
            created_at=r.created_at.isoformat()
        )
        for r in resources
    ]


@router.post("/learning-resources", response_model=LearningResourceResponse, status_code=status.HTTP_201_CREATED)
async def create_learning_resource(
    resource: LearningResourceCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new learning resource (instructors can add to any module, students can add general resources)"""
    # Verify module exists if module_id provided
    if resource.module_id:
        result = await db.execute(select(Module).where(Module.id == resource.module_id))
        module = result.scalar_one_or_none()
        if not module:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Module not found"
            )
        
        # Only instructors can add resources to specific modules
        if current_user.role not in [UserRole.INSTRUCTOR, UserRole.ADMIN]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only instructors can add resources to specific modules"
            )
    
    # Create resource
    learning_resource = LearningResource(
        title=resource.title,
        url=resource.url,
        resource_type=resource.resource_type,
        difficulty=resource.difficulty,
        module_id=resource.module_id,
        added_by=current_user.id
    )
    
    db.add(learning_resource)
    await db.commit()
    await db.refresh(learning_resource)
    
    # Get module title if applicable
    module_title = None
    if learning_resource.module_id:
        result = await db.execute(select(Module.title).where(Module.id == learning_resource.module_id))
        module_title = result.scalar_one_or_none()
    
    return LearningResourceResponse(
        id=learning_resource.id,
        title=learning_resource.title,
        url=learning_resource.url,
        resource_type=learning_resource.resource_type,
        difficulty=learning_resource.difficulty,
        upvotes=learning_resource.upvotes,
        module_id=learning_resource.module_id,
        module_title=module_title,
        added_by=learning_resource.added_by,
        created_at=learning_resource.created_at.isoformat()
    )


@router.get("/learning-resources/{resource_id}", response_model=LearningResourceResponse)
async def get_learning_resource(
    resource_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific learning resource"""
    result = await db.execute(select(LearningResource).where(LearningResource.id == resource_id))
    resource = result.scalar_one_or_none()
    
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning resource not found"
        )
    
    # Get module title if applicable
    module_title = None
    if resource.module_id:
        result = await db.execute(select(Module.title).where(Module.id == resource.module_id))
        module_title = result.scalar_one_or_none()
    
    return LearningResourceResponse(
        id=resource.id,
        title=resource.title,
        url=resource.url,
        resource_type=resource.resource_type,
        difficulty=resource.difficulty,
        upvotes=resource.upvotes,
        module_id=resource.module_id,
        module_title=module_title,
        added_by=resource.added_by,
        created_at=resource.created_at.isoformat()
    )


@router.put("/learning-resources/{resource_id}", response_model=LearningResourceResponse)
async def update_learning_resource(
    resource_id: int,
    resource_update: LearningResourceUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a learning resource (only creator or instructor/admin)"""
    result = await db.execute(select(LearningResource).where(LearningResource.id == resource_id))
    resource = result.scalar_one_or_none()
    
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning resource not found"
        )
    
    # Check permissions
    if resource.added_by != current_user.id and current_user.role not in [UserRole.INSTRUCTOR, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this resource"
        )
    
    # Update fields
    if resource_update.title is not None:
        resource.title = resource_update.title
    if resource_update.url is not None:
        resource.url = resource_update.url
    if resource_update.resource_type is not None:
        resource.resource_type = resource_update.resource_type
    if resource_update.difficulty is not None:
        resource.difficulty = resource_update.difficulty
    
    await db.commit()
    await db.refresh(resource)
    
    # Get module title if applicable
    module_title = None
    if resource.module_id:
        result = await db.execute(select(Module.title).where(Module.id == resource.module_id))
        module_title = result.scalar_one_or_none()
    
    return LearningResourceResponse(
        id=resource.id,
        title=resource.title,
        url=resource.url,
        resource_type=resource.resource_type,
        difficulty=resource.difficulty,
        upvotes=resource.upvotes,
        module_id=resource.module_id,
        module_title=module_title,
        added_by=resource.added_by,
        created_at=resource.created_at.isoformat()
    )


@router.post("/learning-resources/{resource_id}/upvote", response_model=LearningResourceResponse)
async def upvote_learning_resource(
    resource_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Upvote a learning resource"""
    result = await db.execute(select(LearningResource).where(LearningResource.id == resource_id))
    resource = result.scalar_one_or_none()
    
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning resource not found"
        )
    
    resource.upvotes += 1
    await db.commit()
    await db.refresh(resource)
    
    # Get module title if applicable
    module_title = None
    if resource.module_id:
        result = await db.execute(select(Module.title).where(Module.id == resource.module_id))
        module_title = result.scalar_one_or_none()
    
    return LearningResourceResponse(
        id=resource.id,
        title=resource.title,
        url=resource.url,
        resource_type=resource.resource_type,
        difficulty=resource.difficulty,
        upvotes=resource.upvotes,
        module_id=resource.module_id,
        module_title=module_title,
        added_by=resource.added_by,
        created_at=resource.created_at.isoformat()
    )


@router.delete("/learning-resources/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_learning_resource(
    resource_id: int,
    current_user: User = Depends(require_role([UserRole.INSTRUCTOR, UserRole.ADMIN])),
    db: AsyncSession = Depends(get_db)
):
    """Delete a learning resource (instructor/admin only)"""
    result = await db.execute(select(LearningResource).where(LearningResource.id == resource_id))
    resource = result.scalar_one_or_none()
    
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning resource not found"
        )
    
    await db.delete(resource)
    await db.commit()
    
    return None

