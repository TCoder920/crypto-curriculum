"""Cohort management endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_, text, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from datetime import datetime, date, timedelta
import logging

from app.backend.core.database import get_db
from app.backend.core.security import get_current_user
from app.backend.models.user import User, UserRole
from app.backend.models.cohort import Cohort, CohortMember, CohortRole
from app.backend.schemas.cohort import (
    CohortCreate,
    CohortUpdate,
    CohortResponse,
    CohortListResponse,
    CohortMemberCreate,
    CohortMemberResponse
)
from app.backend.api.v1.endpoints.auth import require_role

router = APIRouter()
logger = logging.getLogger(__name__)


def calculate_is_active(start_date: Optional[date], end_date: Optional[date]) -> bool:
    """Calculate if cohort is active based on dates"""
    if start_date is None and end_date is None:
        return True  # No dates set, default to active
    
    today = date.today()
    
    # If only start_date is set, check if today >= start_date
    if start_date is not None and end_date is None:
        return today >= start_date
    
    # If only end_date is set, check if today <= end_date
    if start_date is None and end_date is not None:
        return today <= end_date
    
    # Both dates set, check if today is between them
    return start_date <= today <= end_date


@router.post("/cohorts", response_model=CohortResponse, status_code=status.HTTP_201_CREATED)
async def create_cohort(
    cohort_data: CohortCreate,
    current_user: User = Depends(require_role([UserRole.INSTRUCTOR, UserRole.ADMIN])),
    db: AsyncSession = Depends(get_db)
):
    """Create a new cohort (instructor/admin only)"""
    try:
        # Calculate is_active based on dates (override user input)
        calculated_is_active = calculate_is_active(cohort_data.start_date, cohort_data.end_date)
        
        new_cohort = Cohort(
            name=cohort_data.name,
            description=cohort_data.description,
            start_date=cohort_data.start_date,
            end_date=cohort_data.end_date,
            is_active=calculated_is_active,
            created_by=current_user.id
        )
        
        db.add(new_cohort)
        await db.commit()
        await db.refresh(new_cohort)
    except Exception as e:
        await db.rollback()
        logger.error(f"Error creating cohort: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating cohort: {str(e)}"
        )
    
    # Add creator as instructor member (check if already exists)
    try:
        existing_member = await db.execute(
            select(CohortMember)
            .where(
                and_(
                    CohortMember.cohort_id == new_cohort.id,
                    CohortMember.user_id == current_user.id
                )
            )
        )
        if not existing_member.scalar_one_or_none():
            creator_member = CohortMember(
                cohort_id=new_cohort.id,
                user_id=current_user.id,
                role=CohortRole.INSTRUCTOR.value
            )
            db.add(creator_member)
            await db.commit()
    except IntegrityError as e:
        await db.rollback()
        error_str = str(e)
        if 'cohort_members_pkey' in error_str or 'duplicate key' in error_str.lower():
            # Primary key sequence is out of sync - try to fix it
            try:
                # Fix the sequence using raw SQL
                await db.execute(
                    text(
                        "SELECT setval('cohort_members_id_seq', "
                        "(SELECT COALESCE(MAX(id), 0) FROM cohort_members) + 1, false)"
                    )
                )
                await db.commit()
                logger.warning(f"Fixed sequence for cohort_members after duplicate key error")
                
                # Try adding member again
                existing_member = await db.execute(
                    select(CohortMember)
                    .where(
                        and_(
                            CohortMember.cohort_id == new_cohort.id,
                            CohortMember.user_id == current_user.id
                        )
                    )
                )
                if not existing_member.scalar_one_or_none():
                    creator_member = CohortMember(
                        cohort_id=new_cohort.id,
                        user_id=current_user.id,
                        role=CohortRole.INSTRUCTOR.value
                    )
                    db.add(creator_member)
                    await db.commit()
            except Exception as fix_error:
                await db.rollback()
                logger.error(f"Error fixing sequence: {str(fix_error)}", exc_info=True)
        else:
            logger.warning(f"Creator already a member or constraint violation: {error_str}")
            # If it's a unique constraint violation, the user is already a member
            # This is fine - just continue
    except Exception as e:
        await db.rollback()
        logger.error(f"Error adding creator as member: {str(e)}", exc_info=True)
        # If member addition fails, we can still return the cohort (it's created)
        # Just log the error and continue
    
    # Fetch cohort with members
    result = await db.execute(
        select(Cohort)
        .where(Cohort.id == new_cohort.id)
    )
    cohort = result.scalar_one()
    
    # Get members
    members_result = await db.execute(
        select(CohortMember)
        .where(CohortMember.cohort_id == cohort.id)
    )
    members = members_result.scalars().all()
    
    # Get user details for members
    member_responses = []
    for member in members:
        user_result = await db.execute(select(User).where(User.id == member.user_id))
        user = user_result.scalar_one_or_none()
        member_data = {
            "id": member.id,
            "cohort_id": member.cohort_id,
            "user_id": member.user_id,
            "role": member.role,
            "joined_at": member.joined_at,
            "user": {
                "id": user.id if user else None,
                "email": user.email if user else None,
                "full_name": user.full_name if user else None,
                "username": user.username if user else None
            } if user else None
        }
        member_responses.append(CohortMemberResponse(**member_data))
    
    # Recalculate is_active based on dates
    calculated_is_active = calculate_is_active(cohort.start_date, cohort.end_date)
    
    # Update database if status changed
    if calculated_is_active != cohort.is_active:
        cohort.is_active = calculated_is_active
        await db.commit()
        await db.refresh(cohort)
    
    return CohortResponse(
        id=cohort.id,
        name=cohort.name,
        description=cohort.description,
        start_date=cohort.start_date,
        end_date=cohort.end_date,
        is_active=calculated_is_active,
        cancelled_at=cohort.cancelled_at,
        created_by=cohort.created_by,
        created_at=cohort.created_at,
        updated_at=cohort.updated_at,
        members=member_responses,
        member_count=len(member_responses),
        student_count=sum(1 for m in member_responses if m.role == CohortRole.STUDENT.value),
        instructor_count=sum(1 for m in member_responses if m.role == CohortRole.INSTRUCTOR.value)
    )


@router.put("/cohorts/{cohort_id}", response_model=CohortResponse)
async def update_cohort(
    cohort_id: int,
    cohort_data: CohortUpdate,
    current_user: User = Depends(require_role([UserRole.INSTRUCTOR, UserRole.ADMIN])),
    db: AsyncSession = Depends(get_db)
):
    """Update a cohort (instructor/admin only)"""
    # Check if cohort exists
    result = await db.execute(select(Cohort).where(Cohort.id == cohort_id))
    cohort = result.scalar_one_or_none()
    
    if not cohort:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cohort not found"
        )
    
    try:
        # Update fields if provided
        if cohort_data.name is not None:
            cohort.name = cohort_data.name
        if cohort_data.description is not None:
            cohort.description = cohort_data.description
        if cohort_data.start_date is not None:
            cohort.start_date = cohort_data.start_date
        if cohort_data.end_date is not None:
            cohort.end_date = cohort_data.end_date
        
        # If is_active is explicitly set to False, mark as canceled/inactive
        # Otherwise, calculate based on dates
        if cohort_data.is_active is False:
            cohort.is_active = False
        else:
            # Recalculate is_active based on dates
            calculated_is_active = calculate_is_active(cohort.start_date, cohort.end_date)
            cohort.is_active = calculated_is_active
        
        await db.commit()
        await db.refresh(cohort)
    except Exception as e:
        await db.rollback()
        logger.error(f"Error updating cohort: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating cohort: {str(e)}"
        )
    
    # Get members
    members_result = await db.execute(
        select(CohortMember)
        .where(CohortMember.cohort_id == cohort.id)
    )
    members = members_result.scalars().all()
    
    # Get user details for members
    member_responses = []
    for member in members:
        user_result = await db.execute(select(User).where(User.id == member.user_id))
        user = user_result.scalar_one_or_none()
        member_data = {
            "id": member.id,
            "cohort_id": member.cohort_id,
            "user_id": member.user_id,
            "role": member.role,
            "joined_at": member.joined_at,
            "user": {
                "id": user.id if user else None,
                "email": user.email if user else None,
                "full_name": user.full_name if user else None,
                "username": user.username if user else None
            } if user else None
        }
        member_responses.append(CohortMemberResponse(**member_data))
    
    # Recalculate is_active based on dates
    calculated_is_active = calculate_is_active(cohort.start_date, cohort.end_date)
    
    # Update database if status changed (unless explicitly set to False)
    if cohort_data.is_active is not False and calculated_is_active != cohort.is_active:
        cohort.is_active = calculated_is_active
        await db.commit()
        await db.refresh(cohort)
    
    return CohortResponse(
        id=cohort.id,
        name=cohort.name,
        description=cohort.description,
        start_date=cohort.start_date,
        end_date=cohort.end_date,
        is_active=cohort.is_active,
        cancelled_at=cohort.cancelled_at,
        created_by=cohort.created_by,
        created_at=cohort.created_at,
        updated_at=cohort.updated_at,
        members=member_responses,
        member_count=len(member_responses),
        student_count=sum(1 for m in member_responses if m.role == CohortRole.STUDENT.value),
        instructor_count=sum(1 for m in member_responses if m.role == CohortRole.INSTRUCTOR.value)
    )


@router.patch("/cohorts/{cohort_id}/cancel", response_model=CohortResponse)
async def cancel_cohort(
    cohort_id: int,
    current_user: User = Depends(require_role([UserRole.INSTRUCTOR, UserRole.ADMIN])),
    db: AsyncSession = Depends(get_db)
):
    """Cancel a future or inactive cohort (instructor/admin only)"""
    # Check if cohort exists
    result = await db.execute(select(Cohort).where(Cohort.id == cohort_id))
    cohort = result.scalar_one_or_none()
    
    if not cohort:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cohort not found"
        )
    
    # Only allow canceling future or inactive cohorts
    today = date.today()
    is_future = (cohort.start_date is not None and cohort.start_date > today) or \
                (cohort.start_date is None and cohort.end_date is not None and cohort.end_date > today)
    
    if not is_future and cohort.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot cancel an active cohort. Only future or inactive cohorts can be canceled."
        )
    
    try:
        cohort.is_active = False
        cohort.cancelled_at = datetime.now()
        await db.commit()
        await db.refresh(cohort)
    except Exception as e:
        await db.rollback()
        logger.error(f"Error canceling cohort: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error canceling cohort: {str(e)}"
        )
    
    # Get members
    members_result = await db.execute(
        select(CohortMember)
        .where(CohortMember.cohort_id == cohort.id)
    )
    members = members_result.scalars().all()
    
    # Get user details for members
    member_responses = []
    for member in members:
        user_result = await db.execute(select(User).where(User.id == member.user_id))
        user = user_result.scalar_one_or_none()
        member_data = {
            "id": member.id,
            "cohort_id": member.cohort_id,
            "user_id": member.user_id,
            "role": member.role,
            "joined_at": member.joined_at,
            "user": {
                "id": user.id if user else None,
                "email": user.email if user else None,
                "full_name": user.full_name if user else None,
                "username": user.username if user else None
            } if user else None
        }
        member_responses.append(CohortMemberResponse(**member_data))
    
    return CohortResponse(
        id=cohort.id,
        name=cohort.name,
        description=cohort.description,
        start_date=cohort.start_date,
        end_date=cohort.end_date,
        is_active=False,
        cancelled_at=cohort.cancelled_at,
        created_by=cohort.created_by,
        created_at=cohort.created_at,
        updated_at=cohort.updated_at,
        members=member_responses,
        member_count=len(member_responses),
        student_count=sum(1 for m in member_responses if m.role == CohortRole.STUDENT.value),
        instructor_count=sum(1 for m in member_responses if m.role == CohortRole.INSTRUCTOR.value)
    )


@router.delete("/cohorts/{cohort_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cohort(
    cohort_id: int,
    current_user: User = Depends(require_role([UserRole.INSTRUCTOR, UserRole.ADMIN])),
    db: AsyncSession = Depends(get_db)
):
    """Delete a cohort (instructor/admin only)
    
    Validation rules:
    - If no students assigned: can be deleted immediately
    - If students assigned: must be cancelled first, then wait 14 days after cancellation
    """
    # Check if cohort exists
    result = await db.execute(select(Cohort).where(Cohort.id == cohort_id))
    cohort = result.scalar_one_or_none()
    
    if not cohort:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cohort not found"
        )
    
    # Get members to check for students
    members_result = await db.execute(
        select(CohortMember)
        .where(CohortMember.cohort_id == cohort_id)
    )
    members = members_result.scalars().all()
    
    # Check if there are any students assigned
    student_count = sum(1 for m in members if m.role == CohortRole.STUDENT.value)
    
    # If students are assigned, enforce the 14-day rule
    if student_count > 0:
        # Must be cancelled first
        if cohort.cancelled_at is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot delete cohort with {student_count} student(s) assigned. Cancel the cohort first, then wait 14 days before deletion."
            )
        
        # Check if 14 days have passed since cancellation
        # Use timezone-aware datetime for comparison
        now = datetime.now(cohort.cancelled_at.tzinfo) if cohort.cancelled_at.tzinfo else datetime.now()
        days_since_cancellation = (now - cohort.cancelled_at).days
        if days_since_cancellation < 14:
            days_remaining = 14 - days_since_cancellation
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot delete cohort yet. Must wait {days_remaining} more day(s) after cancellation (14 days total required)."
            )
    
    # If no students assigned, can delete immediately (no need to check cancellation)
    try:
        # Delete the cohort (cascade will handle members, deadlines, announcements)
        await db.execute(delete(Cohort).where(Cohort.id == cohort_id))
        await db.commit()
        logger.info(f"Cohort {cohort_id} deleted by user {current_user.id}")
    except Exception as e:
        await db.rollback()
        logger.error(f"Error deleting cohort: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting cohort: {str(e)}"
        )
    
    return None


@router.get("/cohorts", response_model=CohortListResponse)
async def list_cohorts(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    active_only: bool = False
):
    """List all cohorts (instructors/admins see all, students see only their cohorts)"""
    # Students can only see cohorts they're members of
    if current_user.role == UserRole.STUDENT:
        # Get cohorts where user is a member
        members_result = await db.execute(
            select(CohortMember.cohort_id)
            .where(CohortMember.user_id == current_user.id)
        )
        cohort_ids = [row[0] for row in members_result.all()]
        
        if not cohort_ids:
            return CohortListResponse(cohorts=[], total=0)
        
        query = select(Cohort).where(Cohort.id.in_(cohort_ids))
    else:
        # Instructors and admins see all cohorts
        query = select(Cohort)
    
    if active_only:
        query = query.where(Cohort.is_active == True)
    
    result = await db.execute(query.order_by(Cohort.created_at.desc()))
    cohorts = result.scalars().all()
    
    cohort_responses = []
    for cohort in cohorts:
        # Get members
        members_result = await db.execute(
            select(CohortMember)
            .where(CohortMember.cohort_id == cohort.id)
        )
        members = members_result.scalars().all()
        
        # Get user details for members
        member_responses = []
        for member in members:
            user_result = await db.execute(select(User).where(User.id == member.user_id))
            user = user_result.scalar_one_or_none()
            member_data = {
                "id": member.id,
                "cohort_id": member.cohort_id,
                "user_id": member.user_id,
                "role": member.role,
                "joined_at": member.joined_at,
                "user": {
                    "id": user.id if user else None,
                    "email": user.email if user else None,
                    "full_name": user.full_name if user else None,
                    "username": user.username if user else None
                } if user else None
            }
            member_responses.append(CohortMemberResponse(**member_data))
        
        # Recalculate is_active based on dates
        calculated_is_active = calculate_is_active(cohort.start_date, cohort.end_date)
        
        # Update database if status changed
        if calculated_is_active != cohort.is_active:
            cohort.is_active = calculated_is_active
            await db.commit()
            await db.refresh(cohort)
        
        cohort_responses.append(CohortResponse(
            id=cohort.id,
            name=cohort.name,
            description=cohort.description,
            start_date=cohort.start_date,
            end_date=cohort.end_date,
            is_active=calculated_is_active,
            cancelled_at=cohort.cancelled_at,
            created_by=cohort.created_by,
            created_at=cohort.created_at,
            updated_at=cohort.updated_at,
            members=member_responses,
            member_count=len(member_responses),
            student_count=sum(1 for m in member_responses if m.role == CohortRole.STUDENT.value),
            instructor_count=sum(1 for m in member_responses if m.role == CohortRole.INSTRUCTOR.value)
        ))
    
    return CohortListResponse(cohorts=cohort_responses, total=len(cohort_responses))


@router.get("/cohorts/{cohort_id}", response_model=CohortResponse)
async def get_cohort(
    cohort_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get cohort details with members"""
    # Check if cohort exists
    result = await db.execute(select(Cohort).where(Cohort.id == cohort_id))
    cohort = result.scalar_one_or_none()
    
    if not cohort:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cohort not found"
        )
    
    # Check access: students can only see cohorts they're members of
    if current_user.role == UserRole.STUDENT:
        member_check = await db.execute(
            select(CohortMember)
            .where(
                and_(
                    CohortMember.cohort_id == cohort_id,
                    CohortMember.user_id == current_user.id
                )
            )
        )
        if not member_check.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. You are not a member of this cohort."
            )
    
    # Get members
    members_result = await db.execute(
        select(CohortMember)
        .where(CohortMember.cohort_id == cohort_id)
    )
    members = members_result.scalars().all()
    
    # Get user details for members
    member_responses = []
    for member in members:
        user_result = await db.execute(select(User).where(User.id == member.user_id))
        user = user_result.scalar_one_or_none()
        member_data = {
            "id": member.id,
            "cohort_id": member.cohort_id,
            "user_id": member.user_id,
            "role": member.role,
            "joined_at": member.joined_at,
            "user": {
                "id": user.id if user else None,
                "email": user.email if user else None,
                "full_name": user.full_name if user else None,
                "username": user.username if user else None
            } if user else None
        }
        member_responses.append(CohortMemberResponse(**member_data))
    
    # Recalculate is_active based on dates
    calculated_is_active = calculate_is_active(cohort.start_date, cohort.end_date)
    
    # Update database if status changed
    if calculated_is_active != cohort.is_active:
        cohort.is_active = calculated_is_active
        await db.commit()
        await db.refresh(cohort)
    
    return CohortResponse(
        id=cohort.id,
        name=cohort.name,
        description=cohort.description,
        start_date=cohort.start_date,
        end_date=cohort.end_date,
        is_active=calculated_is_active,
        cancelled_at=cohort.cancelled_at,
        created_by=cohort.created_by,
        created_at=cohort.created_at,
        updated_at=cohort.updated_at,
        members=member_responses,
        member_count=len(member_responses),
        student_count=sum(1 for m in member_responses if m.role == CohortRole.STUDENT.value),
        instructor_count=sum(1 for m in member_responses if m.role == CohortRole.INSTRUCTOR.value)
    )


