"""Cohort and related models"""
from sqlalchemy import Column, Integer, String, Text, Date, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.backend.core.database import Base
import enum


class CohortRole(str, enum.Enum):
    """Cohort member role"""
    STUDENT = "student"
    INSTRUCTOR = "instructor"


class Cohort(Base):
    """Represents classes or course offerings"""
    __tablename__ = "cohorts"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Content
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    
    # Metadata
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    # members = relationship("CohortMember", back_populates="cohort", cascade="all, delete-orphan")
    # deadlines = relationship("CohortDeadline", back_populates="cohort", cascade="all, delete-orphan")
    # announcements = relationship("Announcement", back_populates="cohort", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Cohort(id={self.id}, name='{self.name}')>"


class CohortMember(Base):
    """Links students and instructors to cohorts"""
    __tablename__ = "cohort_members"
    
    id = Column(Integer, primary_key=True, index=True)
    cohort_id = Column(Integer, ForeignKey("cohorts.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Role in cohort
    role = Column(String(20), nullable=False)  # 'student', 'instructor'
    
    # Timestamps
    joined_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Unique constraint
    __table_args__ = (
        UniqueConstraint('cohort_id', 'user_id', name='uq_cohort_user'),
    )
    
    # Relationships
    # cohort = relationship("Cohort", back_populates="members")
    # user = relationship("User")
    
    def __repr__(self):
        return f"<CohortMember(cohort_id={self.cohort_id}, user_id={self.user_id}, role='{self.role}')>"


class CohortDeadline(Base):
    """Tracks important milestone dates per cohort"""
    __tablename__ = "cohort_deadlines"
    
    id = Column(Integer, primary_key=True, index=True)
    cohort_id = Column(Integer, ForeignKey("cohorts.id", ondelete="CASCADE"), nullable=False, index=True)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=True)
    
    # Content
    deadline_date = Column(Date, nullable=False, index=True)
    description = Column(Text, nullable=True)
    is_mandatory = Column(Boolean, default=True, nullable=False)
    
    # Metadata
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    # cohort = relationship("Cohort", back_populates="deadlines")
    # module = relationship("Module")
    
    def __repr__(self):
        return f"<CohortDeadline(id={self.id}, cohort_id={self.cohort_id}, deadline_date='{self.deadline_date}')>"


class Announcement(Base):
    """Platform and cohort announcements"""
    __tablename__ = "announcements"
    
    id = Column(Integer, primary_key=True, index=True)
    cohort_id = Column(Integer, ForeignKey("cohorts.id", ondelete="CASCADE"), nullable=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Content
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    is_pinned = Column(Boolean, default=False, nullable=False, index=True)
    priority = Column(String(20), default="normal", nullable=False)  # 'low', 'normal', 'high', 'urgent'
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    # cohort = relationship("Cohort", back_populates="announcements")
    # author = relationship("User")
    
    def __repr__(self):
        return f"<Announcement(id={self.id}, title='{self.title}', cohort_id={self.cohort_id})>"


