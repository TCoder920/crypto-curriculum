"""Forum schemas"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ForumPostCreate(BaseModel):
    """Schema for creating a forum post"""
    module_id: Optional[int] = None
    title: Optional[str] = Field(None, max_length=200, description="Title (required for top-level posts)")
    content: str = Field(..., min_length=1, description="Post content")
    parent_post_id: Optional[int] = None  # If set, this is a reply


class ForumPostUpdate(BaseModel):
    """Schema for updating a forum post"""
    title: Optional[str] = Field(None, max_length=200)
    content: Optional[str] = Field(None, min_length=1)


class AuthorInfo(BaseModel):
    """Author information for forum posts"""
    id: int
    username: Optional[str]
    full_name: Optional[str]
    role: str

    class Config:
        from_attributes = True


class ForumPostResponse(BaseModel):
    """Schema for forum post response"""
    id: int
    module_id: Optional[int]
    user_id: int
    parent_post_id: Optional[int]
    title: Optional[str]
    content: str
    is_pinned: bool
    is_solved: bool
    upvotes: int
    created_at: datetime
    updated_at: Optional[datetime]
    author: AuthorInfo
    reply_count: int = 0
    user_vote: Optional[str] = None  # 'upvote' or 'downvote' or None

    class Config:
        from_attributes = True


class ForumPostListResponse(BaseModel):
    """Schema for paginated forum post list"""
    posts: List[ForumPostResponse]
    total: int
    limit: int
    offset: int


class ForumVoteCreate(BaseModel):
    """Schema for creating a vote"""
    vote_type: str = Field(..., pattern="^(upvote|downvote)$", description="Vote type: upvote or downvote")


class ForumVoteResponse(BaseModel):
    """Schema for vote response"""
    post_id: int
    user_id: int
    vote_type: str
    created_at: datetime

    class Config:
        from_attributes = True

