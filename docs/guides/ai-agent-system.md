# AI Agent Development System

This document explains the AI agent framework we've set up in Cursor to efficiently develop the cryptocurrency curriculum platform.

## Overview

We've created a multi-agent system where specialized AI agents handle different aspects of development. This approach ensures consistency, follows best practices, and accelerates development.

## Agent Architecture

```
┌─────────────────────────────────────┐
│   Master Orchestrator Agent         │
│   (Coordinates everything)           │
└───────────┬─────────────────────────┘
            │
            ├───────────────────────────────────────────────┐
            │                                               │
    ┌───────▼────────┐  ┌───────────────┐  ┌─────────────▼──────┐
    │  Frontend      │  │   Backend     │  │    Database        │
    │  Component     │  │   API         │  │    Schema          │
    │  Agent         │  │   Agent       │  │    Agent           │
    └────────────────┘  └───────────────┘  └────────────────────┘
                                │
                        ┌───────▼────────┐
                        │  Trading Bot   │
                        │  Framework     │
                        │  Agent         │
                        └────────────────┘
```

## Specialized Agents

### 1. Master Orchestrator Agent
**File**: `.cursor/rules/masterOrchestrator.mdc`  
**Status**: `alwaysApply: true` (Always active)

**Purpose**: Coordinates between specialized agents, maintains project consistency, and guides overall development strategy.

**Responsibilities**:
- Task analysis and agent selection
- Cross-agent coordination
- Project structure maintenance
- Decision framework
- Progress tracking

### 2. Frontend Component Agent
**File**: `.cursor/rules/frontendComponentAgent.mdc`  
**Status**: `alwaysApply: false` (Activate on demand)

**Purpose**: Build React components with TypeScript, MUI v7, and Tailwind CSS.

**Use this agent for**:
- Creating React components
- Building pages and layouts
- Implementing UI/UX features
- Styling with MUI and Tailwind
- State management
- API integration (frontend side)

**Tech Stack**:
- React 18.3 + TypeScript
- Vite 5.4
- Material-UI v7 + Emotion
- Tailwind CSS
- React Router v6
- Axios

### 3. Backend API Agent
**File**: `.cursor/rules/backendApiAgent.mdc`  
**Status**: `alwaysApply: false` (Activate on demand)

**Purpose**: Build FastAPI REST API with proper architecture and best practices.

**Use this agent for**:
- Creating API endpoints
- Writing business logic (services)
- Pydantic schema validation
- Authentication/authorization
- Error handling
- Logging

**Tech Stack**:
- Python 3.11+
- FastAPI
- SQLAlchemy 2.0+
- Pydantic v2
- JWT authentication
- Pytest

### 4. Database Schema Agent
**File**: `.cursor/rules/databaseSchemaAgent.mdc`  
**Status**: `alwaysApply: false` (Activate on demand)

**Purpose**: Design database schemas, create models, and manage migrations.

**Use this agent for**:
- Designing database schemas
- Creating SQLAlchemy models
- Writing Alembic migrations
- Defining relationships
- Adding indexes
- Optimization

**Tech Stack**:
- PostgreSQL 15+
- SQLAlchemy 2.0+ (async)
- Alembic
- psycopg2-binary

### 5. Trading Bot Framework Agent
**File**: `.cursor/rules/tradingBotAgent.mdc`  
**Status**: `alwaysApply: false` (Activate on demand)

**Purpose**: Build custom LLM-agnostic AI trading bot framework for Module 17.

**Use this agent for**:
- Building base agent architecture
- Creating LLM provider interfaces
- Implementing trading tools
- Technical indicator calculators
- Backtesting engine
- Student examples

**Tech Stack**:
- Python 3.11+
- Abstract base classes
- httpx for async HTTP
- pandas/numpy for data
- Support for OpenAI, Anthropic, Ollama

## How to Use the Agent System

### Method 1: Explicit Agent Activation

When you know exactly which agent you need:

```
"Use Frontend Component Agent to create a ModuleDashboard component 
that displays all curriculum modules with progress tracking."
```

```
"Activate Database Schema Agent to create models for the quiz system 
with questions, answers, and user attempts."
```

```
"Use Trading Bot Framework Agent to implement the base agent class 
with tool registration capability."
```

### Method 2: Let Orchestrator Decide

Describe what you want, and the orchestrator will activate appropriate agents:

```
"Build a login page with email/password authentication."
```
→ Orchestrator will activate: Frontend Component Agent + Backend API Agent

```
"Create the entire quiz system with questions, attempts, and scoring."
```
→ Orchestrator will activate: Database Schema Agent + Backend API Agent + Frontend Component Agent

### Method 3: Multi-Agent Tasks

For complex features requiring multiple agents:

```
"Build the user progress tracking system end-to-end."
```

This will coordinate:
1. Database Schema Agent → Create models
2. Backend API Agent → Create endpoints and services
3. Frontend Component Agent → Build UI components

## Agent Configuration Files

Each agent configuration file (`.mdc`) contains:

1. **Tech Stack**: Technologies and tools the agent uses
2. **Core Principles**: Fundamental rules and patterns
3. **Code Examples**: Templates and patterns to follow
4. **File Organization**: Where to place files
5. **Naming Conventions**: Consistent naming across project
6. **Anti-Patterns**: What to avoid
7. **Testing Requirements**: How to test
8. **Documentation Standards**: How to document code

