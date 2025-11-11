"""Re-seed assessments with proper questions (clears existing assessments first)"""
import asyncio
from datetime import datetime
from typing import List
from sqlalchemy import delete, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.core.database import AsyncSessionLocal
from app.backend.models.assessment import Assessment
from app.backend.models.module import Module, Lesson, Track
from app.backend.assessment_questions import get_all_assessments


async def seed_modules_lessons(session: AsyncSession) -> List[Module]:
    """Create basic modules and lessons if they don't exist"""
    modules: List[Module] = []
    
    def resolve_track(module_id: int) -> Track:
        if 1 <= module_id <= 7:
            return Track.USER
        if 8 <= module_id <= 10:
            return Track.ANALYST
        if 11 <= module_id <= 13:
            return Track.DEVELOPER
        return Track.ARCHITECT
    
    for module_id in range(1, 18):
        module = Module(
            id=module_id,
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
    """Seed assessments for all modules using assessment_questions.py"""
    assessments: List[Assessment] = []
    all_assessments = get_all_assessments()
    
    for module in modules:
        if module.id in all_assessments:
            # Use comprehensive questions from assessment_questions.py
            for assessment_template in all_assessments[module.id]:
                assessment = Assessment(
                    module_id=module.id,
                    question_text=assessment_template.question_text,
                    question_type=assessment_template.question_type,
                    order_index=assessment_template.order_index,
                    points=assessment_template.points,
                    options=assessment_template.options,
                    correct_answer=assessment_template.correct_answer,
                    explanation=assessment_template.explanation,
                    is_active=assessment_template.is_active,
                )
                assessments.append(assessment)
        else:
            # Fallback: Should not happen, but handle gracefully
            print(f"Warning: No assessments found for module {module.id}")
    
    session.add_all(assessments)
    await session.flush()


async def clear_assessments(session: AsyncSession) -> None:
    """Clear all existing assessments"""
    await session.execute(delete(Assessment))
    await session.flush()
    print("✓ Cleared all existing assessments")


async def main() -> None:
    """Clear and re-seed assessments with proper questions"""
    async with AsyncSessionLocal() as session:
        print("Clearing existing assessments...")
        await clear_assessments(session)
        
        print("Fetching modules...")
        # Get all modules (they should already exist)
        result = await session.execute(select(Module))
        modules = result.scalars().all()
        
        if not modules:
            print("No modules found. Seeding modules first...")
            modules = await seed_modules_lessons(session)
            await session.commit()
            print(f"✓ Created {len(modules)} modules")
        
        print(f"Re-seeding assessments for {len(modules)} modules...")
        await seed_assessments(session, modules)
        
        await session.commit()
        
        # Realign sequence so future inserts don't collide
        await session.execute(
            text(
                "SELECT setval('assessments_id_seq', "
                "(SELECT COALESCE(MAX(id), 0) FROM assessments) + 1, false)"
            )
        )
        await session.execute(
            text(
                "SELECT setval('quiz_attempts_id_seq', "
                "(SELECT COALESCE(MAX(id), 0) FROM quiz_attempts) + 1, false)"
            )
        )
        await session.commit()
        print("✓ Reset assessment ID sequence")
        print("✓ Successfully re-seeded all assessments with proper questions")
        print(f"✓ Module 1 now has 10 multiple choice questions")


if __name__ == "__main__":
    asyncio.run(main())

