"""OpenAI utilities for managing assistants and vector stores"""
from typing import Optional, Dict, Any
import logging
from openai import AsyncOpenAI
from pathlib import Path
from sqlalchemy import update, inspect, select, or_
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.core.config import settings
from app.backend.models.user import User
from app.backend.models.document import Document

logger = logging.getLogger(__name__)

# Initialize OpenAI client
_client: Optional[AsyncOpenAI] = None


def get_openai_client() -> AsyncOpenAI:
    """Get or create OpenAI client instance"""
    global _client
    if _client is None:
        api_key = settings.OPENAI_API_KEY
        if not api_key or api_key.strip() == "":
            raise ValueError("OPENAI_API_KEY is not set in configuration. Please set it in your .env file.")
        _client = AsyncOpenAI(api_key=api_key)
    return _client


async def get_or_create_user_assistant(user: User, db=None, vector_store_id: Optional[str] = None) -> str:
    """
    Get or create a user-specific OpenAI assistant.
    
    Args:
        user: User object
        db: Optional database session to save assistant_id
        vector_store_id: Optional vector store ID to attach to assistant
    
    Returns:
        Assistant ID
    """
    client = get_openai_client()
    
    # Check if user already has an assistant
    if user.openai_assistant_id:
        try:
            # Verify assistant still exists and update if vector store provided
            assistant = await client.beta.assistants.retrieve(user.openai_assistant_id)
            
            # Update assistant with vector store if provided and different
            if vector_store_id:
                tool_resources = {"file_search": {"vector_store_ids": [vector_store_id]}}
                # Check if assistant needs update
                current_tool_resources = getattr(assistant, 'tool_resources', None)
                current_vs_ids = current_tool_resources.get("file_search", {}).get("vector_store_ids", []) if current_tool_resources else []
                
                if vector_store_id not in current_vs_ids:
                    # Update assistant with file_search tool and vector store
                    await client.beta.assistants.update(
                        assistant.id,
                        tools=[{"type": "file_search"}],
                        tool_resources=tool_resources
                    )
                    logger.info(f"Updated assistant {assistant.id} with vector store {vector_store_id}")
            
            return assistant.id
        except Exception as e:
            logger.warning(f"User assistant {user.openai_assistant_id} not found, creating new one: {e}")
    
    # Prepare assistant configuration
    assistant_config = {
        "name": f"Learning Assistant for {user.username or user.email}",
        "instructions": "You are a helpful learning assistant for blockchain and cryptocurrency education.",
        "model": "gpt-4.1-mini",  # Using gpt-4.1-mini model
        "tools": [],
    }
    
    # Add file_search tool and vector store if provided
    if vector_store_id:
        assistant_config["tools"] = [{"type": "file_search"}]
        assistant_config["tool_resources"] = {"file_search": {"vector_store_ids": [vector_store_id]}}
    
    # Create new assistant
    assistant = await client.beta.assistants.create(**assistant_config)
    
    # Store assistant ID in user model
    user.openai_assistant_id = assistant.id
    
    # Save to database if session provided
    if db:
        await db.execute(
            update(User)
            .where(User.id == user.id)
            .values(openai_assistant_id=assistant.id)
        )
        await db.commit()
        try:
            user_state = inspect(user)
            if user_state.persistent:
                await db.refresh(user)
            else:
                refreshed_user = await db.get(User, user.id)
                if refreshed_user:
                    user.openai_assistant_id = refreshed_user.openai_assistant_id
        except InvalidRequestError as refresh_err:
            logger.warning(f"Could not refresh user {user.id} after assistant creation: {refresh_err}")
        except Exception as refresh_err:  # pragma: no cover
            logger.warning(f"Unexpected error refreshing user {user.id}: {refresh_err}")
    
    return assistant.id


