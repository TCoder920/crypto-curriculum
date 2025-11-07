import asyncio
from datetime import datetime
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.core.database import AsyncSessionLocal
from app.backend.models.user import User, UserRole
from app.backend.models.module import Module, Lesson, Track
from app.backend.models.assessment import Assessment, QuestionType


async def seed_users(session: AsyncSession) -> List[User]:
    users: List[User] = []

    admin = User(
        email="admin@example.com",
        hashed_password="dev-only-placeholder",
        username="admin_lead",
        full_name="Avery Admin",
        role=UserRole.ADMIN,
        is_active=True,
        is_verified=True,
        last_login=datetime.utcnow(),
    )
    users.append(admin)

    instructor = User(
        email="instructor.alex@example.com",
        hashed_password="dev-only-placeholder",
        username="alex_instructor",
        full_name="Alex Instructor",
        role=UserRole.INSTRUCTOR,
        is_active=True,
        is_verified=True,
    )
    users.append(instructor)

    student = User(
        email="student.casey@example.com",
        hashed_password="dev-only-placeholder",
        username="student_1",
        full_name="Casey Learner",
        role=UserRole.STUDENT,
        is_active=True,
        is_verified=True,
    )
    users.append(student)

    session.add_all(users)
    await session.flush()
    return users


def resolve_track(module_id: int) -> Track:
    if 1 <= module_id <= 7:
        return Track.USER
    if 8 <= module_id <= 10:
        return Track.ANALYST
    if 11 <= module_id <= 13:
        return Track.DEVELOPER
    return Track.ARCHITECT


async def seed_modules_lessons(session: AsyncSession) -> List[Module]:
    modules: List[Module] = []
    for module_id in range(1, 18):
        module = Module(
            id=module_id,  # fixed id to match curriculum
            title=f"Module {module_id}",
            description=f"Auto-seeded description for module {module_id}",
            track=resolve_track(module_id),
            order_index=module_id,
            duration_hours=2.0,
            prerequisites=list(range(1, module_id)) if module_id > 1 else [],
            learning_objectives=[f"Objective {i}" for i in range(1, 4)],
            is_active=True,
            is_published=True,
        )
        # minimal lessons
        module.lessons = [
            Lesson(
                title=f"{module.title} - Lesson 1",
                content=f"# {module.title} Lesson 1\n\nThis is sample content for lesson 1.",
                order_index=1,
                estimated_minutes=20,
                lesson_type="reading",
                is_active=True,
            ),
            Lesson(
                title=f"{module.title} - Lesson 2",
                content=f"# {module.title} Lesson 2\n\nThis is sample content for lesson 2.",
                order_index=2,
                estimated_minutes=20,
                lesson_type="reading",
                is_active=True,
            ),
        ]
        modules.append(module)

    session.add_all(modules)
    await session.flush()
    return modules


async def seed_assessments(session: AsyncSession, modules: List[Module]) -> None:
    assessments: List[Assessment] = []
    for module in modules:
        # 2 MC + 1 TF + 1 Short Answer per module (sample)
        assessments.extend(
            [
                Assessment(
                    module_id=module.id,
                    question_text=f"What is the key concept of {module.title}?",
                    question_type=QuestionType.MULTIPLE_CHOICE,
                    order_index=1,
                    points=10,
                    options={"A": "Concept A", "B": "Concept B", "C": "Concept C", "D": "Concept D"},
                    correct_answer="A",
                    explanation="Sample explanation",
                    is_active=True,
                ),
                Assessment(
                    module_id=module.id,
                    question_text=f"True or False: {module.title} requires prior modules.",
                    question_type=QuestionType.TRUE_FALSE,
                    order_index=2,
                    points=5,
                    options=None,
                    correct_answer="false",
                    explanation="Sample explanation",
                    is_active=True,
                ),
                Assessment(
                    module_id=module.id,
                    question_text=f"Briefly explain a concept from {module.title}.",
                    question_type=QuestionType.SHORT_ANSWER,
                    order_index=3,
                    points=10,
                    options=None,
                    correct_answer="",
                    explanation="Instructor graded.",
                    is_active=True,
                ),
            ]
        )

    session.add_all(assessments)
    await session.flush()


async def main() -> None:
    async with AsyncSessionLocal() as session:
        # Users
        await seed_users(session)
        # Modules + Lessons
        modules = await seed_modules_lessons(session)
        # Assessments
        await seed_assessments(session, modules)
        # Commit
        await session.commit()


if __name__ == "__main__":
    asyncio.run(main())
