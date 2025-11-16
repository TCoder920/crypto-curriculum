"""Forum endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_, desc, case
from sqlalchemy.orm import selectinload
from typing import Optional, List
from datetime import datetime
import logging

from app.backend.core.database import get_db
from app.backend.core.security import get_current_user
from app.backend.models.user import User, UserRole
from app.backend.models.forum import ForumPost, ForumVote
from app.backend.models.module import Module
from app.backend.schemas.forum import (
    ForumPostCreate,
    ForumPostUpdate,
    ForumPostResponse,
    ForumPostListResponse,
    ForumVoteCreate,
    ForumVoteResponse
)
from app.backend.api.v1.endpoints.auth import require_role
from app.backend.services.notification_service import notify_forum_reply
from app.backend.services.achievement_service import check_achievements

router = APIRouter()
logger = logging.getLogger(__name__)


async def get_author_info(user_id: int, db: AsyncSession) -> dict:
    """Get author information for a user"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return {"id": user_id, "username": None, "full_name": None, "role": "student"}
    return {
        "id": user.id,
        "username": user.username,
        "full_name": user.full_name,
        "role": user.role.value if user.role else "student"
    }


@router.get("/forums/modules/{module_id}/posts", response_model=ForumPostListResponse)
async def get_module_posts(
    module_id: int,
    sort: str = Query("recent", regex="^(recent|popular|unsolved)$"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: Optional[User] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get forum posts for a module"""
    # Verify module exists
    module_result = await db.execute(select(Module).where(Module.id == module_id))
    module = module_result.scalar_one_or_none()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    # Build query for top-level posts only
    query = select(ForumPost).where(
        and_(
            ForumPost.module_id == module_id,
            ForumPost.parent_post_id.is_(None)
        )
    )
    
    # Apply sorting
    if sort == "popular":
        query = query.order_by(desc(ForumPost.upvotes), desc(ForumPost.created_at))
    elif sort == "unsolved":
        query = query.order_by(ForumPost.is_solved, desc(ForumPost.created_at))
    else:  # recent
        query = query.order_by(desc(ForumPost.created_at))
    
    # Get total count
    count_query = select(func.count()).select_from(
        select(ForumPost).where(
            and_(
                ForumPost.module_id == module_id,
                ForumPost.parent_post_id.is_(None)
            )
        ).subquery()
    )
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # Apply pagination
    query = query.limit(limit).offset(offset)
    
    # Execute query
    result = await db.execute(query)
    posts = result.scalars().all()
    
    # Build response with author info and reply counts
    post_responses = []
    for post in posts:
        # Get reply count
        reply_count_result = await db.execute(
            select(func.count(ForumPost.id)).where(ForumPost.parent_post_id == post.id)
        )
        reply_count = reply_count_result.scalar() or 0
        
        # Get user vote if authenticated
        user_vote = None
        if current_user:
            vote_result = await db.execute(
                select(ForumVote).where(
                    and_(
                        ForumVote.post_id == post.id,
                        ForumVote.user_id == current_user.id
                    )
                )
            )
            vote = vote_result.scalar_one_or_none()
            if vote:
                user_vote = vote.vote_type
        
        author_info = await get_author_info(post.user_id, db)
        
        post_responses.append(ForumPostResponse(
            id=post.id,
            module_id=post.module_id,
            user_id=post.user_id,
            parent_post_id=post.parent_post_id,
            title=post.title,
            content=post.content,
            is_pinned=post.is_pinned,
            is_solved=post.is_solved,
            upvotes=post.upvotes,
            created_at=post.created_at,
            updated_at=post.updated_at,
            author=author_info,
            reply_count=reply_count,
            user_vote=user_vote
        ))
    
    return ForumPostListResponse(
        posts=post_responses,
        total=total,
        limit=limit,
        offset=offset
    )


@router.get("/forums/posts/{post_id}", response_model=ForumPostResponse)
async def get_post(
    post_id: int,
    current_user: Optional[User] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a single forum post with all replies"""
    result = await db.execute(select(ForumPost).where(ForumPost.id == post_id))
    post = result.scalar_one_or_none()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Get reply count
    reply_count_result = await db.execute(
        select(func.count(ForumPost.id)).where(ForumPost.parent_post_id == post.id)
    )
    reply_count = reply_count_result.scalar() or 0
    
    # Get user vote if authenticated
    user_vote = None
    if current_user:
        vote_result = await db.execute(
            select(ForumVote).where(
                and_(
                    ForumVote.post_id == post.id,
                    ForumVote.user_id == current_user.id
                )
            )
        )
        vote = vote_result.scalar_one_or_none()
        if vote:
            user_vote = vote.vote_type
    
    author_info = await get_author_info(post.user_id, db)
    
    return ForumPostResponse(
        id=post.id,
        module_id=post.module_id,
        user_id=post.user_id,
        parent_post_id=post.parent_post_id,
        title=post.title,
        content=post.content,
        is_pinned=post.is_pinned,
        is_solved=post.is_solved,
        upvotes=post.upvotes,
        created_at=post.created_at,
        updated_at=post.updated_at,
        author=author_info,
        reply_count=reply_count,
        user_vote=user_vote
    )


@router.get("/forums/posts/{post_id}/replies", response_model=List[ForumPostResponse])
async def get_post_replies(
    post_id: int,
    current_user: Optional[User] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all replies to a post"""
    # Verify parent post exists
    parent_result = await db.execute(select(ForumPost).where(ForumPost.id == post_id))
    parent = parent_result.scalar_one_or_none()
    if not parent:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Get replies
    result = await db.execute(
        select(ForumPost)
        .where(ForumPost.parent_post_id == post_id)
        .order_by(ForumPost.created_at)
    )
    replies = result.scalars().all()
    
    # Build response
    reply_responses = []
    for reply in replies:
        # Get user vote if authenticated
        user_vote = None
        if current_user:
            vote_result = await db.execute(
                select(ForumVote).where(
                    and_(
                        ForumVote.post_id == reply.id,
                        ForumVote.user_id == current_user.id
                    )
                )
            )
            vote = vote_result.scalar_one_or_none()
            if vote:
                user_vote = vote.vote_type
        
        author_info = await get_author_info(reply.user_id, db)
        
        reply_responses.append(ForumPostResponse(
            id=reply.id,
            module_id=reply.module_id,
            user_id=reply.user_id,
            parent_post_id=reply.parent_post_id,
            title=reply.title,
            content=reply.content,
            is_pinned=reply.is_pinned,
            is_solved=reply.is_solved,
            upvotes=reply.upvotes,
            created_at=reply.created_at,
            updated_at=reply.updated_at,
            author=author_info,
            reply_count=0,
            user_vote=user_vote
        ))
    
    return reply_responses


@router.post("/forums/posts", response_model=ForumPostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: ForumPostCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new forum post or reply"""
    # Validate: top-level posts need title, replies don't
    if post_data.parent_post_id is None:
        if not post_data.title:
            raise HTTPException(
                status_code=400,
                detail="Title is required for top-level posts"
            )
    else:
        # Verify parent post exists
        parent_result = await db.execute(
            select(ForumPost).where(ForumPost.id == post_data.parent_post_id)
        )
        parent = parent_result.scalar_one_or_none()
        if not parent:
            raise HTTPException(status_code=404, detail="Parent post not found")
        # Replies inherit module_id from parent
        if post_data.module_id is None:
            post_data.module_id = parent.module_id
    
    # Verify module exists if provided
    if post_data.module_id:
        module_result = await db.execute(
            select(Module).where(Module.id == post_data.module_id)
        )
        module = module_result.scalar_one_or_none()
        if not module:
            raise HTTPException(status_code=404, detail="Module not found")
    
    new_post = ForumPost(
        module_id=post_data.module_id,
        user_id=current_user.id,
        parent_post_id=post_data.parent_post_id,
        title=post_data.title,
        content=post_data.content,
        is_pinned=False,
        is_solved=False,
        upvotes=0
    )
    
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    
    # Check for achievements (forum engagement)
    await check_achievements(
        db=db,
        user_id=current_user.id,
        event_type="forum_post",
        event_data={"post_id": new_post.id, "module_id": new_post.module_id}
    )
    
    # Send notification if this is a reply (and not replying to own post)
    if new_post.parent_post_id and parent.user_id != current_user.id:
        try:
            author_username = current_user.username or current_user.full_name or "Someone"
            await notify_forum_reply(
                db=db,
                post_author_id=parent.user_id,
                reply_author_username=author_username,
                post_id=parent.id,
                module_id=parent.module_id
            )
        except Exception as e:
            logger.error(f"Failed to send forum reply notification: {str(e)}")
            # Don't fail the request if notification fails
    
    author_info = await get_author_info(new_post.user_id, db)
    
    return ForumPostResponse(
        id=new_post.id,
        module_id=new_post.module_id,
        user_id=new_post.user_id,
        parent_post_id=new_post.parent_post_id,
        title=new_post.title,
        content=new_post.content,
        is_pinned=new_post.is_pinned,
        is_solved=new_post.is_solved,
        upvotes=new_post.upvotes,
        created_at=new_post.created_at,
        updated_at=new_post.updated_at,
        author=author_info,
        reply_count=0,
        user_vote=None
    )


@router.patch("/forums/posts/{post_id}", response_model=ForumPostResponse)
async def update_post(
    post_id: int,
    post_data: ForumPostUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a forum post (author only)"""
    result = await db.execute(select(ForumPost).where(ForumPost.id == post_id))
    post = result.scalar_one_or_none()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Only author can update
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only edit your own posts")
    
    # Update fields
    if post_data.title is not None:
        post.title = post_data.title
    if post_data.content is not None:
        post.content = post_data.content
    
    post.updated_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(post)
    
    # Get reply count
    reply_count_result = await db.execute(
        select(func.count(ForumPost.id)).where(ForumPost.parent_post_id == post.id)
    )
    reply_count = reply_count_result.scalar() or 0
    
    author_info = await get_author_info(post.user_id, db)
    
    return ForumPostResponse(
        id=post.id,
        module_id=post.module_id,
        user_id=post.user_id,
        parent_post_id=post.parent_post_id,
        title=post.title,
        content=post.content,
        is_pinned=post.is_pinned,
        is_solved=post.is_solved,
        upvotes=post.upvotes,
        created_at=post.created_at,
        updated_at=post.updated_at,
        author=author_info,
        reply_count=reply_count,
        user_vote=None
    )


@router.post("/forums/posts/{post_id}/vote", response_model=ForumVoteResponse)
async def vote_post(
    post_id: int,
    vote_data: ForumVoteCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Vote on a forum post (upvote or downvote)"""
    # Verify post exists
    result = await db.execute(select(ForumPost).where(ForumPost.id == post_id))
    post = result.scalar_one_or_none()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Check if user already voted
    existing_vote_result = await db.execute(
        select(ForumVote).where(
            and_(
                ForumVote.post_id == post_id,
                ForumVote.user_id == current_user.id
            )
        )
    )
    existing_vote = existing_vote_result.scalar_one_or_none()
    
    if existing_vote:
        # Update existing vote
        if existing_vote.vote_type == vote_data.vote_type:
            # Same vote type - remove vote
            await db.delete(existing_vote)
            # Update post upvotes
            if vote_data.vote_type == "upvote":
                post.upvotes = max(0, post.upvotes - 1)
            else:
                post.upvotes = max(0, post.upvotes + 1)
        else:
            # Different vote type - change vote
            old_type = existing_vote.vote_type
            existing_vote.vote_type = vote_data.vote_type
            # Update post upvotes
            if old_type == "upvote" and vote_data.vote_type == "downvote":
                post.upvotes = max(0, post.upvotes - 2)
            elif old_type == "downvote" and vote_data.vote_type == "upvote":
                post.upvotes = post.upvotes + 2
    else:
        # Create new vote
        new_vote = ForumVote(
            post_id=post_id,
            user_id=current_user.id,
            vote_type=vote_data.vote_type
        )
        db.add(new_vote)
        # Update post upvotes
        if vote_data.vote_type == "upvote":
            post.upvotes = post.upvotes + 1
        else:
            post.upvotes = max(0, post.upvotes - 1)
    
    await db.commit()
    
    # Get the vote that was created/updated
    vote_result = await db.execute(
        select(ForumVote).where(
            and_(
                ForumVote.post_id == post_id,
                ForumVote.user_id == current_user.id
            )
        )
    )
    vote = vote_result.scalar_one_or_none()
    
    if not vote:
        # Vote was removed
        raise HTTPException(status_code=404, detail="Vote removed")
    
    return ForumVoteResponse(
        post_id=vote.post_id,
        user_id=vote.user_id,
        vote_type=vote.vote_type,
        created_at=vote.created_at
    )


@router.patch("/forums/posts/{post_id}/solve", response_model=ForumPostResponse)
async def mark_solved(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Mark a post as solved (author only)"""
    result = await db.execute(select(ForumPost).where(ForumPost.id == post_id))
    post = result.scalar_one_or_none()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Only author can mark as solved
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the post author can mark it as solved")
    
    # Only top-level posts can be marked as solved
    if post.parent_post_id is not None:
        raise HTTPException(status_code=400, detail="Only top-level posts can be marked as solved")
    
    post.is_solved = not post.is_solved
    await db.commit()
    await db.refresh(post)
    
    # Get reply count
    reply_count_result = await db.execute(
        select(func.count(ForumPost.id)).where(ForumPost.parent_post_id == post.id)
    )
    reply_count = reply_count_result.scalar() or 0
    
    author_info = await get_author_info(post.user_id, db)
    
    return ForumPostResponse(
        id=post.id,
        module_id=post.module_id,
        user_id=post.user_id,
        parent_post_id=post.parent_post_id,
        title=post.title,
        content=post.content,
        is_pinned=post.is_pinned,
        is_solved=post.is_solved,
        upvotes=post.upvotes,
        created_at=post.created_at,
        updated_at=post.updated_at,
        author=author_info,
        reply_count=reply_count,
        user_vote=None
    )


@router.patch("/forums/posts/{post_id}/pin", response_model=ForumPostResponse)
async def pin_post(
    post_id: int,
    current_user: User = Depends(require_role([UserRole.INSTRUCTOR, UserRole.ADMIN])),
    db: AsyncSession = Depends(get_db)
):
    """Pin/unpin a post (instructor/admin only)"""
    result = await db.execute(select(ForumPost).where(ForumPost.id == post_id))
    post = result.scalar_one_or_none()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Only top-level posts can be pinned
    if post.parent_post_id is not None:
        raise HTTPException(status_code=400, detail="Only top-level posts can be pinned")
    
    post.is_pinned = not post.is_pinned
    await db.commit()
    await db.refresh(post)
    
    # Get reply count
    reply_count_result = await db.execute(
        select(func.count(ForumPost.id)).where(ForumPost.parent_post_id == post.id)
    )
    reply_count = reply_count_result.scalar() or 0
    
    author_info = await get_author_info(post.user_id, db)
    
    return ForumPostResponse(
        id=post.id,
        module_id=post.module_id,
        user_id=post.user_id,
        parent_post_id=post.parent_post_id,
        title=post.title,
        content=post.content,
        is_pinned=post.is_pinned,
        is_solved=post.is_solved,
        upvotes=post.upvotes,
        created_at=post.created_at,
        updated_at=post.updated_at,
        author=author_info,
        reply_count=reply_count,
        user_vote=None
    )


@router.get("/forums/search", response_model=ForumPostListResponse)
async def search_posts(
    q: str = Query(..., min_length=1, description="Search query"),
    module_id: Optional[int] = Query(None, description="Filter by module"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: Optional[User] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Search forum posts"""
    # Build search query
    search_term = f"%{q.lower()}%"
    query = select(ForumPost).where(
        and_(
            or_(
                ForumPost.title.ilike(search_term),
                ForumPost.content.ilike(search_term)
            ),
            ForumPost.parent_post_id.is_(None)  # Only top-level posts
        )
    )
    
    if module_id:
        query = query.where(ForumPost.module_id == module_id)
    
    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # Apply sorting and pagination
    query = query.order_by(desc(ForumPost.created_at)).limit(limit).offset(offset)
    
    # Execute query
    result = await db.execute(query)
    posts = result.scalars().all()
    
    # Build response
    post_responses = []
    for post in posts:
        # Get reply count
        reply_count_result = await db.execute(
            select(func.count(ForumPost.id)).where(ForumPost.parent_post_id == post.id)
        )
        reply_count = reply_count_result.scalar() or 0
        
        # Get user vote if authenticated
        user_vote = None
        if current_user:
            vote_result = await db.execute(
                select(ForumVote).where(
                    and_(
                        ForumVote.post_id == post.id,
                        ForumVote.user_id == current_user.id
                    )
                )
            )
            vote = vote_result.scalar_one_or_none()
            if vote:
                user_vote = vote.vote_type
        
        author_info = await get_author_info(post.user_id, db)
        
        post_responses.append(ForumPostResponse(
            id=post.id,
            module_id=post.module_id,
            user_id=post.user_id,
            parent_post_id=post.parent_post_id,
            title=post.title,
            content=post.content,
            is_pinned=post.is_pinned,
            is_solved=post.is_solved,
            upvotes=post.upvotes,
            created_at=post.created_at,
            updated_at=post.updated_at,
            author=author_info,
            reply_count=reply_count,
            user_vote=user_vote
        ))
    
    return ForumPostListResponse(
        posts=post_responses,
        total=total,
        limit=limit,
        offset=offset
    )

