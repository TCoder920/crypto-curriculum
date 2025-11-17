"""LLM service for OpenAI Assistants API integration"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, Dict, Any, AsyncGenerator
import logging
from openai import AsyncOpenAI

from app.backend.core.openai_utils import (
    get_openai_client,
    get_assistant_for_user,
    cancel_active_run,
    list_active_runs,
    update_vector_store,
)
from app.backend.core.chat_utils import (
    format_system_prompt_with_context,
    sanitize_message
)
from app.backend.services.context_service import gather_user_context
from app.backend.models.user import User
from app.backend.models.thread_map import ThreadMap
from app.backend.models.query_log import QueryLog
from app.backend.models.document import Document
from pathlib import Path

logger = logging.getLogger(__name__)


async def get_or_create_thread(
    db: AsyncSession,
    user: User,
    conversation_id: int
) -> str:
    """
    Get or create OpenAI thread for a conversation.
    
    Args:
        db: Database session
        user: User object
        conversation_id: Frontend conversation ID
    
    Returns:
        OpenAI thread ID
    """
    # Check if thread mapping exists
    result = await db.execute(
        select(ThreadMap)
        .where(ThreadMap.conversation_id == conversation_id)
        .where(ThreadMap.user_id == user.id)
    )
    thread_map = result.scalar_one_or_none()
    
    if thread_map:
        # Update last_used_at
        thread_map.last_used_at = func.now()
        await db.commit()
        return thread_map.thread_id
    
    # Create new thread
    client = get_openai_client()
    thread = await client.beta.threads.create()
    
    # Create thread mapping
    thread_map = ThreadMap(
        conversation_id=conversation_id,
        thread_id=thread.id,
        user_id=user.id
    )
    db.add(thread_map)
    await db.commit()
    await db.refresh(thread_map)
    
    logger.info(f"Created new thread {thread.id} for conversation {conversation_id}")
    return thread.id


async def cancel_active_runs_for_thread(thread_id: str) -> None:
    """
    Cancel any active runs for a thread to prevent conflicts.
    
    Args:
        thread_id: OpenAI thread ID
    """
    try:
        active_runs = await list_active_runs(thread_id)
        for run in active_runs:
            await cancel_active_run(thread_id, run["id"])
    except Exception as e:
        logger.warning(f"Error cancelling active runs: {e}")


async def _get_image_file_ids(
    db: AsyncSession,
    user: User,
    image_document_ids: Optional[list[int]] = None,
) -> list[str]:
    """
    Get OpenAI file IDs for image documents.
    Uploads images to OpenAI if not already uploaded.
    """
    if not image_document_ids:
        return []
    
    from app.backend.core.openai_utils import get_openai_client, _upload_file_to_openai, _is_image_file
    
    client = get_openai_client()
    file_ids = []
    
    result = await db.execute(
        select(Document)
        .where(Document.id.in_(image_document_ids))
        .where(Document.is_deleted == False)  # noqa: E712
        .where(Document.uploader_id == user.id)  # Only user's own images
    )
    documents = result.scalars().all()
    
    for document in documents:
        file_path = Path(document.storage_path)
        if not file_path.exists() or not _is_image_file(file_path):
            continue
        
        # Use existing OpenAI file ID if available
        if document.openai_file_id:
            file_ids.append(document.openai_file_id)
            continue
        
        # Upload to OpenAI
        file_id = await _upload_file_to_openai(client, file_path)
        if file_id:
            document.openai_file_id = file_id
            file_ids.append(file_id)
    
    if file_ids:
        await db.commit()
    
    return file_ids


async def send_message(
    db: AsyncSession,
    user: User,
    message: str,
    conversation_id: int,
    current_module_id: Optional[int] = None,
    current_lesson_id: Optional[int] = None,
    ip_address: Optional[str] = None,
    context_payload: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Send a message to the AI assistant and get response.
    
    Args:
        db: Database session
        user: User object
        message: User's message
        conversation_id: Conversation ID
        current_module_id: Optional current module ID for context
        current_lesson_id: Optional current lesson ID for context
        ip_address: Optional IP address for logging
    
    Returns:
        Dict with 'response' and 'conversation_id'
    """
    try:
        client = get_openai_client()
    except ValueError as e:
        logger.error(f"OpenAI client initialization failed: {e}")
        raise Exception(f"AI service configuration error: {str(e)}")
    
    # Sanitize message
    sanitized_message = sanitize_message(message)
    
    # Get image file IDs if provided
    image_file_ids = await _get_image_file_ids(db, user, image_document_ids)
    
    # Get or create thread
    thread_id = await get_or_create_thread(db, user, conversation_id)
    
    # Cancel any active runs to prevent conflicts
    await cancel_active_runs_for_thread(thread_id)
    
    # Gather user context
    try:
        context = await gather_user_context(
            user,
            db,
            current_module_id=current_module_id,
            current_lesson_id=current_lesson_id,
            extra_context=context_payload,
        )
    except Exception as e:
        logger.error(f"Error gathering context: {e}")
        context = {}
    
    # Format system prompt with context
    system_instructions = format_system_prompt_with_context(context)

    # Sync vector store
    vector_store_id = None
    try:
        vector_store_id = await update_vector_store(db, user)
    except Exception as e:
        logger.warning(f"Vector store sync failed for user {user.id}: {e}")
    
    # Get user's assistant (will attach vector store if available)
    try:
        assistant_id = await get_assistant_for_user(user, db, vector_store_id)
    except Exception as e:
        logger.error(f"Failed to get assistant for user {user.id}: {e}")
        raise Exception(f"Failed to initialize AI assistant: {str(e)}")
    
    # Build message content (text + images)
    message_content: list[Dict[str, Any]] = [{"type": "text", "text": sanitized_message}]
    
    # Add image file attachments if any
    for file_id in image_file_ids:
        message_content.append({"type": "image_file", "image_file": {"file_id": file_id}})
    
    # Add message to thread
    try:
        await client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message_content if image_file_ids else sanitized_message
        )
    except Exception as e:
        logger.error(f"Failed to add message to thread {thread_id}: {e}")
        raise Exception(f"Failed to send message to AI: {str(e)}")
    
    # Create run with context in additional_instructions
    # Note: tool_resources is set on the assistant, not on the run
    try:
        run = await client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
            additional_instructions=system_instructions,
        )
    except Exception as e:
        logger.error(f"Failed to create run for thread {thread_id}: {e}")
        raise Exception(f"Failed to start AI conversation: {str(e)}")
    
    # Wait for completion
    import asyncio
    while True:
        run_status = await client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        
        if run_status.status == "completed":
            break
        elif run_status.status in ["failed", "cancelled", "expired"]:
            error_msg = f"Run {run_status.status}: {run_status.last_error.message if run_status.last_error else 'Unknown error'}"
            logger.error(error_msg)
            raise Exception(error_msg)
        
        await asyncio.sleep(0.5)  # Poll every 500ms
    
    # Get response
    messages = await client.beta.threads.messages.list(thread_id=thread_id, limit=1)
    response_text = ""
    
    if messages.data:
        message = messages.data[0]
        if hasattr(message, 'content') and message.content:
            for content in message.content:
                if hasattr(content, 'type') and content.type == "text":
                    if hasattr(content, 'text') and hasattr(content.text, 'value'):
                        response_text = content.text.value
                        break
    
    if not response_text:
        logger.warning(f"No response text found for thread {thread_id}, run {run.id}")
        response_text = "I apologize, but I couldn't generate a response. Please try again."
    
    # Log query
    try:
        query_log = QueryLog(
            user_id=user.id,
            query=sanitized_message,
            response=response_text,
            operation_type="chat",
            conversation_id=conversation_id,
            ip_address=ip_address
        )
        db.add(query_log)
        await db.commit()
    except Exception as e:
        logger.error(f"Error logging query: {e}")
        await db.rollback()
    
    return {
        "response": response_text,
        "conversation_id": conversation_id
    }