async def get_or_create_user_vector_store(user: User, db: AsyncSession | None = None) -> Optional[str]:
    """
    Get or create a user-specific vector store for RAG.
    
    Returns:
        Vector store ID or None if OpenAI is not configured
    """
    try:
        client = get_openai_client()
    except ValueError as e:
        logger.warning(f"Vector store unavailable: {e}")
        return None

    if user.openai_vector_store_id:
        try:
            store = await client.beta.vector_stores.retrieve(user.openai_vector_store_id)
            return store.id
        except Exception as e:
            logger.warning(f"Vector store {user.openai_vector_store_id} missing, recreating: {e}")

    vector_store = await client.beta.vector_stores.create(
        name=f"{user.username or 'user'} reference library",
        metadata={"user_id": str(user.id)},
    )

    user.openai_vector_store_id = vector_store.id
    if db:
        await db.execute(
            update(User)
            .where(User.id == user.id)
            .values(openai_vector_store_id=vector_store.id)
        )
        await db.commit()
        try:
            user_state = inspect(user)
            if user_state.persistent:
                await db.refresh(user)
            else:
                refreshed_user = await db.get(User, user.id)
                if refreshed_user:
                    user.openai_vector_store_id = refreshed_user.openai_vector_store_id
        except Exception as refresh_err:  # pragma: no cover
            logger.warning(f"Unable to refresh user {user.id} after vector store creation: {refresh_err}")

    return vector_store.id


async def update_user_assistant_instructions(
    user: User,
    instructions: str
) -> str:
    """
    Update user assistant's instructions with context.
    
    Args:
        user: User object
        instructions: New instructions to set
    
    Returns:
        Updated assistant ID
    """
    client = get_openai_client()
    assistant_id = await get_or_create_user_assistant(user)
    
    await client.beta.assistants.update(
        assistant_id,
        instructions=instructions
    )
    
    return assistant_id


async def get_global_assistant_id() -> Optional[str]:
    """
    Get the global fallback assistant ID from config.
    Validates that the assistant exists before returning it.
    
    Returns:
        Assistant ID or None if not configured or doesn't exist
    """
    assistant_id = settings.OPENAI_ASSISTANT_ID
    if not assistant_id or not assistant_id.strip():
        return None
    
    assistant_id = assistant_id.strip()
    
    # Validate that the assistant exists
    try:
        client = get_openai_client()
        await client.beta.assistants.retrieve(assistant_id)
        return assistant_id
    except Exception as e:
        logger.warning(f"Global assistant {assistant_id} not found or invalid: {e}")
        return None


async def get_assistant_for_user(user: User, db=None, vector_store_id: Optional[str] = None) -> str:
    """
    Get assistant ID for user, falling back to global assistant if needed.
    
    Args:
        user: User object
        db: Optional database session
        vector_store_id: Optional vector store ID to attach to assistant
    
    Returns:
        Assistant ID
    """
    # First check if global assistant is configured and valid - use it if available
    global_id = await get_global_assistant_id()
    if global_id:
        logger.info(f"Using validated global assistant: {global_id}")
        return global_id
    
    # Otherwise, try to get or create user-specific assistant
    try:
        logger.info(f"Creating/getting user-specific assistant for user {user.id}")
        return await get_or_create_user_assistant(user, db, vector_store_id)
    except Exception as e:
        logger.error(f"Error getting user assistant: {e}", exc_info=True)
        # Try global assistant one more time as fallback
        global_id = await get_global_assistant_id()
        if global_id:
            logger.warning(f"Falling back to global assistant due to error: {e}")
            return global_id
        raise ValueError(f"No assistant available. Error: {str(e)}. Please configure OPENAI_API_KEY. If using OPENAI_ASSISTANT_ID, ensure it exists in your OpenAI account.")


def _is_image_file(file_path: Path) -> bool:
    """Check if a file is an image based on extension."""
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
    return file_path.suffix.lower() in image_extensions


def _is_text_document(file_path: Path) -> bool:
    """Check if a file is a text-based document suitable for vector store."""
    text_extensions = {'.pdf', '.docx', '.txt', '.md', '.csv'}
    return file_path.suffix.lower() in text_extensions


async def _upload_file_to_openai(client: AsyncOpenAI, file_path: Path) -> Optional[str]:
    """Upload a local file to OpenAI and return the file ID."""
    if not file_path.exists():
        logger.warning("Skipping upload; file missing at %s", file_path)
        return None
    try:
        with file_path.open("rb") as handle:
            uploaded = await client.files.create(file=handle, purpose="assistants")
        return uploaded.id
    except Exception as e:
        logger.error("Failed to upload %s to OpenAI: %s", file_path, e)
        return None


