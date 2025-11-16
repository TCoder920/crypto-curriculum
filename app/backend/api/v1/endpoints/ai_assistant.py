"""AI Learning Assistant endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from app.backend.models.progress import UserProgress
from app.backend.models.module import Module
from typing import Optional, List
import logging
import os

from app.backend.core.database import get_db
from app.backend.core.security import get_current_user
from app.backend.models.user import User
from app.backend.models.notification import ChatMessage
from app.backend.schemas.notification import (
    ChatMessageCreate,
    ChatMessageResponse,
    ChatHistoryResponse
)

router = APIRouter()
logger = logging.getLogger(__name__)


async def gather_user_context(
    user: User,
    db: AsyncSession
) -> dict:
    """
    Gather user-specific context for the AI assistant.
    Only includes information specific to this user for privacy and security.
    """
    
    # Get user's progress across all modules
    progress_result = await db.execute(
        select(UserProgress)
        .where(UserProgress.user_id == user.id)
        .order_by(UserProgress.last_accessed_at.desc())
    )
    user_progress = progress_result.scalars().all()
    
    # Get all modules for context
    modules_result = await db.execute(
        select(Module)
        .where(Module.is_published == True)
        .order_by(Module.order_index)
    )
    all_modules = modules_result.scalars().all()
    
    # Build context with only user-specific data
    context = {
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role.value if user.role else "student",
        },
        "progress": [
            {
                "module_id": p.module_id,
                "status": p.status.value if p.status else "not_started",
                "completion_percentage": p.completion_percentage,
                "last_accessed": p.last_accessed_at.isoformat() if p.last_accessed_at else None,
            }
            for p in user_progress
        ],
        "available_modules": [
            {
                "id": m.id,
                "title": m.title,
                "track": m.track.value if m.track else None,
                "order_index": m.order_index,
            }
            for m in all_modules
        ],
    }
    
    return context


@router.post("/ai-assistant/chat", response_model=ChatMessageResponse, status_code=status.HTTP_201_CREATED)
async def chat_with_assistant(
    chat_data: ChatMessageCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Chat with the AI learning assistant"""
    # Gather user-specific context
    user_context = await gather_user_context(current_user, db)
    
    # Merge with any additional context from the request
    full_context = {
        **user_context,
        **(chat_data.context or {}),
    }
    
    # Get LLM response - this will be handled by the LLM service/system prompt
    # No hardcoded logic here - just pass through to the LLM service
    try:
        # This should call your LLM service which will use the system prompt
        # The system prompt will handle all AI logic, blocking assessment answers, etc.
        # For now, we'll store the message and let the LLM service handle it
        response = None  # Will be populated by LLM service call
        
        # TODO: Call your LLM service here with:
        # - user_message: chat_data.message
        # - context: full_context
        # - system_prompt: (handled by LLM service)
        
    except Exception as e:
        logger.error(f"Error getting LLM response: {str(e)}")
        response = None
    
    # Save chat message
    chat_message = ChatMessage(
        user_id=current_user.id,
        message=chat_data.message,
        response=response,
        context=full_context,
        suggested_lessons=None,
        escalated=False
    )
    
    db.add(chat_message)
    await db.commit()
    await db.refresh(chat_message)
    
    return ChatMessageResponse(
        id=chat_message.id,
        user_id=chat_message.user_id,
        message=chat_message.message,
        response=chat_message.response,
        context=chat_message.context,
        suggested_lessons=chat_message.suggested_lessons,
        escalated=chat_message.escalated,
        created_at=chat_message.created_at
    )


@router.get("/ai-assistant/history", response_model=ChatHistoryResponse)
async def get_chat_history(
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user's chat history with AI assistant"""
    result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.user_id == current_user.id)
        .order_by(ChatMessage.created_at.desc())
        .limit(limit)
    )
    messages = result.scalars().all()
    
    # Get total count
    count_result = await db.execute(
        select(func.count()).where(ChatMessage.user_id == current_user.id)
    )
    total = count_result.scalar() or 0
    
    message_responses = [
        ChatMessageResponse(
            id=m.id,
            user_id=m.user_id,
            message=m.message,
            response=m.response,
            context=m.context,
            suggested_lessons=m.suggested_lessons,
            escalated=m.escalated,
            created_at=m.created_at
        )
        for m in messages
    ]
    
    return ChatHistoryResponse(
        messages=message_responses,
        total=total
    )

