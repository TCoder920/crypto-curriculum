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


def get_module_1_assessments(module_id: int) -> List[Assessment]:
    """Module 1: Blockchain Technology - 10 questions"""
    return [
        # Multiple Choice (4 questions)
        Assessment(
            module_id=module_id,
            question_text="What is a distributed ledger?",
            question_type=QuestionType.MULTIPLE_CHOICE,
            order_index=1,
            points=10,
            options={
                "A": "A centralized database managed by a single authority",
                "B": "A shared database that is synchronized across multiple locations",
                "C": "A cloud storage service",
                "D": "A type of spreadsheet"
            },
            correct_answer="B",
            explanation="A distributed ledger is a shared database that is synchronized across multiple locations, participants, or institutions. Unlike a centralized database, no single party controls it.",
            is_active=True,
        ),
        Assessment(
            module_id=module_id,
            question_text="What is the primary purpose of a blockchain?",
            question_type=QuestionType.MULTIPLE_CHOICE,
            order_index=2,
            points=10,
            options={
                "A": "To store large amounts of data",
                "B": "To create an immutable record of transactions",
                "C": "To speed up internet connections",
                "D": "To replace traditional databases"
            },
            correct_answer="B",
            explanation="The primary purpose of a blockchain is to create an immutable, tamper-proof record of transactions that can be verified by all participants.",
            is_active=True,
        ),
        Assessment(
            module_id=module_id,
            question_text="What is a block in a blockchain?",
            question_type=QuestionType.MULTIPLE_CHOICE,
            order_index=3,
            points=10,
            options={
                "A": "A physical storage device",
                "B": "A collection of transactions grouped together and cryptographically linked to the previous block",
                "C": "A type of cryptocurrency",
                "D": "A network node"
            },
            correct_answer="B",
            explanation="A block is a collection of transactions that are grouped together and cryptographically linked to the previous block, forming a chain.",
            is_active=True,
        ),
        Assessment(
            module_id=module_id,
            question_text="What does 'immutable' mean in the context of blockchain?",
            question_type=QuestionType.MULTIPLE_CHOICE,
            order_index=4,
            points=10,
            options={
                "A": "Can be easily changed",
                "B": "Cannot be altered or deleted once recorded",
                "C": "Requires permission to view",
                "D": "Stored in multiple locations"
            },
            correct_answer="B",
            explanation="Immutable means that once data is recorded on the blockchain, it cannot be altered or deleted. This is a key security feature of blockchain technology.",
            is_active=True,
        ),
        # True/False (3 questions)
        Assessment(
            module_id=module_id,
            question_text="True or False: Blockchain requires a central authority to validate transactions.",
            question_type=QuestionType.TRUE_FALSE,
            order_index=5,
            points=10,
            options=None,
            correct_answer="False",
            explanation="Blockchain is decentralized and does not require a central authority. Transactions are validated by network participants through consensus mechanisms.",
            is_active=True,
        ),
        Assessment(
            module_id=module_id,
            question_text="True or False: Once a block is added to the blockchain, it can be easily modified.",
            question_type=QuestionType.TRUE_FALSE,
            order_index=6,
            points=10,
            options=None,
            correct_answer="False",
            explanation="Blocks are cryptographically linked, making it extremely difficult to modify past blocks without invalidating the entire chain.",
            is_active=True,
        ),
        Assessment(
            module_id=module_id,
            question_text="True or False: Blockchain technology can only be used for cryptocurrencies.",
            question_type=QuestionType.TRUE_FALSE,
            order_index=7,
            points=10,
            options=None,
            correct_answer="False",
            explanation="Blockchain has many applications beyond cryptocurrencies, including supply chain management, voting systems, identity verification, and more.",
            is_active=True,
        ),
        # Short Answer (3 questions)
        Assessment(
            module_id=module_id,
            question_text="Explain in your own words what makes blockchain technology secure.",
            question_type=QuestionType.SHORT_ANSWER,
            order_index=8,
            points=10,
            options=None,
            correct_answer="",
            explanation="Instructor will review your answer. Key points may include: cryptographic hashing, distributed consensus, immutability, and transparency.",
            is_active=True,
        ),
        Assessment(
            module_id=module_id,
            question_text="Describe one real-world application of blockchain technology (besides cryptocurrency).",
            question_type=QuestionType.SHORT_ANSWER,
            order_index=9,
            points=10,
            options=None,
            correct_answer="",
            explanation="Instructor will review your answer. Examples include: supply chain tracking, digital identity, voting systems, medical records, etc.",
            is_active=True,
        ),
        Assessment(
            module_id=module_id,
            question_text="What is the relationship between blocks in a blockchain? How are they connected?",
            question_type=QuestionType.SHORT_ANSWER,
            order_index=10,
            points=10,
            options=None,
            correct_answer="",
            explanation="Instructor will review your answer. Key points: blocks contain a hash of the previous block, creating a chain. Each block references the previous one cryptographically.",
            is_active=True,
        ),
    ]


