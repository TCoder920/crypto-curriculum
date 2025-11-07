import asyncio
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.core.database import AsyncSessionLocal
from app.backend.models.user import User, UserRole
from app.backend.models.module import Module, Lesson, Track
from app.backend.models.assessment import Assessment, QuestionType


# Module metadata from curriculum outline
MODULE_METADATA = {
    1: {"title": "Blockchain Technology", "duration": 2.0, "description": "Learn the fundamentals of blockchain, distributed ledgers, immutability, and consensus mechanisms."},
    2: {"title": "Web3 Wallets & Security", "duration": 3.0, "description": "Understand public/private keys, wallet types, security best practices, and seed phrases."},
    3: {"title": "Transactions, dApps & Gas Fees", "duration": 1.0, "description": "Learn how transactions work, interact with dApps, and understand gas fees."},
    4: {"title": "Tokens & Digital Assets", "duration": 3.0, "description": "Explore fungible tokens, NFTs, token standards, and digital asset management."},
    5: {"title": "Trading", "duration": 2.0, "description": "Learn about exchanges, trading pairs, order types, and market analysis basics."},
    6: {"title": "DeFi & DAOs", "duration": 2.5, "description": "Understand decentralized finance, DAOs, governance, and DeFi protocols."},
    7: {"title": "Advanced Concepts Overview", "duration": 2.5, "description": "Explore layer 2 solutions, bridges, oracles, and advanced blockchain concepts."},
    8: {"title": "Practical On-Chain Analysis", "duration": 3.0, "description": "Learn to analyze blockchain data, track transactions, and use on-chain analytics tools."},
    9: {"title": "Advanced Market & Tokenomic Analysis", "duration": 4.0, "description": "Deep dive into tokenomics, market analysis, and economic models."},
    10: {"title": "Advanced DeFi Strategies", "duration": 3.0, "description": "Master advanced DeFi strategies, yield farming, and protocol interactions."},
    11: {"title": "Development & Programming Prerequisites", "duration": 3.0, "description": "Learn programming fundamentals, development tools, and prerequisites for blockchain development."},
    12: {"title": "Smart Contract Development (Solidity & EVM)", "duration": 6.0, "description": "Master Solidity, EVM, smart contract security, and deployment."},
    13: {"title": "dApp Development & Tooling", "duration": 4.0, "description": "Build decentralized applications, integrate with wallets, and use development tooling."},
    14: {"title": "Creating a Fungible Token & ICO", "duration": 4.0, "description": "Create your own token, understand ICOs, and launch token projects."},
    15: {"title": "Creating an NFT Collection & Marketplace", "duration": 4.0, "description": "Build NFT collections, create marketplaces, and understand NFT standards."},
    16: {"title": "Building Your Own Blockchain & Mining", "duration": 4.0, "description": "Learn blockchain architecture, consensus implementation, and mining mechanisms."},
    17: {"title": "AI Agent Application Development", "duration": 6.0, "description": "Build AI-powered trading bots, integrate LLMs, and create autonomous agents."},
}


def parse_curriculum_file(file_path: Path) -> Dict[int, List[Dict]]:
    """Parse curriculum markdown file and extract lessons by module"""
    if not file_path.exists():
        return {}
    
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}")
        return {}
    
    modules_lessons: Dict[int, List[Dict]] = {}
    
    # Split by module headers (## Module X:)
    module_pattern = r'## Module (\d+):\s*(.+?)(?=## Module \d+:|$)'
    matches = re.finditer(module_pattern, content, re.DOTALL | re.IGNORECASE)
    
    for match in matches:
        module_num = int(match.group(1))
        module_content = match.group(2).strip()
        
        lessons = []
        lesson_order = 1
        
        # Split by lesson headers (### X.Y Lesson Title)
        lesson_pattern = r'### (\d+\.\d+)\s+(.+?)(?=### \d+\.\d+|$)'
        lesson_matches = re.finditer(lesson_pattern, module_content, re.DOTALL)
        
        for lesson_match in lesson_matches:
            lesson_num = lesson_match.group(1)
            lesson_title = lesson_match.group(2).split('\n')[0].strip()
            lesson_content = lesson_match.group(2).strip()
            
            # Clean up the content
            lesson_content = re.sub(r'^### \d+\.\d+\s+.*?\n', '', lesson_content, flags=re.MULTILINE)
            
            lessons.append({
                'title': lesson_title,
                'content': lesson_content,
                'order_index': lesson_order,
                'estimated_minutes': 20,  # Default estimate
            })
            lesson_order += 1
        
        # If no structured lessons found, create one lesson from the module content
        if not lessons:
            lessons.append({
                'title': f"{MODULE_METADATA.get(module_num, {}).get('title', f'Module {module_num}')} - Overview",
                'content': module_content[:5000] if len(module_content) > 5000 else module_content,  # Limit content length
                'order_index': 1,
                'estimated_minutes': 30,
            })
        
        modules_lessons[module_num] = lessons
    
    return modules_lessons


