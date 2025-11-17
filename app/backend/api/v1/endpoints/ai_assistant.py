"""AI Learning Assistant endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, and_, delete
from typing import Optional
import logging
import json
from datetime import datetime, timedelta, timezone

from app.backend.core.database import get_db
from app.backend.core.security import get_current_user
from app.backend.models.user import User
from app.backend.models.notification import ChatMessage
from app.backend.models.thread_map import ThreadMap
from app.backend.models.query_log import QueryLog
from app.backend.services.llm_service import send_message, send_message_stream
from app.backend.core.chat_utils import extract_conversation_title
from app.backend.schemas.notification import (
    ChatMessageCreate,
    ChatMessageResponse,
    ChatHistoryResponse,
    ConversationResponse,
    ConversationListResponse,
    ConversationDetailResponse,
    ConversationTitleUpdate,
)

router = APIRouter()
logger = logging.getLogger(__name__)


def generate_conversation_id() -> int:
    """Generate a new conversation ID (simple timestamp-based)"""
    return int(datetime.now().timestamp() * 1000) % (10 ** 9)  # 9-digit ID


@router.post("/chat", response_model=ChatMessageResponse, status_code=status.HTTP_201_CREATED)
@router.post("/ai-assistant/chat", response_model=ChatMessageResponse, status_code=status.HTTP_201_CREATED)
async def chat_with_assistant(
    chat_data: ChatMessageCreate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Chat with the AI learning assistant (non-streaming)"""
    try:
        # Generate conversation_id if not provided
        conversation_id = chat_data.conversation_id
        if not conversation_id:
            conversation_id = generate_conversation_id()
    
        # Extract context from request
        context = chat_data.context or {}
        current_module_id = context.get("current_module_id")
        current_lesson_id = context.get("current_lesson_id")
        
        # Get IP address for logging
        ip_address = request.client.host if request.client else None
        
        # Call LLM service
        result = await send_message(
            db=db,
            user=current_user,
            message=chat_data.message,
            conversation_id=conversation_id,
            current_module_id=current_module_id,
            current_lesson_id=current_lesson_id,
            ip_address=ip_address,
            context_payload=context,
            image_document_ids=chat_data.image_document_ids,
        )
        
        response_text = result["response"]
        
        # Save chat message
        chat_message = ChatMessage(
            user_id=current_user.id,
            message=chat_data.message,
            response=response_text,
            context=context,
            suggested_lessons=None,
            escalated=False,
            conversation_id=conversation_id
        )
        
        db.add(chat_message)
        
        # Update thread map title if this is the first message
        thread_map_result = await db.execute(
            select(ThreadMap)
            .where(ThreadMap.conversation_id == conversation_id)
            .where(ThreadMap.user_id == current_user.id)
        )
        thread_map = thread_map_result.scalar_one_or_none()
        if thread_map and not thread_map.title:
            # Generate title from first message
            title = extract_conversation_title(chat_data.message)
            thread_map.title = title
        
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
            conversation_id=chat_message.conversation_id,
            created_at=chat_message.created_at
        )

    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat message: {str(e)}"
        )