async def seed_assessments(session: AsyncSession, modules: List[Module]) -> None:
    """Seed assessments for all modules. Module 1 has full 10 questions, others have sample questions."""
    assessments: List[Assessment] = []
    
    for module in modules:
        if module.id == 1:
            # Module 1: Full set of 10 questions
            assessments.extend(get_module_1_assessments(module.id))
        else:
            # Other modules: Sample questions (can be expanded later)
            # 4 Multiple Choice
            assessments.extend([
                Assessment(
                    module_id=module.id,
                    question_text=f"What is a key concept in {module.title}?",
                    question_type=QuestionType.MULTIPLE_CHOICE,
                    order_index=1,
                    points=10,
                    options={
                        "A": "Option A",
                        "B": "Option B",
                        "C": "Option C",
                        "D": "Option D"
                    },
                    correct_answer="A",
                    explanation="Sample explanation for this question.",
                    is_active=True,
                ),
                Assessment(
                    module_id=module.id,
                    question_text=f"Which of the following best describes {module.title}?",
                    question_type=QuestionType.MULTIPLE_CHOICE,
                    order_index=2,
                    points=10,
                    options={
                        "A": "Description A",
                        "B": "Description B",
                        "C": "Description C",
                        "D": "Description D"
                    },
                    correct_answer="B",
                    explanation="Sample explanation.",
                    is_active=True,
                ),
                Assessment(
                    module_id=module.id,
                    question_text=f"What is the primary purpose of {module.title}?",
                    question_type=QuestionType.MULTIPLE_CHOICE,
                    order_index=3,
                    points=10,
                    options={
                        "A": "Purpose A",
                        "B": "Purpose B",
                        "C": "Purpose C",
                        "D": "Purpose D"
                    },
                    correct_answer="C",
                    explanation="Sample explanation.",
                    is_active=True,
                ),
                Assessment(
                    module_id=module.id,
                    question_text=f"Which feature is most important in {module.title}?",
                    question_type=QuestionType.MULTIPLE_CHOICE,
                    order_index=4,
                    points=10,
                    options={
                        "A": "Feature A",
                        "B": "Feature B",
                        "C": "Feature C",
                        "D": "Feature D"
                    },
                    correct_answer="D",
                    explanation="Sample explanation.",
                    is_active=True,
                ),
            ])
            # 3 True/False
            assessments.extend([
                Assessment(
                    module_id=module.id,
                    question_text=f"True or False: {module.title} requires prior knowledge.",
                    question_type=QuestionType.TRUE_FALSE,
                    order_index=5,
                    points=10,
                    options=None,
                    correct_answer="True",
                    explanation="Sample explanation.",
                    is_active=True,
                ),
                Assessment(
                    module_id=module.id,
                    question_text=f"True or False: {module.title} is only used in specific contexts.",
                    question_type=QuestionType.TRUE_FALSE,
                    order_index=6,
                    points=10,
                    options=None,
                    correct_answer="False",
                    explanation="Sample explanation.",
                    is_active=True,
                ),
                Assessment(
                    module_id=module.id,
                    question_text=f"True or False: {module.title} is a fundamental concept.",
                    question_type=QuestionType.TRUE_FALSE,
                    order_index=7,
                    points=10,
                    options=None,
                    correct_answer="True",
                    explanation="Sample explanation.",
                    is_active=True,
                ),
            ])
            # 3 Short Answer
            assessments.extend([
                Assessment(
                    module_id=module.id,
                    question_text=f"Explain a key concept from {module.title} in your own words.",
                    question_type=QuestionType.SHORT_ANSWER,
                    order_index=8,
                    points=10,
                    options=None,
                    correct_answer="",
                    explanation="Instructor will review your answer.",
                    is_active=True,
                ),
                Assessment(
                    module_id=module.id,
                    question_text=f"Describe how {module.title} relates to blockchain technology.",
                    question_type=QuestionType.SHORT_ANSWER,
                    order_index=9,
                    points=10,
                    options=None,
                    correct_answer="",
                    explanation="Instructor will review your answer.",
                    is_active=True,
                ),
                Assessment(
                    module_id=module.id,
                    question_text=f"What are the main benefits of understanding {module.title}?",
                    question_type=QuestionType.SHORT_ANSWER,
                    order_index=10,
                    points=10,
                    options=None,
                    correct_answer="",
                    explanation="Instructor will review your answer.",
                    is_active=True,
                ),
            ])

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