def parse_all_curriculum_files() -> Dict[int, List[Dict]]:
    """Parse all curriculum markdown files"""
    curriculum_dir = Path(__file__).parent.parent.parent / "curriculum"
    all_lessons: Dict[int, List[Dict]] = {}
    
    # Parse each part file
    for part_num in range(1, 5):
        part_file = curriculum_dir / f"blockchain curriculum part {part_num}.md"
        if part_file.exists():
            lessons = parse_curriculum_file(part_file)
            all_lessons.update(lessons)
    
    return all_lessons


async def seed_users(session: AsyncSession) -> List[User]:
    """Seed users (idempotent - skips if already exist)"""
    from sqlalchemy import select
    
    users: List[User] = []
    user_emails = ["admin@example.com", "instructor.alex@example.com", "student.casey@example.com"]
    
    # Check existing users
    result = await session.execute(select(User).where(User.email.in_(user_emails)))
    existing_users = {u.email: u for u in result.scalars().all()}
    
    if "admin@example.com" not in existing_users:
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
    else:
        users.append(existing_users["admin@example.com"])

    if "instructor.alex@example.com" not in existing_users:
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
    else:
        users.append(existing_users["instructor.alex@example.com"])

    if "student.casey@example.com" not in existing_users:
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
    else:
        users.append(existing_users["student.casey@example.com"])

    if len(users) > len(existing_users):
        session.add_all([u for u in users if u.email not in existing_users])
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
    """Seed modules and lessons from curriculum files (idempotent - updates existing)"""
    from sqlalchemy import select
    
    modules: List[Module] = []
    
    # Parse curriculum files
    curriculum_lessons = parse_all_curriculum_files()
    
    # Get existing modules
    result = await session.execute(select(Module))
    existing_modules = {m.id: m for m in result.scalars().all()}
    
    for module_id in range(1, 18):
        metadata = MODULE_METADATA.get(module_id, {})
        
        # Calculate prerequisites (previous modules in same track or earlier tracks)
        prerequisites = []
        if module_id > 1:
            # Simple: require all previous modules
            prerequisites = list(range(1, module_id))
        
        # Check if module exists
        if module_id in existing_modules:
            module = existing_modules[module_id]
            # Update metadata
            module.title = metadata.get("title", f"Module {module_id}")
            module.description = metadata.get("description", f"Curriculum content for module {module_id}")
            module.duration_hours = metadata.get("duration", 2.0)
            module.prerequisites = prerequisites if prerequisites else None
            module.learning_objectives = [
                f"Understand key concepts in {metadata.get('title', f'Module {module_id}')}",
                f"Apply knowledge from {metadata.get('title', f'Module {module_id}')}",
                f"Analyze real-world applications of {metadata.get('title', f'Module {module_id}')}",
            ]
        else:
            module = Module(
                id=module_id,
                title=metadata.get("title", f"Module {module_id}"),
                description=metadata.get("description", f"Curriculum content for module {module_id}"),
                track=resolve_track(module_id),
                order_index=module_id,
                duration_hours=metadata.get("duration", 2.0),
                prerequisites=prerequisites if prerequisites else None,
                learning_objectives=[
                    f"Understand key concepts in {metadata.get('title', f'Module {module_id}')}",
                    f"Apply knowledge from {metadata.get('title', f'Module {module_id}')}",
                    f"Analyze real-world applications of {metadata.get('title', f'Module {module_id}')}",
                ],
                is_active=True,
                is_published=True,
            )
        
        # Get lessons from parsed curriculum or create default
        lesson_data = curriculum_lessons.get(module_id, [])
        
        # Delete existing lessons if updating
        if module_id in existing_modules:
            from app.backend.models.module import Lesson
            from sqlalchemy import delete
            await session.execute(delete(Lesson).where(Lesson.module_id == module_id))
        
        # Create new lessons
        new_lessons = []
        if lesson_data:
            # Use parsed lessons
            for i, lesson in enumerate(lesson_data):
                new_lessons.append(
                    Lesson(
                        module_id=module_id,
                        title=lesson.get("title", f"Lesson {i+1}"),
                        content=lesson.get("content", f"Content for lesson {i+1}"),
                        order_index=lesson.get("order_index", i+1),
                        estimated_minutes=lesson.get("estimated_minutes", 20),
                        lesson_type="reading",
                        is_active=True,
                    )
                )
        else:
            # Fallback: create placeholder lessons
            new_lessons.append(
                Lesson(
                    module_id=module_id,
                    title=f"{module.title} - Lesson 1",
                    content=f"# {module.title}\n\n{module.description}\n\nThis module is part of the curriculum. Content will be available soon.",
                    order_index=1,
                    estimated_minutes=30,
                    lesson_type="reading",
                    is_active=True,
                )
            )
        
        if new_lessons:
            session.add_all(new_lessons)
        
        modules.append(module)
    
    # Only add new modules
    new_modules = [m for m in modules if m.id not in existing_modules]
    if new_modules:
        session.add_all(new_modules)
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
        print(f"✅ Seeded {len(modules)} modules with lessons and assessments")


if __name__ == "__main__":
    asyncio.run(main())