@router.post("/chat/stream")
@router.post("/ai-assistant/chat/stream")
async def chat_with_assistant_stream(
    chat_data: ChatMessageCreate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Chat with the AI learning assistant (streaming)"""
    try:
        # Generate conversation_id if not provided
        conversation_id = chat_data.conversation_id
        if not conversation_id:
            conversation_id = generate_conversation_id()
        
        # Extract context
        context = chat_data.context or {}
        current_module_id = context.get("current_module_id")
        current_lesson_id = context.get("current_lesson_id")
        
        # Get IP address
        ip_address = request.client.host if request.client else None
        
        async def generate():
            full_response = ""
            try:
                # Send initial conversation_id
                yield f"data: {json.dumps({'type': 'conversation_id', 'conversation_id': conversation_id})}\n\n"
                
                # Stream response
                async for chunk in send_message_stream(
                    db=db,
                    user=current_user,
                    message=chat_data.message,
                    conversation_id=conversation_id,
                    current_module_id=current_module_id,
                    current_lesson_id=current_lesson_id,
                    ip_address=ip_address,
                    context_payload=context,
                    image_document_ids=chat_data.image_document_ids,
                ):
                    full_response += chunk
                    yield f"data: {json.dumps({'type': 'chunk', 'content': chunk})}\n\n"
                
                # Save chat message after streaming completes
                chat_message = ChatMessage(
                    user_id=current_user.id,
                    message=chat_data.message,
                    response=full_response,
                    context=context,
                    suggested_lessons=None,
                    escalated=False,
                    conversation_id=conversation_id
                )
                db.add(chat_message)
                
                # Update thread map title if needed
                thread_map_result = await db.execute(
                    select(ThreadMap)
                    .where(ThreadMap.conversation_id == conversation_id)
                    .where(ThreadMap.user_id == current_user.id)
                )
                thread_map = thread_map_result.scalar_one_or_none()
                if thread_map and not thread_map.title:
                    title = extract_conversation_title(chat_data.message)
                    thread_map.title = title
                
                await db.commit()
                
                # Send completion
                yield f"data: {json.dumps({'type': 'done'})}\n\n"
                
            except Exception as e:
                logger.error(f"Error in streaming: {str(e)}", exc_info=True)
                yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
                await db.rollback()
        
        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Conversation-Id": str(conversation_id),
            }
        )
        
    except Exception as e:
        logger.error(f"Error in stream endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing streaming chat: {str(e)}"
        )


@router.get("/conversations", response_model=ConversationListResponse)
@router.get("/ai-assistant/conversations", response_model=ConversationListResponse)
async def get_conversations(
    limit: int = 50,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get list of all conversations for the user"""
    # Get thread maps (conversations)
    result = await db.execute(
        select(ThreadMap)
        .where(ThreadMap.user_id == current_user.id)
        .order_by(desc(ThreadMap.last_used_at))
        .limit(limit)
        .offset(offset)
    )
    thread_maps = result.scalars().all()
    
    # Get total count
    count_result = await db.execute(
        select(func.count()).where(ThreadMap.user_id == current_user.id)
    )
    total = count_result.scalar() or 0
    
    # Get message counts and last message times for each conversation
    conversations = []
    for thread_map in thread_maps:
        # Get message count
        msg_count_result = await db.execute(
            select(func.count())
            .where(ChatMessage.conversation_id == thread_map.conversation_id)
            .where(ChatMessage.user_id == current_user.id)
        )
        message_count = msg_count_result.scalar() or 0
        
        # Get last message time
        last_msg_result = await db.execute(
            select(ChatMessage)
            .where(ChatMessage.conversation_id == thread_map.conversation_id)
            .where(ChatMessage.user_id == current_user.id)
            .order_by(desc(ChatMessage.created_at))
            .limit(1)
        )
        last_message = last_msg_result.scalar_one_or_none()
        last_message_at = last_message.created_at if last_message else thread_map.created_at
        
        conversations.append(ConversationResponse(
            conversation_id=thread_map.conversation_id,
            title=thread_map.title,
            last_message_at=last_message_at,
            message_count=message_count,
            created_at=thread_map.created_at
        ))
    
    return ConversationListResponse(
        conversations=conversations,
        total=total
    )


@router.get("/conversations/{conversation_id}", response_model=ConversationDetailResponse)
@router.get("/ai-assistant/conversations/{conversation_id}", response_model=ConversationDetailResponse)
async def get_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get conversation details with all messages"""
    # Verify conversation belongs to user
    thread_map_result = await db.execute(
        select(ThreadMap)
        .where(ThreadMap.conversation_id == conversation_id)
        .where(ThreadMap.user_id == current_user.id)
    )
    thread_map = thread_map_result.scalar_one_or_none()
    
    if not thread_map:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    # Get all messages for this conversation
    messages_result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.conversation_id == conversation_id)
        .where(ChatMessage.user_id == current_user.id)
        .order_by(ChatMessage.created_at)
    )
    messages = messages_result.scalars().all()
    
    # Get last message time
    last_message_at = messages[-1].created_at if messages else thread_map.created_at
    
    message_responses = [
        ChatMessageResponse(
            id=m.id,
            user_id=m.user_id,
            message=m.message,
            response=m.response,
            context=m.context,
            suggested_lessons=m.suggested_lessons,
            escalated=m.escalated,
            conversation_id=m.conversation_id,
            created_at=m.created_at
        )
        for m in messages
    ]
    
    return ConversationDetailResponse(
        conversation_id=conversation_id,
        title=thread_map.title,
        created_at=thread_map.created_at,
        last_message_at=last_message_at,
        message_count=len(messages),
        messages=message_responses
    )


@router.delete("/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
@router.delete("/ai-assistant/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a conversation and all associated data"""
    # Verify conversation belongs to user
    thread_map_result = await db.execute(
        select(ThreadMap)
        .where(ThreadMap.conversation_id == conversation_id)
        .where(ThreadMap.user_id == current_user.id)
    )
    thread_map = thread_map_result.scalar_one_or_none()
    
    if not thread_map:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    try:
        # Cancel any active OpenAI runs (if needed)
        # This would require additional logic to track active runs
        
        # Delete chat messages
        await db.execute(
            delete(ChatMessage)
            .where(ChatMessage.conversation_id == conversation_id)
            .where(ChatMessage.user_id == current_user.id)
        )
        
        # Delete query logs (optional - might want to keep for analytics)
        # await db.execute(
        #     delete(QueryLog)
        #     .where(QueryLog.conversation_id == conversation_id)
        #     .where(QueryLog.user_id == current_user.id)
        # )
        
        # Delete thread map
        await db.delete(thread_map)
        
        await db.commit()
        
    except Exception as e:
        logger.error(f"Error deleting conversation: {str(e)}", exc_info=True)
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting conversation: {str(e)}"
        )


