"""Forum and discussion models"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.backend.core.database import Base


class ForumPost(Base):
    """Discussion forums for each module"""
    __tablename__ = "forum_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.id", ondelete="CASCADE"), nullable=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    parent_post_id = Column(Integer, ForeignKey("forum_posts.id", ondelete="CASCADE"), nullable=True, index=True)  # NULL = top-level
    
    # Content
    title = Column(String(200), nullable=True)  # NULL if reply
    content = Column(Text, nullable=False)
    is_pinned = Column(Boolean, default=False, nullable=False, index=True)
    is_solved = Column(Boolean, default=False, nullable=False)
    upvotes = Column(Integer, default=0, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    # module = relationship("Module")
    # user = relationship("User")
    # parent_post = relationship("ForumPost", remote_side=[id], backref="replies")
    # votes = relationship("ForumVote", back_populates="post", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<ForumPost(id={self.id}, title='{self.title}', module_id={self.module_id})>"


class ForumVote(Base):
    """Track upvotes/downvotes on forum posts"""
    __tablename__ = "forum_votes"
    
    post_id = Column(Integer, ForeignKey("forum_posts.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    vote_type = Column(String(10), nullable=False)  # 'upvote', 'downvote'
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    # post = relationship("ForumPost", back_populates="votes")
    # user = relationship("User")
    
    def __repr__(self):
        return f"<ForumVote(post_id={self.post_id}, user_id={self.user_id}, vote_type='{self.vote_type}')>"


