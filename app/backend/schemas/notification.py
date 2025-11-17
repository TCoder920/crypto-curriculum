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
    conversation_id: Optional[int] = Field(None, description="Conversation ID (generated if not provided)")
    context: Optional[dict] = Field(None, description="Context about current module/lesson")
    image_document_ids: Optional[List[int]] = Field(None, description="List of image document IDs to attach to the message")


class ChatMessageResponse(BaseModel):
    """Schema for chat message response"""
    id: int
    user_id: int
    message: str
    response: Optional[str]
    context: Optional[dict]
    suggested_lessons: Optional[List[int]]
    escalated: bool
    conversation_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


class ChatHistoryResponse(BaseModel):
    """Schema for chat history response"""
    messages: List[ChatMessageResponse]
    total: int


class ConversationResponse(BaseModel):
    """Schema for conversation metadata"""
    conversation_id: int
    title: Optional[str]
    last_message_at: Optional[datetime]
    message_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationListResponse(BaseModel):
    """Schema for conversation list response"""
    conversations: List[ConversationResponse]
    total: int


class ConversationDetailResponse(BaseModel):
    """Schema for conversation detail with messages"""
    conversation_id: int
    title: Optional[str]
    created_at: datetime
    last_message_at: Optional[datetime]
    message_count: int
    messages: List[ChatMessageResponse]


class ConversationTitleUpdate(BaseModel):
    """Schema for updating conversation title"""
    title: str = Field(..., min_length=1, max_length=200)

