"""Notification endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, desc
from typing import Optional, List
from datetime import datetime
import logging

from app.backend.core.database import get_db
from app.backend.core.security import get_current_user
from app.backend.models.user import User
from app.backend.models.notification import Notification
from app.backend.schemas.notification import (
    NotificationResponse,
    NotificationListResponse,
    NotificationUpdate
)

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/notifications", response_model=NotificationListResponse)
async def get_notifications(
    unread_only: bool = Query(False, description="Filter to unread only"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user's notifications"""
    # Build query
    query = select(Notification).where(Notification.user_id == current_user.id)
    
    if unread_only:
        query = query.where(Notification.is_read == False)
    
    # Get total count
    count_query = select(func.count()).select_from(
        select(Notification).where(Notification.user_id == current_user.id).subquery()
    )
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # Get unread count
    unread_count_result = await db.execute(
        select(func.count()).where(
            and_(
                Notification.user_id == current_user.id,
                Notification.is_read == False
            )
        )
    )
    unread_count = unread_count_result.scalar() or 0
    
    # Apply sorting and pagination
    query = query.order_by(desc(Notification.created_at)).limit(limit).offset(offset)
    
    # Execute query
    result = await db.execute(query)
    notifications = result.scalars().all()
    
    # Build response
    notification_responses = [
        NotificationResponse(
            id=n.id,
            user_id=n.user_id,
            type=n.type,
            title=n.title,
            message=n.message,
            link=n.link,
            is_read=n.is_read,
            created_at=n.created_at,
            read_at=n.read_at
        )
        for n in notifications
    ]
    
    return NotificationListResponse(
        notifications=notification_responses,
        total=total,
        unread_count=unread_count
    )


@router.patch("/notifications/{notification_id}", response_model=NotificationResponse)
async def update_notification(
    notification_id: int,
    notification_data: NotificationUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Mark notification as read/unread"""
    result = await db.execute(
        select(Notification).where(Notification.id == notification_id)
    )
    notification = result.scalar_one_or_none()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    # Only owner can update
    if notification.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only update your own notifications")
    
    # Update read status
    notification.is_read = notification_data.is_read
    if notification_data.is_read:
        notification.read_at = datetime.utcnow()
    else:
        notification.read_at = None
    
    await db.commit()
    await db.refresh(notification)
    
    return NotificationResponse(
        id=notification.id,
        user_id=notification.user_id,
        type=notification.type,
        title=notification.title,
        message=notification.message,
        link=notification.link,
        is_read=notification.is_read,
        created_at=notification.created_at,
        read_at=notification.read_at
    )


@router.patch("/notifications/mark-all-read", status_code=status.HTTP_204_NO_CONTENT)
async def mark_all_read(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Mark all notifications as read"""
    result = await db.execute(
        select(Notification).where(
            and_(
                Notification.user_id == current_user.id,
                Notification.is_read == False
            )
        )
    )
    notifications = result.scalars().all()
    
    for notification in notifications:
        notification.is_read = True
        notification.read_at = datetime.utcnow()
    
    await db.commit()
    
    return None


@router.delete("/notifications/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notification(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a notification"""
    result = await db.execute(
        select(Notification).where(Notification.id == notification_id)
    )
    notification = result.scalar_one_or_none()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    # Only owner can delete
    if notification.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only delete your own notifications")
    
    await db.delete(notification)
    await db.commit()
    
    return None