@router.post("/cohorts/{cohort_id}/members", response_model=CohortMemberResponse, status_code=status.HTTP_201_CREATED)
async def add_cohort_member(
    cohort_id: int,
    member_data: CohortMemberCreate,
    current_user: User = Depends(require_role([UserRole.INSTRUCTOR, UserRole.ADMIN])),
    db: AsyncSession = Depends(get_db)
):
    """Add a member to a cohort (instructor/admin only)"""
    # Check if cohort exists
    result = await db.execute(select(Cohort).where(Cohort.id == cohort_id))
    cohort = result.scalar_one_or_none()
    
    if not cohort:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cohort not found"
        )
    
    # Check if user exists
    user_result = await db.execute(select(User).where(User.id == member_data.user_id))
    user = user_result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if user is already a member
    existing_member = await db.execute(
        select(CohortMember)
        .where(
            and_(
                CohortMember.cohort_id == cohort_id,
                CohortMember.user_id == member_data.user_id
            )
        )
    )
    if existing_member.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a member of this cohort"
        )
    
    # Create new member
    new_member = CohortMember(
        cohort_id=cohort_id,
        user_id=member_data.user_id,
        role=member_data.role.value
    )
    
    db.add(new_member)
    await db.commit()
    await db.refresh(new_member)
    
    return CohortMemberResponse(
        id=new_member.id,
        cohort_id=new_member.cohort_id,
        user_id=new_member.user_id,
        role=new_member.role,
        joined_at=new_member.joined_at,
        user={
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "username": user.username
        } if user else None
    )