@router.patch("/conversations/{conversation_id}/title", response_model=ConversationResponse)
@router.patch("/ai-assistant/conversations/{conversation_id}/title", response_model=ConversationResponse)
async def update_conversation_title(
    conversation_id: int,
    title_data: ConversationTitleUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update conversation title"""
    # Verify conversation belongs to user
    thread_map_result = await db.execute(
        select(ThreadMap)
        .where(ThreadMap.conversation_id == conversation_id)
        .where(ThreadMap.user_id == current_user.id)
    )
    thread_map = thread_map_result.scalar_one_or_none()
    
    if not thread_map:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    thread_map.title = title_data.title
    await db.commit()
    await db.refresh(thread_map)
    
    # Get message count for response
    msg_count_result = await db.execute(
        select(func.count())
        .where(ChatMessage.conversation_id == conversation_id)
        .where(ChatMessage.user_id == current_user.id)
    )
    message_count = msg_count_result.scalar() or 0
    
    # Get last message time
    last_msg_result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.conversation_id == conversation_id)
        .where(ChatMessage.user_id == current_user.id)
        .order_by(desc(ChatMessage.created_at))
        .limit(1)
    )
    last_message = last_msg_result.scalar_one_or_none()
    last_message_at = last_message.created_at if last_message else thread_map.created_at
    
    return ConversationResponse(
        conversation_id=thread_map.conversation_id,
        title=thread_map.title,
        last_message_at=last_message_at,
        message_count=message_count,
        created_at=thread_map.created_at
    )


@router.get("/chat/history", response_model=ChatHistoryResponse)
@router.get("/ai-assistant/history", response_model=ChatHistoryResponse)
async def get_chat_history(
    limit: int = 50,
    conversation_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user's chat history, optionally filtered by conversation"""
    query = select(ChatMessage).where(ChatMessage.user_id == current_user.id)
    
    if conversation_id:
        query = query.where(ChatMessage.conversation_id == conversation_id)
    
    result = await db.execute(
        query.order_by(desc(ChatMessage.created_at)).limit(limit)
    )
    messages = result.scalars().all()
    
    # Get total count
    count_query = select(func.count()).where(ChatMessage.user_id == current_user.id)
    if conversation_id:
        count_query = count_query.where(ChatMessage.conversation_id == conversation_id)
    count_result = await db.execute(count_query)
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
            conversation_id=m.conversation_id,
            created_at=m.created_at
        )
        for m in messages
    ]
    
    return ChatHistoryResponse(
        messages=message_responses,
        total=total
    )