async def update_vector_store(db: AsyncSession, user: User) -> Optional[str]:
    """
    Ensure the user's vector store is synchronized with stored documents.
    
    Returns:
        The vector store ID if available, otherwise None.
    """
    vector_store_id = await get_or_create_user_vector_store(user, db)
    if not vector_store_id:
        return None

    client = get_openai_client()

    # Fetch documents visible to the user (their uploads + shared/standard)
    try:
        result = await db.execute(
            select(Document)
            .where(Document.is_deleted == False)  # noqa: E712
            .where(or_(Document.uploader_id == user.id, Document.category == "standard"))
        )
        documents = result.scalars().all()
    except Exception as e:
        logger.warning("Unable to load documents for vector sync: %s", e)
        return vector_store_id

    # Check currently attached files (OpenAI max limit is 100 per request)
    attached_file_ids = set()
    try:
        # List files with max limit of 100
        vector_files = await client.beta.vector_stores.files.list(
            vector_store_id=vector_store_id,
            limit=100
        )
        attached_file_ids = {item.id for item in vector_files.data}
        
        # If there are more files, paginate (though unlikely for most users)
        # Note: OpenAI API uses cursor-based pagination with 'after' parameter
        while vector_files.has_more and vector_files.last_id:
            vector_files = await client.beta.vector_stores.files.list(
                vector_store_id=vector_store_id,
                limit=100,
                after=vector_files.last_id
            )
            attached_file_ids.update({item.id for item in vector_files.data})
    except Exception as e:
        logger.warning("Unable to list files for vector store %s: %s", vector_store_id, e)

    desired_file_ids: set[str] = set()
    dirty = False

    for document in documents:
        file_path = Path(document.storage_path)
        if not file_path.exists():
            logger.warning("Document %s missing on disk at %s", document.id, document.storage_path)
            continue

        # Skip image files - they are not suitable for vector store file_search
        # Images will be attached directly to messages when needed
        if _is_image_file(file_path):
            logger.debug("Skipping image file %s from vector store (images attached directly to messages)", file_path.name)
            continue

        # Only process text-based documents for vector store
        if not _is_text_document(file_path):
            logger.debug("Skipping non-text document %s from vector store", file_path.name)
            continue

        file_id = document.openai_file_id

        # If file already attached, mark as desired and continue
        if file_id and file_id in attached_file_ids:
            desired_file_ids.add(file_id)
            continue

        # If file exists in DB but not attached, try to reattach
        if file_id:
            try:
                await client.beta.vector_stores.files.create(vector_store_id=vector_store_id, file_id=file_id)
                desired_file_ids.add(file_id)
                attached_file_ids.add(file_id)
                continue
            except Exception as e:
                logger.warning("Reattaching OpenAI file %s failed: %s", file_id, e)

        # Upload a fresh copy
        uploaded_id = await _upload_file_to_openai(client, file_path)
        if not uploaded_id:
            continue

        document.openai_file_id = uploaded_id
        desired_file_ids.add(uploaded_id)
        dirty = True

        try:
            await client.beta.vector_stores.files.create(vector_store_id=vector_store_id, file_id=uploaded_id)
            attached_file_ids.add(uploaded_id)
        except Exception as e:
            logger.error(
                "Unable to attach uploaded file %s to vector store %s: %s",
                uploaded_id,
                vector_store_id,
                e,
            )

    # Remove stale files no longer tied to documents
    stale_files = attached_file_ids - desired_file_ids
    for file_id in stale_files:
        try:
            await client.beta.vector_stores.files.delete(vector_store_id=vector_store_id, file_id=file_id)
        except Exception as e:
            logger.warning("Failed to remove stale file %s from vector store %s: %s", file_id, vector_store_id, e)

    if dirty:
        await db.commit()

    return vector_store_id


async def cancel_active_run(thread_id: str, run_id: str) -> None:
    """
    Cancel an active OpenAI run.
    
    Args:
        thread_id: OpenAI thread ID
        run_id: OpenAI run ID
    """
    try:
        client = get_openai_client()
        await client.beta.threads.runs.cancel(thread_id=thread_id, run_id=run_id)
        logger.info(f"Cancelled run {run_id} for thread {thread_id}")
    except Exception as e:
        logger.warning(f"Error cancelling run {run_id}: {e}")


async def list_active_runs(thread_id: str) -> list[Dict[str, Any]]:
    """
    List active runs for a thread.
    
    Args:
        thread_id: OpenAI thread ID
    
    Returns:
        List of active run objects
    """
    try:
        client = get_openai_client()
        runs = await client.beta.threads.runs.list(thread_id=thread_id, limit=10)
        active_runs = [run for run in runs.data if run.status in ["queued", "in_progress"]]
        return [{"id": run.id, "status": run.status} for run in active_runs]
    except Exception as e:
        logger.warning(f"Error listing runs for thread {thread_id}: {e}")
        return []