@router.delete("/cohorts/{cohort_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_cohort_member(
    cohort_id: int,
    user_id: int,
    current_user: User = Depends(require_role([UserRole.INSTRUCTOR, UserRole.ADMIN])),
    db: AsyncSession = Depends(get_db)
):
    """Remove a member from a cohort (instructor/admin only)"""
    # Check if cohort exists
    result = await db.execute(select(Cohort).where(Cohort.id == cohort_id))
    cohort = result.scalar_one_or_none()
    
    if not cohort:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cohort not found"
        )
    
    # Find member
    member_result = await db.execute(
        select(CohortMember)
        .where(
            and_(
                CohortMember.cohort_id == cohort_id,
                CohortMember.user_id == user_id
            )
        )
    )
    member = member_result.scalar_one_or_none()
    
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found in this cohort"
        )
    
    # Prevent removing the last instructor
    if member.role == CohortRole.INSTRUCTOR.value:
        instructor_count = await db.execute(
            select(func.count(CohortMember.id))
            .where(
                and_(
                    CohortMember.cohort_id == cohort_id,
                    CohortMember.role == CohortRole.INSTRUCTOR.value
                )
            )
        )
        count = instructor_count.scalar()
        if count <= 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot remove the last instructor from a cohort"
            )
    
    try:
        await db.execute(delete(CohortMember).where(CohortMember.id == member.id))
        await db.commit()
    except Exception as e:
        await db.rollback()
        logger.error(f"Error removing cohort member: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error removing cohort member: {str(e)}"
        )
    
    return None