async def send_message_stream(
    db: AsyncSession,
    user: User,
    message: str,
    conversation_id: int,
    current_module_id: Optional[int] = None,
    current_lesson_id: Optional[int] = None,
    ip_address: Optional[str] = None,
    context_payload: Optional[Dict[str, Any]] = None,
    image_document_ids: Optional[list[int]] = None,
) -> AsyncGenerator[str, None]:
    """
    Send a message and stream the response.
    
    Yields:
        Response text chunks
    """
    client = get_openai_client()
    
    # Sanitize message
    sanitized_message = sanitize_message(message)
    
    # Get image file IDs if provided
    image_file_ids = await _get_image_file_ids(db, user, image_document_ids)
    
    # Get or create thread
    thread_id = await get_or_create_thread(db, user, conversation_id)
    
    # Cancel any active runs
    await cancel_active_runs_for_thread(thread_id)
    
    # Gather user context
    try:
        context = await gather_user_context(
            user,
            db,
            current_module_id=current_module_id,
            current_lesson_id=current_lesson_id,
            extra_context=context_payload,
        )
    except Exception as e:
        logger.error(f"Error gathering context: {e}")
        context = {}
    
    # Format system prompt
    system_instructions = format_system_prompt_with_context(context)

    # Sync vector store
    vector_store_id = None
    try:
        vector_store_id = await update_vector_store(db, user)
    except Exception as e:
        logger.warning(f"Vector store sync failed for user {user.id}: {e}")
    
    # Get assistant (will attach vector store if available)
    assistant_id = await get_assistant_for_user(user, db, vector_store_id)
    
    # Build message content (text + images)
    message_content: list[Dict[str, Any]] = [{"type": "text", "text": sanitized_message}]
    
    # Add image file attachments if any
    for file_id in image_file_ids:
        message_content.append({"type": "image_file", "image_file": {"file_id": file_id}})
    
    # Add message to thread
    await client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message_content if image_file_ids else sanitized_message
    )
    
    # Create run
    # Note: tool_resources is set on the assistant, not on the run
    run = await client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        additional_instructions=system_instructions,
    )
    
    # Stream response
    import asyncio
    full_response = ""
    
    while True:
        run_status = await client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        
        if run_status.status == "completed":
            # Get final response
            messages = await client.beta.threads.messages.list(thread_id=thread_id, limit=1)
            if messages.data:
                message = messages.data[0]
                if message.content:
                    for content in message.content:
                        if content.type == "text":
                            remaining = content.text.value[len(full_response):]
                            if remaining:
                                yield remaining
                                full_response = content.text.value
            break
        elif run_status.status in ["failed", "cancelled", "expired"]:
            error_msg = f"Run {run_status.status}: {run_status.last_error.message if run_status.last_error else 'Unknown error'}"
            logger.error(error_msg)
            yield f"\n\n[Error: {error_msg}]"
            break
        elif run_status.status == "requires_action":
            # Handle tool calls if needed (for future web search feature)
            logger.warning("Run requires action - tool calls not yet implemented")
            await asyncio.sleep(0.5)
        else:
            await asyncio.sleep(0.5)
    
    # Log query
    try:
        query_log = QueryLog(
            user_id=user.id,
            query=sanitized_message,
            response=full_response,
            operation_type="stream",
            conversation_id=conversation_id,
            ip_address=ip_address
        )
        db.add(query_log)
        await db.commit()
    except Exception as e:
        logger.error(f"Error logging query: {e}")
        await db.rollback()
