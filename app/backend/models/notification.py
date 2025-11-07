"""Notification and chat models"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.backend.core.database import Base


class Notification(Base):
    """Stores user notifications"""
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Content
    type = Column(String(50), nullable=False)  # 'assessment_graded', 'forum_reply', 'announcement', 'module_unlocked'
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    link = Column(String(500), nullable=True)
    
    # Status
    is_read = Column(Boolean, default=False, nullable=False, index=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    read_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    # user = relationship("User")
    
    def __repr__(self):
        return f"<Notification(id={self.id}, user_id={self.user_id}, type='{self.type}', is_read={self.is_read})>"


class ChatMessage(Base):
    """Logs AI assistant chat sessions"""
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Content
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=True)
    context = Column(JSON, nullable=True)  # Stores current module/lesson info
    suggested_lessons = Column(JSON, nullable=True)  # Array of lesson IDs
    
    # Metadata
    escalated = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    
    # Relationships
    # user = relationship("User")
    
    def __repr__(self):
        return f"<ChatMessage(id={self.id}, user_id={self.user_id}, escalated={self.escalated})>"


class LearningResource(Base):
    """External resources linked to modules"""
    __tablename__ = "learning_resources"
    
    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.id", ondelete="CASCADE"), nullable=True, index=True)
    
    # Content
    title = Column(String(200), nullable=False)
    url = Column(String(500), nullable=False)
    resource_type = Column(String(50), nullable=True)  # 'video', 'article', 'tutorial', 'documentation'
    difficulty = Column(String(20), nullable=True)  # 'beginner', 'intermediate', 'advanced'
    upvotes = Column(Integer, default=0, nullable=False)
    
    # Metadata
    added_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<LearningResource(id={self.id}, title='{self.title}', module_id={self.module_id})>"


