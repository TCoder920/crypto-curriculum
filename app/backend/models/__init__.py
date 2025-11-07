"""Import all models for Alembic to detect"""
from app.backend.models.user import User, UserRole
from app.backend.models.module import Module, Lesson, Track
from app.backend.models.assessment import Assessment, QuestionType
from app.backend.models.progress import UserProgress, QuizAttempt, ProgressStatus, ReviewStatus
from app.backend.models.cohort import Cohort, CohortMember, CohortDeadline, Announcement, CohortRole
from app.backend.models.forum import ForumPost, ForumVote
from app.backend.models.achievement import Achievement, UserAchievement, Leaderboard
from app.backend.models.notification import Notification, ChatMessage, LearningResource

__all__ = [
    # User
    "User",
    "UserRole",
    # Module
    "Module",
    "Lesson",
    "Track",
    # Assessment
    "Assessment",
    "QuestionType",
    # Progress
    "UserProgress",
    "QuizAttempt",
    "ProgressStatus",
    "ReviewStatus",
    # Cohort
    "Cohort",
    "CohortMember",
    "CohortDeadline",
    "Announcement",
    "CohortRole",
    # Forum
    "ForumPost",
    "ForumVote",
    # Achievement
    "Achievement",
    "UserAchievement",
    "Leaderboard",
    # Notification
    "Notification",
    "ChatMessage",
    "LearningResource",
]


