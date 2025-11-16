"""Notification schemas"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class NotificationResponse(BaseModel):
    """Schema for notification response"""
    id: int
    user_id: int
    type: str  # 'assessment_graded', 'forum_reply', 'announcement', 'module_unlocked'
    title: str
    message: str
    link: Optional[str]
    is_read: bool
    created_at: datetime
    read_at: Optional[datetime]

    class Config:
        from_attributes = True


class NotificationListResponse(BaseModel):
    """Schema for paginated notification list"""
    notifications: List[NotificationResponse]
    total: int
    unread_count: int


class NotificationUpdate(BaseModel):
    """Schema for updating notification (mark as read)"""
    is_read: bool = True


class ChatMessageCreate(BaseModel):
    """Schema for creating a chat message"""
    message: str = Field(..., min_length=1, description="User message")
    context: Optional[dict] = Field(None, description="Context about current module/lesson")


class ChatMessageResponse(BaseModel):
    """Schema for chat message response"""
    id: int
    user_id: int
    message: str
    response: Optional[str]
    context: Optional[dict]
    suggested_lessons: Optional[List[int]]
    escalated: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ChatHistoryResponse(BaseModel):
    """Schema for chat history response"""
    messages: List[ChatMessageResponse]
    total: int

