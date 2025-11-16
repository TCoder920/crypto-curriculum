"""Notification service for creating notifications"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from typing import Optional
import logging

from app.backend.models.notification import Notification
from app.backend.models.user import User

logger = logging.getLogger(__name__)


async def create_notification(
    db: AsyncSession,
    user_id: int,
    notification_type: str,
    title: str,
    message: str,
    link: Optional[str] = None
) -> Notification:
    """Create a notification for a user"""
    notification = Notification(
        user_id=user_id,
        type=notification_type,
        title=title,
        message=message,
        link=link,
        is_read=False
    )
    
    db.add(notification)
    await db.commit()
    await db.refresh(notification)
    
    logger.info(f"Created notification {notification.id} for user {user_id}: {notification_type}")
    
    return notification


async def notify_forum_reply(
    db: AsyncSession,
    post_author_id: int,
    reply_author_username: str,
    post_id: int,
    module_id: Optional[int] = None
):
    """Notify a user when someone replies to their forum post"""
    link = f"/modules/{module_id}/forums/posts/{post_id}" if module_id else f"/forums/posts/{post_id}"
    
    await create_notification(
        db=db,
        user_id=post_author_id,
        notification_type="forum_reply",
        title="New reply to your post",
        message=f"{reply_author_username} replied to your forum post",
        link=link
    )


async def notify_assessment_graded(
    db: AsyncSession,
    user_id: int,
    module_id: int,
    score: float
):
    """Notify a user when their assessment is graded"""
    await create_notification(
        db=db,
        user_id=user_id,
        notification_type="assessment_graded",
        title="Assessment graded",
        message=f"Your assessment for Module {module_id} has been graded. Score: {score}%",
        link=f"/modules/{module_id}/assessments/results"
    )


async def notify_module_unlocked(
    db: AsyncSession,
    user_id: int,
    module_id: int,
    module_title: str
):
    """Notify a user when a module is unlocked (prerequisites met)"""
    await create_notification(
        db=db,
        user_id=user_id,
        notification_type="module_unlocked",
        title="New module available",
        message=f"Module '{module_title}' is now available!",
        link=f"/modules/{module_id}"
    )


async def notify_announcement(
    db: AsyncSession,
    user_id: int,
    title: str,
    message: str,
    link: Optional[str] = None
):
    """Notify a user of an announcement"""
    await create_notification(
        db=db,
        user_id=user_id,
        notification_type="announcement",
        title=title,
        message=message,
        link=link
    )

