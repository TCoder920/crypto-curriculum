"""Module and Lesson models for curriculum content"""
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.backend.core.database import Base
import enum


class Track(str, enum.Enum):
    """Curriculum track enumeration"""
    USER = "user"
    ANALYST = "analyst"
    DEVELOPER = "developer"
    ARCHITECT = "architect"


class Module(Base):
    """Curriculum module model"""
    __tablename__ = "modules"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Content
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    track = Column(SQLEnum(Track), nullable=False, index=True)
    order_index = Column(Integer, nullable=False, index=True)
    duration_hours = Column(Float, nullable=False)
    
    # Metadata
    prerequisites = Column(JSON, nullable=True)  # Array of module IDs
    learning_objectives = Column(JSON, nullable=True)  # Array of objectives
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_published = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    lessons = relationship("Lesson", back_populates="module", cascade="all, delete-orphan")
    assessments = relationship("Assessment", back_populates="module", cascade="all, delete-orphan")
    # user_progress = relationship("UserProgress", back_populates="module")
    
    def __repr__(self):
        return f"<Module(id={self.id}, title='{self.title}', track='{self.track}')>"


class Lesson(Base):
    """Individual lesson within a module"""
    __tablename__ = "lessons"
    
    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Content
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)  # Markdown or HTML
    order_index = Column(Integer, nullable=False)
    estimated_minutes = Column(Integer, nullable=True)
    
    # Metadata
    lesson_type = Column(String(50), nullable=False, default="reading")  # 'text', 'video', 'interactive', 'code'
    media_url = Column(String(500), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    module = relationship("Module", back_populates="lessons")
    
    def __repr__(self):
        return f"<Lesson(id={self.id}, title='{self.title}', module_id={self.module_id})>"