## Project Structure

The agents maintain this structure:

```
crypto curriculum/
├── curriculum/              # Content files
│   ├── blockchain curriculum part 1.md (✅ Complete)
│   ├── blockchain curriculum part 2.md (⏳ To create)
│   ├── blockchain curriculum part 3.md (⏳ To create)
│   └── blockchain curriculum part 4.md (⏳ To create)
├── app/
│   ├── frontend/           # React application
│   │   ├── src/
│   │   │   ├── components/
│   │   │   ├── pages/
│   │   │   ├── modules/
│   │   │   ├── services/
│   │   │   ├── types/
│   │   │   ├── hooks/
│   │   │   └── theme/
│   │   └── package.json
│   └── backend/            # FastAPI application
│       ├── api/
│       ├── services/
│       ├── models/
│       ├── schemas/
│       ├── ai_agent/
│       └── requirements.txt
└── .cursor/
    └── rules/              # Agent configurations (Cursor's standard location)
        ├── systemPrompt.mdc
        ├── masterOrchestrator.mdc
        ├── frontendComponentAgent.mdc
        ├── backendApiAgent.mdc
        ├── databaseSchemaAgent.mdc
        └── tradingBotAgent.mdc
└── docs/
    └── guides/
        └── ai-agent-system.md  # This documentation file
```

## Development Phases

### ✅ Phase 1: Agent System Setup (COMPLETE)
- Created specialized agent configurations
- Established coordination framework
- Documented usage

### ⏳ Phase 2: Curriculum Content Expansion (IN PROGRESS)
- Part 1: Complete (Modules 1-7)
- Part 2: To create (Modules 8-10)
- Part 3: To create (Modules 11-13)
- Part 4: To create (Modules 14-17 + AI Trading Bot)
- Testing components: 10 questions/tasks per module

### 📋 Phase 3: Project Initialization (NEXT)
- Initialize frontend project
- Initialize backend project
- Set up PostgreSQL database
- Configure development environment

### 📋 Phase 4: Core Development
- Database schema implementation
- API development
- Frontend components
- AI trading bot framework

### 📋 Phase 5: Integration & Testing
- Content integration
- End-to-end testing
- Documentation

### 📋 Phase 6: Deployment
- Docker containerization
- CI/CD setup
- Production deployment

## Best Practices

### 1. Clear Task Descriptions
✅ Good: "Use Frontend Component Agent to create a reusable QuizCard component that displays a question with multiple choice options and handles answer selection."

❌ Bad: "Make a quiz thing."

### 2. Specify Context
✅ Good: "Using the Database Schema Agent, add a new 'notes' field to the UserProgress model to allow students to save lesson notes."

❌ Bad: "Add notes feature."

### 3. Reference Existing Code
✅ Good: "Following the pattern in `ModuleCard.tsx`, create a `LessonCard.tsx` component with similar styling."

❌ Bad: "Make another card."

### 4. Break Down Complex Tasks
Large tasks should be broken into agent-specific subtasks:

**Task**: "Build the quiz system"

**Breakdown**:
1. Database Schema Agent: Create Quiz, Question, QuizAttempt models
2. Backend API Agent: Create quiz endpoints and services
3. Frontend Component Agent: Build QuizInterface component
4. Testing: Add unit tests for each layer

## Agent Guidelines Summary

### Frontend Component Agent
- Always use TypeScript (strict mode)
- Functional components with hooks
- MUI components + Tailwind utilities
- Accessibility first
- Responsive design

### Backend API Agent
- Separate routes → services → models
- Pydantic validation for all inputs
- Async/await for I/O operations
- Proper error handling
- Structured logging

### Database Schema Agent
- Timestamps on all tables
- Soft deletes where appropriate
- Proper foreign keys and cascades
- Indexes on frequently queried columns
- Clear relationships

### Trading Bot Framework Agent
- LLM-agnostic design
- Tool-based architecture
- Educational focus (easy to understand)
- Well-documented for students
- Provider pattern for extensibility

## Troubleshooting

### Agent Not Following Guidelines?
Make sure to explicitly reference the agent:
```
"Use Frontend Component Agent (see .cursor/rules/frontendComponentAgent.mdc) to..."
```

### Need Multiple Agents?
Let the orchestrator coordinate:
```
"Build the complete user authentication system including database, API, and frontend."
```

### Conflicting Patterns?
The Master Orchestrator has final say on cross-cutting concerns. Reference it explicitly:
```
"According to the Master Orchestrator guidelines, what naming convention should I use for..."
```

## Next Steps

1. **Complete curriculum content** (Parts 2-4)
2. **Initialize project structure**
3. **Start with database schema** (foundational)
4. **Build API layer** (business logic)
5. **Create frontend components** (user interface)
6. **Implement trading bot framework** (Module 17)

## Questions?

- Check the specific agent's `.mdc` file for detailed guidelines
- Review the Master Orchestrator for coordination rules
- Look at existing examples in the project
- Reference this document for high-level overview

---

**Remember**: This agent system is designed to make development faster, more consistent, and higher quality. Use it actively and iterate on the patterns as you discover what works best!

