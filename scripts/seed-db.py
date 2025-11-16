#!/usr/bin/env python3
"""
Seed the Crypto Curriculum database with curriculum-driven sample data.

This script ingests the markdown curriculum, generates modules, lessons,
assessments, cohorts, and sample activity records, and writes them to a
PostgreSQL database using SQLAlchemy Core.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import random
import re
import sys
import uuid
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Connection
from sqlalchemy.exc import SQLAlchemyError
from passlib.context import CryptContext

# Password hashing context (matches backend security)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Default password for all seeded users (development only)
DEFAULT_PASSWORD = "password123"

BASE_DIR = Path(__file__).resolve().parents[1]
CURRICULUM_DIR = BASE_DIR / "curriculum"
OUTLINE_FILE = CURRICULUM_DIR / "blockchain curriculum outline.md"
PART_FILES = [
    CURRICULUM_DIR / "blockchain curriculum part 1.md",
    CURRICULUM_DIR / "blockchain curriculum part 2.md",
    CURRICULUM_DIR / "blockchain curriculum part 3.md",
    CURRICULUM_DIR / "blockchain curriculum part 4.md",
]

DEFAULT_DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/crypto_curriculum"

TABLES_TO_TRUNCATE = [
    "notifications",
    "chat_messages",
    "announcements",
    "cohort_deadlines",
    "cohort_members",
    "cohorts",
    "quiz_attempts",
    "user_progress",
    "leaderboards",
    "user_achievements",
    "achievements",
    "learning_resources",
    "assessments",
    "lessons",
    "modules",
    "users",
]

MODULE_TRACKS = {
    "user": range(1, 8),
    "power-user": range(8, 11),
    "developer": range(11, 14),
    "architect": range(14, 18),
}


def new_uuid() -> str:
    return str(uuid.uuid4())


def resolve_track(module_id: int) -> str:
    """Resolve track name and return uppercase enum value for database"""
    track_map = {
        "user": "USER",
        "power-user": "ANALYST",
        "developer": "DEVELOPER",
        "architect": "ARCHITECT",
    }
    for track, module_range in MODULE_TRACKS.items():
        if module_id in module_range:
            return track_map.get(track, "USER")
    return "USER"


def load_modules_from_outline(path: Path) -> List[Dict[str, object]]:
    logging.info("Loading modules from outline: %s", path)
    if not path.exists():
        raise FileNotFoundError(f"Curriculum outline not found: {path}")

    module_pattern = re.compile(r"^##\s+Module\s+(\d+):\s*(.+)$")
    modules: List[Dict[str, object]] = []
    current: Dict[str, object] | None = None
    summary_lines: List[str] = []

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        match = module_pattern.match(line)
        if match:
            if current is not None:
                current["summary"] = " ".join(summary_lines[:6]).strip()
                modules.append(current)
            module_id = int(match.group(1))
            title = match.group(2).strip()
            current = {
                "id": module_id,
                "title": title,
                "summary": "",
            }
            summary_lines = []
            continue

        if current is not None and line:
            cleaned = line.lstrip("-*• ").strip()
            if cleaned:
                summary_lines.append(cleaned)

    if current is not None:
        current["summary"] = " ".join(summary_lines[:6]).strip()
        modules.append(current)

    modules.sort(key=lambda m: m["id"])  # type: ignore[arg-type]
    logging.info("Found %s modules in outline", len(modules))
    return modules


def load_lessons_from_curriculum(files: Iterable[Path]) -> Dict[int, List[Dict[str, object]]]:
    logging.info("Parsing lessons from curriculum parts")
    module_pattern = re.compile(r"^##\s+Module\s+(\d+):\s*(.+?)(?:\s+\(([\d.]+)h\))?$")
    lesson_pattern = re.compile(r"^###\s+(\d+\.\d+)\s+(.*)$")
    lessons_by_module: Dict[int, List[Dict[str, object]]] = {}
    current_module: int | None = None
    current_lesson: Dict[str, object] | None = None
    buffer: List[str] = []

    for file_path in files:
        if not file_path.exists():
            raise FileNotFoundError(f"Curriculum part missing: {file_path}")
        lines = file_path.read_text(encoding="utf-8").splitlines()
        for raw_line in lines:
            line = raw_line.rstrip()
            module_match = module_pattern.match(line.strip())
            if module_match:
                if current_lesson is not None and current_module is not None:
                    current_lesson["content"] = "\n".join(buffer).strip()
                    lessons_by_module.setdefault(current_module, []).append(current_lesson)
                current_module = int(module_match.group(1))
                current_lesson = None
                buffer = []
                continue

            lesson_match = lesson_pattern.match(line.strip())
            if lesson_match and current_module is not None:
                if current_lesson is not None:
                    current_lesson["content"] = "\n".join(buffer).strip()
                    lessons_by_module.setdefault(current_module, []).append(current_lesson)
                lesson_title = lesson_match.group(2).strip()
                current_lesson = {
                    "title": lesson_title,
                }
                buffer = []
                continue

            if current_lesson is not None:
                buffer.append(line)

        # Commit any pending lesson at end of file
        if current_lesson is not None and current_module is not None:
            current_lesson["content"] = "\n".join(buffer).strip()
            lessons_by_module.setdefault(current_module, []).append(current_lesson)
            current_lesson = None
            buffer = []

    logging.info("Assembled lessons for %s modules", len(lessons_by_module))
    return lessons_by_module


def reset_database(conn: Connection) -> None:
    logging.warning("Resetting database: truncating tables %s", ", ".join(TABLES_TO_TRUNCATE))
    table_list = ", ".join(TABLES_TO_TRUNCATE)
    conn.execute(text(f"TRUNCATE TABLE {table_list} RESTART IDENTITY CASCADE"))


def bulk_insert(conn: Connection, table: str, rows: List[Dict[str, object]]) -> None:
    if not rows:
        return
    keys = rows[0].keys()
    placeholders = ", ".join(f":{key}" for key in keys)
    columns = ", ".join(keys)
    stmt = text(f"INSERT INTO {table} ({columns}) VALUES ({placeholders})")
    conn.execute(stmt, rows)


def generate_modules_and_lessons(modules_outline: List[Dict[str, object]], lessons_map: Dict[int, List[Dict[str, object]]]) -> Tuple[List[Dict[str, object]], List[Dict[str, object]]]:
    module_rows: List[Dict[str, object]] = []
    lesson_rows: List[Dict[str, object]] = []
    published_cutoff = datetime.utcnow() - timedelta(days=7)
    
    # Lesson IDs must be integers (matching Lesson model: id = Column(Integer, ...))
    # Start from 1 and increment for each lesson
    lesson_id = 1

    for module in modules_outline:
        module_id = module["id"]  # type: ignore[index]
        track = resolve_track(module_id)  # type: ignore[arg-type]
        module_rows.append(
            {
                "id": module_id,
                "title": module["title"],
                "description": module.get("summary") or None,
                "track": track,
                "duration_hours": 2.0,  # Default duration for all modules
                "order_index": module_id,
                "is_active": True,
                "is_published": True,
                "prerequisites": json.dumps(list(range(1, module_id)) if module_id > 1 else []),
                "learning_objectives": json.dumps([]),
                "created_at": published_cutoff,
                "updated_at": datetime.utcnow(),
            }
        )

        lessons = lessons_map.get(module_id, [])
        for order_index, lesson in enumerate(lessons, start=1):
            lesson_rows.append(
                {
                    "id": lesson_id,
                    "module_id": module_id,
                    "title": lesson["title"],
                    "content": lesson.get("content") or "",
                    "lesson_type": "reading",
                    "order_index": order_index,
                    "estimated_minutes": 20,
                    "is_active": True,
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow(),
                }
            )
            lesson_id += 1

    logging.info("Prepared %s modules and %s lessons", len(module_rows), len(lesson_rows))
    return module_rows, lesson_rows


def generate_assessments(modules: List[Dict[str, object]]) -> List[Dict[str, object]]:
    assessments: List[Dict[str, object]] = []
    mc_template = [
        ("A", "Concept application scenario"),
        ("B", "Definition or terminology check"),
        ("C", "Comparison question"),
        ("D", "Common misconception"),
    ]
    
    # Assessment IDs must be integers (matching Assessment model: id = Column(Integer, ...))
    # Start from 1 and increment for each assessment
    assessment_id = 1

    for module in modules:
        module_id = module["id"]
        module_title = module["title"]
        base_question = f"in Module {module_id}: {module_title}"
        distribution = [
            ("MULTIPLE_CHOICE", 3),  # Use uppercase to match database enum
            ("TRUE_FALSE", 2),
            ("SHORT_ANSWER", 3),
            ("CODING_TASK", 2),
        ]
        order_index = 1
        for question_type, count in distribution:
            for i in range(count):
                question_text = f"Placeholder question {order_index} {base_question}"
                options = None
                correct_answer = None

                if question_type == "MULTIPLE_CHOICE":
                    choices = {key: f"{value} ({module_title})" for key, value in mc_template}
                    options = json.dumps(choices)
                    correct_answer = random.choice(list(choices.keys()))
                elif question_type == "TRUE_FALSE":
                    correct_answer = random.choice(["True", "False"])
                else:
                    correct_answer = ""

                assessments.append(
                    {
                        "id": assessment_id,
                        "module_id": module_id,
                        "question_text": question_text,
                        "question_type": question_type,
                        "options": options,
                        "correct_answer": correct_answer,
                        "explanation": f"Explanation for {question_type} question {order_index} in module {module_id}.",
                        "points": 10,
                        "order_index": order_index,
                        "is_active": True,
                        "created_at": datetime.utcnow(),
                    }
                )
                assessment_id += 1
                order_index += 1

    logging.info("Prepared %s assessments", len(assessments))
    return assessments


def generate_users() -> Tuple[List[Dict[str, object]], Dict[str, str]]:
    now = datetime.utcnow()
    
    # Generate a real bcrypt hash for the default password
    # This matches the backend's password hashing (bcrypt)
    hashed_password = pwd_context.hash(DEFAULT_PASSWORD)
    
    # User IDs must be integers (matching User model: id = Column(Integer, ...))
    # Start from 1 for consistency
    user_id = 1
    
    users = [
        {
            "id": user_id,
            "email": "admin@example.com",
            "username": "admin_lead",
            "hashed_password": hashed_password,
            "full_name": "Avery Admin",
            "role": "ADMIN",
            "is_active": True,
            "is_verified": True,
            "created_at": now,
            "updated_at": now,
        },
    ]
    user_id += 1
    
    users.append({
        "id": user_id,
            "email": "instructor.alex@example.com",
            "username": "alex_instructor",
        "hashed_password": hashed_password,
            "full_name": "Alex Instructor",
        "role": "INSTRUCTOR",
            "is_active": True,
        "is_verified": True,
            "created_at": now,
            "updated_at": now,
    })
    user_id += 1
    
    users.append({
        "id": user_id,
            "email": "instructor.jordan@example.com",
            "username": "jordan_instructor",
        "hashed_password": hashed_password,
            "full_name": "Jordan Instructor",
        "role": "INSTRUCTOR",
            "is_active": True,
        "is_verified": True,
            "created_at": now,
            "updated_at": now,
    })
    user_id += 1

    student_names = [
        ("casey.student@example.com", "Casey Learner"),
        ("morgan.student@example.com", "Morgan Analyst"),
        ("riley.student@example.com", "Riley Builder"),
        ("jamie.student@example.com", "Jamie Strategist"),
        ("taylor.student@example.com", "Taylor Innovator"),
    ]

    for index, (email, full_name) in enumerate(student_names, start=1):
        users.append(
            {
                "id": user_id,
                "email": email,
                "username": f"student_{index}",
                "hashed_password": hashed_password,
                "full_name": full_name,
                "role": "STUDENT",
                "is_active": True,
                "is_verified": True,
                "created_at": now,
                "updated_at": now,
            }
        )
        user_id += 1

    user_lookup = {user["username"]: user["id"] for user in users}
    logging.info("Prepared %s users", len(users))
    logging.info("Default password for all seeded users: %s", DEFAULT_PASSWORD)
    return users, user_lookup


def generate_cohorts(user_lookup: Dict[str, str]) -> Tuple[List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]]]:
    now = datetime.utcnow()
    # All IDs must be integers - start counters
    cohort_id = 1
    member_id = 1
    deadline_id = 1
    announcement_id = 1
    
    cohorts = [
        {
            "id": cohort_id,
            "name": "Spring 2025 Cohort",
            "description": "Flagship cohort for the spring term.",
            "start_date": datetime(2025, 3, 10),
            "end_date": datetime(2025, 6, 30),
            "is_active": True,
            "created_by": user_lookup["alex_instructor"],
            "created_at": now,
            "updated_at": now,
        },
        {
            "id": cohort_id + 1,
            "name": "Summer 2025 Cohort",
            "description": "Accelerated cohort focused on advanced topics.",
            "start_date": datetime(2025, 7, 8),
            "end_date": datetime(2025, 10, 1),
            "is_active": False,
            "created_by": user_lookup["jordan_instructor"],
            "created_at": now,
            "updated_at": now,
        },
    ]
    cohort_id += 2  # Increment for both cohorts

    cohort_members: List[Dict[str, object]] = []
    cohort_deadlines: List[Dict[str, object]] = []
    announcements: List[Dict[str, object]] = []

    for cohort in cohorts:
        current_cohort_id = cohort["id"]
        instructor = cohort["created_by"]
        cohort_members.append(
            {
                "id": member_id,
                "cohort_id": current_cohort_id,
                "user_id": instructor,
                "role": "INSTRUCTOR",
                "joined_at": now,
            }
        )
        member_id += 1

    students = [username for username in user_lookup if username.startswith("student_")]
    for idx, student_username in enumerate(students):
        current_cohort_id = cohorts[idx % len(cohorts)]["id"]
        cohort_members.append(
            {
                "id": member_id,
                "cohort_id": current_cohort_id,
                "user_id": user_lookup[student_username],
                "role": "STUDENT",
                "joined_at": now - timedelta(days=random.randint(1, 14)),
            }
        )
        member_id += 1

    for cohort in cohorts:
        cohort_deadlines.append(
            {
                "id": deadline_id,
                "cohort_id": cohort["id"],
                "module_id": 3,
                "deadline_date": cohort["start_date"] + timedelta(days=30),
                "is_mandatory": True,
                "description": "Complete foundational modules and assessments.",
                "created_by": cohort["created_by"],
                "created_at": now,
            }
        )
        deadline_id += 1
        cohort_deadlines.append(
            {
                "id": deadline_id,
                "cohort_id": cohort["id"],
                "module_id": 8,
                "deadline_date": cohort["start_date"] + timedelta(days=60),
                "is_mandatory": False,
                "description": "Optional on-chain analysis workshop.",
                "created_by": cohort["created_by"],
                "created_at": now,
            }
        )
        deadline_id += 1

        announcements.append(
            {
                "id": announcement_id,
                "cohort_id": cohort["id"],
                "author_id": cohort["created_by"],
                "title": "Welcome to the cohort!",
                "content": "Review the orientation materials and introduce yourself in the forum.",
                "is_pinned": True,
                "priority": "high",
                "created_at": now,
                "updated_at": now,
            }
        )
        announcement_id += 1

    announcements.append(
        {
            "id": announcement_id,
            "cohort_id": None,
            "author_id": user_lookup["admin_lead"],
            "title": "Platform Update",
            "content": "New grading queue tools and notifications are now live.",
            "is_pinned": False,
            "priority": "normal",
            "created_at": now,
            "updated_at": now,
        }
    )

    logging.info("Prepared cohorts (%s), members (%s), deadlines (%s), announcements (%s)", len(cohorts), len(cohort_members), len(cohort_deadlines), len(announcements))
    return cohorts, cohort_members, cohort_deadlines, announcements


def generate_progress_and_attempts(user_lookup: Dict[str, str], modules: List[Dict[str, object]], assessments: List[Dict[str, object]]) -> Tuple[List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]]]:
    progress_rows: List[Dict[str, object]] = []
    attempts_rows: List[Dict[str, object]] = []
    notifications: List[Dict[str, object]] = []
    chat_messages: List[Dict[str, object]] = []
    now = datetime.utcnow()
    # All IDs must be integers - start counters
    progress_id = 1
    attempt_id = 1
    notification_id = 1
    chat_message_id = 1

    student_ids = [user_lookup[f"student_{idx}"] for idx in range(1, 6)]

    assessments_by_module: Dict[int, List[Dict[str, object]]] = {}
    for assessment in assessments:
        assessments_by_module.setdefault(assessment["module_id"], []).append(assessment)

    for student_id in student_ids:
        completed_modules = random.sample([m["id"] for m in modules if m["id"] <= 6], k=3)
        for module_id in completed_modules:
            progress_rows.append(
                {
                    "id": progress_id,
                    "user_id": student_id,
                    "module_id": module_id,
                    "status": "COMPLETED",
                    "completion_percentage": 100.0,
                    "started_at": now - timedelta(days=30),
                    "completed_at": now - timedelta(days=15),
                    "last_accessed_at": now - timedelta(days=1),
                }
            )
            progress_id += 1

        in_progress_module = random.choice([m["id"] for m in modules if m["id"] > 3])
        progress_rows.append(
            {
                "id": progress_id,
                "user_id": student_id,
                "module_id": in_progress_module,
                    "status": "IN_PROGRESS",
                    "completion_percentage": round(random.uniform(20, 70), 2),
                "started_at": now - timedelta(days=7),
                "completed_at": None,
                    "last_accessed_at": now - timedelta(hours=random.randint(5, 48)),
            }
        )

        for module_id in completed_modules[:2]:
            module_assessments = assessments_by_module.get(module_id, [])[:2]
            for assessment in module_assessments:
                is_manual = assessment["question_type"] in ("SHORT_ANSWER", "CODING_TASK")
                review_status = "PENDING" if is_manual else "GRADED"
                graded_by = user_lookup["alex_instructor"] if not is_manual else None
                graded_at = now - timedelta(days=1) if not is_manual else None
                current_attempt_id = attempt_id
                attempts_rows.append(
                    {
                        "id": current_attempt_id,
                        "user_id": student_id,
                        "assessment_id": assessment["id"],
                        "user_answer": "Sample response",
                        "is_correct": None if is_manual else random.choice([True, False]),
                        "points_earned": None if is_manual else random.randint(6, 10),
                        "review_status": review_status,
                        "graded_by": graded_by,
                        "feedback": None if is_manual else "Automated grading completed.",
                        "partial_credit": False,
                        "graded_at": graded_at,
                        "attempted_at": now - timedelta(days=random.randint(1, 5)),
                        "time_spent_seconds": random.randint(30, 300),
                    }
                )
                attempt_id += 1

                if review_status == "pending":
                    notifications.append(
                        {
                            "id": notification_id,
                            "user_id": user_lookup["alex_instructor"],
                            "type": "assessment_graded",
                            "title": "Grading Needed",
                            "message": f"Manual grading required for attempt {current_attempt_id}.",
                            "link": f"/grading/{current_attempt_id}",
                            "is_read": False,
                            "created_at": now,
                            "read_at": None,
                        }
                    )
                    notification_id += 1

        notifications.append(
            {
                "id": notification_id,
                "user_id": student_id,
                "type": "module_unlocked",
                "title": "Next module unlocked",
                "message": "Great work! The next module is now available.",
                "link": "/modules/next",
                "is_read": False,
                "created_at": now - timedelta(days=2),
                "read_at": None,
            }
        )
        notification_id += 1

        chat_messages.append(
            {
                "id": chat_message_id,
                "user_id": student_id,
                "message": "Can you clarify smart contracts again?",
                "response": "Smart contracts are self-executing code on the blockchain.",
                "context": json.dumps({"module": 1, "lesson": "1.4 Smart Contracts"}),
                "suggested_lessons": None,
                "escalated": False,
                "created_at": now - timedelta(hours=random.randint(1, 24)),
            }
        )
        progress_id += 1
        chat_message_id += 1

    logging.info("Prepared %s progress records, %s quiz attempts, %s notifications, %s chat messages", len(progress_rows), len(attempts_rows), len(notifications), len(chat_messages))
    return progress_rows, attempts_rows, notifications, chat_messages


def generate_leaderboards(user_lookup: Dict[str, str], cohorts: List[Dict[str, object]]) -> List[Dict[str, object]]:
    now = datetime.utcnow()
    leaderboard_rows: List[Dict[str, object]] = []
    categories = ["progress", "scores", "engagement"]
    leaderboard_id = 1

    for cohort in cohorts:
        cohort_id = cohort["id"]
        for rank, student_index in enumerate(range(1, 6), start=1):
            student_id = user_lookup.get(f"student_{student_index}")
            if not student_id:
                continue
            for category in categories:
                leaderboard_rows.append(
                    {
                        "id": leaderboard_id,
                        "cohort_id": cohort_id,
                        "user_id": student_id,
                        "category": category,
                        "score": Decimal(f"{random.uniform(60, 100):.2f}"),
                        "rank": rank,
                        "updated_at": now,
                    }
                )
                leaderboard_id += 1

    logging.info("Prepared %s leaderboard rows", len(leaderboard_rows))
    return leaderboard_rows


def generate_achievements() -> Tuple[List[Dict[str, object]], List[Dict[str, object]]]:
    """Generate 20+ achievements for gamification"""
    now = datetime.utcnow()
    achievement_id = 1
    achievements = []
    
    # Module Completion Achievements
    achievements.append({
        "id": achievement_id,
        "name": "First Steps",
        "description": "Complete Module 1: Introduction to Cryptocurrency",
        "icon": "star",
        "category": "completion",
        "criteria": json.dumps({"module_completion": {"module_id": 1}}),
        "progress_tracking": json.dumps({"module_id": 1, "completed": False}),
        "points": 10,
        "is_active": True,
    })
    achievement_id += 1
    
    achievements.append({
        "id": achievement_id,
        "name": "Blockchain Basics",
        "description": "Complete Module 2: Blockchain Fundamentals",
        "icon": "link",
        "category": "completion",
        "criteria": json.dumps({"module_completion": {"module_id": 2}}),
        "progress_tracking": json.dumps({"module_id": 2, "completed": False}),
        "points": 15,
        "is_active": True,
    })
    achievement_id += 1
    
    achievements.append({
        "id": achievement_id,
        "name": "Wallet Wizard",
        "description": "Complete Module 3: Wallets and Security",
        "icon": "wallet",
        "category": "completion",
        "criteria": json.dumps({"module_completion": {"module_id": 3}}),
        "progress_tracking": json.dumps({"module_id": 3, "completed": False}),
        "points": 15,
        "is_active": True,
    })
    achievement_id += 1
    
    # Perfect Score Achievements
    achievements.append({
        "id": achievement_id,
        "name": "Perfect Score",
        "description": "Score 100% on any assessment",
        "icon": "trophy",
        "category": "score",
        "criteria": json.dumps({"perfect_score": {"any_assessment": True}}),
        "progress_tracking": json.dumps({"best_score": 0, "target": 100}),
        "points": 50,
        "is_active": True,
    })
    achievement_id += 1
    
    achievements.append({
        "id": achievement_id,
        "name": "Module Master",
        "description": "Score 100% on Module 1 assessment",
        "icon": "medal",
        "category": "score",
        "criteria": json.dumps({"perfect_score": {"module_id": 1}}),
        "progress_tracking": json.dumps({"module_id": 1, "score": 0, "target": 100}),
        "points": 25,
        "is_active": True,
    })
    achievement_id += 1
    
    achievements.append({
        "id": achievement_id,
        "name": "High Achiever",
        "description": "Score 90% or higher on any assessment",
        "icon": "award",
        "category": "score",
        "criteria": json.dumps({"score_threshold": {"min_score": 90}}),
        "progress_tracking": json.dumps({"best_score": 0, "target": 90}),
        "points": 30,
        "is_active": True,
    })
    achievement_id += 1
    
    # Track Completion Achievements
    achievements.append({
        "id": achievement_id,
        "name": "Beginner Track Complete",
        "description": "Complete all modules in the Beginner Track (Modules 1-7)",
        "icon": "certificate",
        "category": "completion",
        "criteria": json.dumps({"track_completion": {"track_name": "beginner"}}),
        "progress_tracking": json.dumps({"track": "beginner", "completed_modules": 0, "total": 7}),
        "points": 100,
        "is_active": True,
    })
    achievement_id += 1
    
    achievements.append({
        "id": achievement_id,
        "name": "Power User",
        "description": "Complete all modules in the Power User/Analyst Track (Modules 8-10)",
        "icon": "chart-line",
        "category": "completion",
        "criteria": json.dumps({"track_completion": {"track_name": "power_user"}}),
        "progress_tracking": json.dumps({"track": "power_user", "completed_modules": 0, "total": 3}),
        "points": 150,
        "is_active": True,
    })
    achievement_id += 1
    
    achievements.append({
        "id": achievement_id,
        "name": "Developer",
        "description": "Complete all modules in the Developer Track (Modules 11-13)",
        "icon": "code",
        "category": "completion",
        "criteria": json.dumps({"track_completion": {"track_name": "developer"}}),
        "progress_tracking": json.dumps({"track": "developer", "completed_modules": 0, "total": 3}),
        "points": 200,
        "is_active": True,
    })
    achievement_id += 1
    
    achievements.append({
        "id": achievement_id,
        "name": "Architect",
        "description": "Complete all modules in the Architect/Builder Track (Modules 14-17)",
        "icon": "building",
        "category": "completion",
        "criteria": json.dumps({"track_completion": {"track_name": "architect"}}),
        "progress_tracking": json.dumps({"track": "architect", "completed_modules": 0, "total": 4}),
        "points": 250,
        "is_active": True,
    })
    achievement_id += 1
    
    achievements.append({
        "id": achievement_id,
        "name": "Master Certificate",
        "description": "Complete all 4 tracks - the ultimate achievement!",
        "icon": "crown",
        "category": "completion",
        "criteria": json.dumps({"track_completion": {"all_tracks": True}}),
        "progress_tracking": json.dumps({"tracks_completed": 0, "total": 4}),
        "points": 500,
        "is_active": True,
    })
    achievement_id += 1
    
    # Forum Engagement Achievements
    achievements.append({
        "id": achievement_id,
        "name": "Forum Helper",
        "description": "Help 10 peers in the forum (posts marked as solved or upvoted)",
        "icon": "hand-holding-heart",
        "category": "engagement",
        "criteria": json.dumps({"forum_help": {"posts": 10}}),
        "progress_tracking": json.dumps({"forum_help": {"current": 0, "target": 10}}),
        "points": 25,
        "is_active": True,
    })
    achievement_id += 1
    
    achievements.append({
        "id": achievement_id,
        "name": "Community Champion",
        "description": "Help 25 peers in the forum",
        "icon": "users",
        "category": "engagement",
        "criteria": json.dumps({"forum_help": {"posts": 25}}),
        "progress_tracking": json.dumps({"forum_help": {"current": 0, "target": 25}}),
        "points": 75,
        "is_active": True,
    })
    achievement_id += 1
    
    achievements.append({
        "id": achievement_id,
        "name": "Forum Expert",
        "description": "Help 50 peers in the forum",
        "icon": "star",
        "category": "engagement",
        "criteria": json.dumps({"forum_help": {"posts": 50}}),
        "progress_tracking": json.dumps({"forum_help": {"current": 0, "target": 50}}),
        "points": 150,
        "is_active": True,
    })
    achievement_id += 1
    
    # Streak Achievements
    achievements.append({
        "id": achievement_id,
        "name": "7-Day Streak",
        "description": "Maintain a 7-day learning streak",
        "icon": "fire",
        "category": "engagement",
        "criteria": json.dumps({"streak": {"days": 7}}),
        "progress_tracking": json.dumps({"streak_days": 0, "target": 7}),
        "points": 50,
        "is_active": True,
    })
    achievement_id += 1
    
    achievements.append({
        "id": achievement_id,
        "name": "30-Day Streak",
        "description": "Maintain a 30-day learning streak",
        "icon": "flame",
        "category": "engagement",
        "criteria": json.dumps({"streak": {"days": 30}}),
        "progress_tracking": json.dumps({"streak_days": 0, "target": 30}),
        "points": 200,
        "is_active": True,
    })
    achievement_id += 1
    
    # Milestone Achievements
    achievements.append({
        "id": achievement_id,
        "name": "Halfway There",
        "description": "Complete 9 modules (half of the curriculum)",
        "icon": "route",
        "category": "completion",
        "criteria": json.dumps({"module_completion": {"any_module": True, "count": 9}}),
        "progress_tracking": json.dumps({"completed_modules": 0, "target": 9}),
        "points": 100,
        "is_active": True,
    })
    achievement_id += 1
    
    achievements.append({
        "id": achievement_id,
        "name": "Module Explorer",
        "description": "Complete 5 different modules",
        "icon": "compass",
        "category": "completion",
        "criteria": json.dumps({"module_completion": {"any_module": True, "count": 5}}),
        "progress_tracking": json.dumps({"completed_modules": 0, "target": 5}),
        "points": 50,
        "is_active": True,
    })
    achievement_id += 1
    
    achievements.append({
        "id": achievement_id,
        "name": "Dedicated Learner",
        "description": "Complete 15 modules",
        "icon": "graduation-cap",
        "category": "completion",
        "criteria": json.dumps({"module_completion": {"any_module": True, "count": 15}}),
        "progress_tracking": json.dumps({"completed_modules": 0, "target": 15}),
        "points": 200,
        "is_active": True,
    })
    achievement_id += 1
    
    achievements.append({
        "id": achievement_id,
        "name": "Curiosity Killed the Cat",
        "description": "Complete your first module",
        "icon": "lightbulb",
        "category": "completion",
        "criteria": json.dumps({"module_completion": {"any_module": True}}),
        "progress_tracking": json.dumps({"completed_modules": 0, "target": 1}),
        "points": 20,
        "is_active": True,
    })
    achievement_id += 1
    
    achievements.append({
        "id": achievement_id,
        "name": "Consistent Performer",
        "description": "Score 80% or higher on 5 different assessments",
        "icon": "chart-bar",
        "category": "score",
        "criteria": json.dumps({"score_threshold": {"min_score": 80, "count": 5}}),
        "progress_tracking": json.dumps({"high_scores": 0, "target": 5}),
        "points": 75,
        "is_active": True,
    })
    achievement_id += 1

    user_achievements = []
    logging.info("Prepared %s achievements", len(achievements))
    return achievements, user_achievements


def generate_learning_resources(modules: List[Dict[str, object]]) -> List[Dict[str, object]]:
    now = datetime.utcnow()
    resources: List[Dict[str, object]] = []
    resource_id = 1
    samples = [
        ("video", "beginner"),
        ("article", "intermediate"),
        ("tutorial", "advanced"),
    ]
    for module in modules[:6]:
        for resource_type, difficulty in samples:
            resources.append(
                {
                    "id": resource_id,
                    "module_id": module["id"],
                    "title": f"{module['title']} {resource_type.title()} Resource",
                    "url": f"https://example.com/{module['id']}/{resource_type}",
                    "resource_type": resource_type,
                    "difficulty": difficulty,
                    "upvotes": random.randint(0, 25),
                    "added_by": None,
                    "created_at": now,
                }
            )
            resource_id += 1
    logging.info("Prepared %s learning resources", len(resources))
    return resources


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Seed the Crypto Curriculum database with sample data.")
    parser.add_argument("--reset", action="store_true", help="Truncate tables before seeding.")
    parser.add_argument("--database-url", default=os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL), help="SQLAlchemy database URL.")
    parser.add_argument("--commit", action="store_true", help="Apply changes. Without this flag, run in dry-run mode.")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging.")
    return parser.parse_args(argv)


def main(argv: List[str]) -> int:
    args = parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format="%(levelname)s %(message)s")

    try:
        modules_outline = load_modules_from_outline(OUTLINE_FILE)
        lessons_map = load_lessons_from_curriculum(PART_FILES)
        modules_data, lessons_data = generate_modules_and_lessons(modules_outline, lessons_map)
        assessments_data = generate_assessments(modules_data)
        users_data, user_lookup = generate_users()
        cohorts, cohort_members, cohort_deadlines, announcements = generate_cohorts(user_lookup)
        progress_data, attempts_data, notifications_data, chat_messages_data = generate_progress_and_attempts(user_lookup, modules_data, assessments_data)
        leaderboard_data = generate_leaderboards(user_lookup, cohorts)
        achievements_data, user_achievements_data = generate_achievements()
        learning_resources_data = generate_learning_resources(modules_data)
    except FileNotFoundError as exc:
        logging.error("Missing curriculum source: %s", exc)
        return 1

    if not args.commit:
        logging.warning("Dry run complete. Use --commit to apply changes.")
        return 0

    logging.info("Connecting to database: %s", args.database_url)
    engine = create_engine(args.database_url, future=True)

    try:
        with engine.begin() as conn:
            if args.reset:
                reset_database(conn)

            bulk_insert(conn, "users", users_data)
            bulk_insert(conn, "modules", modules_data)
            bulk_insert(conn, "lessons", lessons_data)
            bulk_insert(conn, "assessments", assessments_data)
            bulk_insert(conn, "achievements", achievements_data)
            bulk_insert(conn, "user_achievements", user_achievements_data)
            bulk_insert(conn, "cohorts", cohorts)
            bulk_insert(conn, "cohort_members", cohort_members)
            bulk_insert(conn, "cohort_deadlines", cohort_deadlines)
            bulk_insert(conn, "announcements", announcements)
            bulk_insert(conn, "user_progress", progress_data)
            bulk_insert(conn, "quiz_attempts", attempts_data)
            bulk_insert(conn, "notifications", notifications_data)
            bulk_insert(conn, "chat_messages", chat_messages_data)
            bulk_insert(conn, "leaderboards", leaderboard_data)
            bulk_insert(conn, "learning_resources", learning_resources_data)
    except SQLAlchemyError as exc:
        logging.error("Database error while seeding: %s", exc)
        return 1

    logging.info("Database seed complete.")
    logging.info(
        "Seeded datasets -> users:%s modules:%s lessons:%s assessments:%s cohorts:%s attempts:%s notifications:%s",
        len(users_data),
        len(modules_data),
        len(lessons_data),
        len(assessments_data),
        len(cohorts),
        len(attempts_data),
        len(notifications_data),
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
