# Cryptocurrency Curriculum Platform

> An educational platform for teaching blockchain and cryptocurrency concepts to complete beginners, developed for Universal Tech Movement (Austin, TX)

## 🎯 Project Overview

This project provides a comprehensive, full-stack educational platform for cryptocurrency and blockchain education. The curriculum takes students from absolute beginners to advanced developers capable of building their own blockchain applications and AI-powered trading bots.

## 📚 Curriculum Structure

### Part 1: The "User" Track (Foundations) ✅ COMPLETE
**Goal**: Create an informed, safe, and competent user of Web3

- **Module 1**: Blockchain Technology (2h)
- **Module 2**: Web3 Wallets & Security (3h)
- **Module 3**: Transactions, dApps & Gas Fees (1h)
- **Module 4**: Tokens & Digital Assets (3h)
- **Module 5**: Trading (2h)
- **Module 6**: DeFi & DAOs (2.5h)
- **Module 7**: Advanced Concepts Overview (2.5h)

### Part 2: The "Power User" / Analyst Track ✅ COMPLETE
**Goal**: Bridge the gap from using the chain to analyzing it

- **Module 8**: Practical On-Chain Analysis (3h)
- **Module 9**: Advanced Market & Tokenomic Analysis (4h)
- **Module 10**: Advanced DeFi Strategies (3h)

### Part 3: The "Developer" Track ✅ COMPLETE
**Goal**: Build technical skills for smart contracts and dApps

- **Module 11**: Development & Programming Prerequisites (3h)
- **Module 12**: Smart Contract Development (Solidity & EVM) (6h)
- **Module 13**: dApp Development & Tooling (4h)

### Part 4: The "Architect" / Builder Track ✅ COMPLETE
**Goal**: Use developer skills to build complex, novel systems

- **Module 14**: Creating a Fungible Token & ICO (4h)
- **Module 15**: Creating an NFT Collection & Marketplace (4h)
- **Module 16**: Building Your Own Blockchain & Mining (4h)
- **Module 17**: AI Agent Application Development (6h)

## 🏗️ Technical Architecture

### Frontend Stack
- **Framework**: React 18.3 with TypeScript
- **Build Tool**: Vite 5.4
- **UI Library**: Material-UI (MUI) v7
- **Design System**: Apple Liquid Glass UI with adaptive materials
- **Styling**: Tailwind CSS + Emotion
- **Animation**: Framer Motion (fluid motion, spring physics)
- **Routing**: React Router v6
- **API Client**: Axios (port 8000)
- **State Management**: React Query (TanStack Query)

### Backend Stack
- **Framework**: FastAPI (Python 3.11+)
- **ORM**: SQLAlchemy 2.0+ (async)
- **Database**: PostgreSQL 15+
- **Validation**: Pydantic v2
- **Authentication**: JWT
- **Testing**: Pytest

### AI Trading Bot Framework
- **Architecture**: Custom LLM-agnostic agent system
- **Supported LLMs**: OpenAI, Anthropic Claude, Ollama (local)
- **Features**: Technical indicators, backtesting, risk management
- **Design**: Educational, extensible, provider-agnostic

## 🤖 AI Agent Development System

This project uses a specialized AI agent framework in Cursor for efficient development:

### Specialized Agents
1. **Master Orchestrator** - Coordinates all development
2. **Frontend Component Agent** - React + TypeScript + MUI
3. **Backend API Agent** - FastAPI + SQLAlchemy
4. **Database Schema Agent** - PostgreSQL models & migrations
5. **Trading Bot Framework Agent** - AI trading bot system

📖 **Full documentation**: See [`cursor/AI_AGENT_SYSTEM.md`](cursor/AI_AGENT_SYSTEM.md)

## 📁 Project Structure

```
crypto-curriculum/
├── .gitignore                    # Git ignore rules (API keys, secrets, etc.)
├── README.md                     # This file - Project overview
│
├── curriculum/                   # 📚 All curriculum content
│   ├── code-examples/           # Reference code for teaching
│   │   └── module-17/           # AI agent examples (Python)
│   ├── blockchain curriculum outline.md
│   ├── blockchain curriculum part 1.md (✅ Complete)
│   ├── blockchain curriculum part 2.md (✅ Complete)
│   ├── blockchain curriculum part 3.md (✅ Complete)
│   └── blockchain curriculum part 4.md (✅ Complete)
│
├── app/                          # 💻 Application code (to be initialized)
│   ├── frontend/                 # React application
│   │   ├── src/
│   │   │   ├── components/      # Reusable UI components
│   │   │   ├── pages/           # Page components (routes)
│   │   │   ├── modules/         # Module-specific content
│   │   │   ├── services/        # API service layer
│   │   │   ├── types/           # TypeScript interfaces
│   │   │   ├── hooks/           # Custom React hooks
│   │   │   ├── utils/           # Helper functions
│   │   │   ├── theme/           # MUI + Liquid Glass theme
│   │   │   └── App.tsx
│   │   ├── public/
│   │   ├── package.json
│   │   ├── vite.config.ts
│   │   └── README.md            # Frontend-specific docs
│   │
│   └── backend/                  # FastAPI application
│       ├── api/                  # API routes
│       │   └── v1/endpoints/
│       ├── services/             # Business logic layer
│       ├── models/               # SQLAlchemy models
│       ├── schemas/              # Pydantic schemas
│       ├── core/                 # Config, database, security
│       ├── ai_agent/             # Trading bot framework
│       │   ├── base_agent.py
│       │   ├── llm_provider.py
│       │   ├── providers/       # OpenAI, Anthropic, Ollama
│       │   └── tools/           # Trading tools
│       ├── utils/
│       ├── tests/
│       ├── main.py
│       ├── requirements.txt
│       └── README.md            # Backend-specific docs
│
├── cursor/                       # 🤖 AI agent configurations
│   ├── AI_AGENT_SYSTEM.md       # Agent system documentation
│   └── rules/                    # Agent rule files
│       ├── masterOrchestrator.mdc
│       ├── frontendComponentAgent.mdc
│       ├── backendApiAgent.mdc
│       ├── databaseSchemaAgent.mdc
│       └── tradingBotAgent.mdc
│
├── UI-examples/                  # 🎨 Design reference for frontend
│   ├── part 1 webpage example.html (DESIGN REFERENCE - mirror this)
│   └── part 1 infographic example.html
│
├── docs/                         # 📖 Project documentation
│   ├── api/
│   │   └── endpoints.md          # ✅ API endpoint reference
│   ├── architecture/
│   │   ├── database-schema.md    # ✅ Database design & ERD
│   │   └── component-hierarchy.md # ✅ React component structure
│   ├── deployment/               # Deployment guides (to create)
│   ├── guides/
│   │   └── development-workflow.md # ✅ Git workflow & best practices
│   ├── templates/
│   │   ├── frontend.env.example  # ✅ Frontend environment template
│   │   └── backend.env.example   # ✅ Backend environment template
│   └── README.md                 # Documentation guidelines
│
├── .github/                      # 🔧 GitHub configuration
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md         # ✅ Bug report template
│   │   └── feature_request.md    # ✅ Feature request template
│   └── pull_request_template.md  # ✅ PR template
│
└── scripts/                      # 🔧 Automation scripts
    └── README.md                 # Script guidelines
```

### 📝 Directory Guidelines

**Where to put files:**

| File Type | Location | Example |
|-----------|----------|---------|
| Curriculum content | `curriculum/` | Markdown lesson files |
| Teaching code examples | `curriculum/code-examples/` | Python examples for Module 17 |
| Application source code | `app/frontend/` or `app/backend/` | React components, API routes |
| Component-specific docs | Component's `README.md` | `app/frontend/README.md` |
| Project-wide documentation | `docs/` | API specs, architecture, checklists |
| Deployment guides | `docs/deployment/` | Google Cloud setup |
| Automation scripts | `scripts/` | Setup, deployment, database scripts |
| AI agent configurations | `cursor/rules/` | Agent rule files (.mdc) |
| UI design references | `UI-examples/` | **HTML examples to mirror** |

**Note:** READMEs can stay in their relevant directories (e.g., `app/frontend/README.md`), but comprehensive documentation belongs in `docs/`.

## 🎓 Key Features

### For Students
- **Progressive Learning**: Four tracks from beginner to architect
- **Interactive Content**: Engaging lessons with visualizations
- **Hands-on Practice**: Coding exercises and real projects
- **Progress Tracking**: Track completion through modules
- **Assessments**: 10 questions/tasks per module (170 total)
- **AI Trading Bot**: Build and customize your own trading bot

### For Instructors
- **Admin Dashboard**: Manage students and content
- **Progress Monitoring**: Track student completion and scores
- **Content Management**: Update curriculum materials
- **Analytics**: View engagement and performance metrics

### Technical Highlights
- **Full TypeScript**: Type-safe frontend and API contracts
- **Async Architecture**: Non-blocking operations throughout
- **LLM-Agnostic Bot**: Works with any LLM provider
- **Responsive Design**: Mobile-first, accessible interface
- **RESTful API**: Clean, well-documented endpoints
- **Database Migrations**: Version-controlled schema changes

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ and npm/yarn
- Python 3.11+
- PostgreSQL 15+
- Git

### Installation

#### Frontend Setup
```bash
cd app/frontend
npm install
npm run dev
```

#### Backend Setup
```bash
cd app/backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn main:app --reload --port 8000
```

#### Database Setup
```bash
# Create PostgreSQL database
createdb crypto_curriculum

# Set environment variables
export DATABASE_URL="postgresql://user:password@localhost/crypto_curriculum"
export SECRET_KEY="your-secret-key"
export LLM_API_KEY="your-llm-api-key"
```

## 📝 Content Development

Each curriculum module follows a structured template:

1. **Core Definition**: Clear, simple explanation
2. **Simple Analogies**: Minimum 2 relatable analogies
3. **Key Talking Points**: Exhaustive itemized list
4. **Step-by-Step Process**: How it works (if applicable)
5. **Relevance/Importance**: Why it matters
6. **Pros & Cons**: Balanced view of trade-offs
7. **Common Misconceptions**: What beginners get wrong
8. **Critical Warnings**: Security and financial risks
9. **Assessment**: 10 questions/tasks per module

See [`curriculum/blockchain curriculum part 1.md`](curriculum/blockchain curriculum part 1.md) for complete example.

## 🧪 Testing

### Frontend Tests
```bash
cd app/frontend
npm run test
npm run test:coverage
```

### Backend Tests
```bash
cd app/backend
pytest
pytest --cov=app
```

### E2E Tests
```bash
npm run test:e2e
```

## 🐳 Docker Deployment

```bash
# Build containers
docker-compose build

# Run services
docker-compose up -d

# View logs
docker-compose logs -f
```

## 📊 Current Status

### ✅ Phase 1: Planning & Content - COMPLETE
- [x] Complete curriculum content (Parts 1-4, all 17 modules)
- [x] Module 17 code examples (AI trading bot framework)
- [x] AI agent system for development
- [x] Design examples and prototypes
- [x] Project structure and documentation
- [x] GitHub repository with branch strategy
- [x] Database schema design
- [x] API endpoint specifications
- [x] Component hierarchy planning
- [x] Environment configuration templates
- [x] Development workflow documentation
- [x] GitHub issue/PR templates

**Total Curriculum:** 49+ hours of instruction across 4 tracks

### 📋 Phase 2: Development - READY TO START

**Complete Development Checklist:** See [Development Checklist](docs/DEVELOPMENT_CHECKLIST.md) for detailed 20-week development plan

#### Foundation (Weeks 1-2)
- [ ] Initialize frontend (Vite + React + MUI + Liquid Glass UI + Framer Motion)
- [ ] Initialize backend (FastAPI + PostgreSQL + SQLAlchemy)
- [ ] Implement complete database schema (16 tables)
- [ ] Build JWT authentication with role-based access
- [ ] Set up development environment

#### Student Core Features (Weeks 3-4)
- [ ] Module and lesson display system
- [ ] Progress tracking dashboard
- [ ] Auto-graded assessments (MC, T/F)
- [ ] Student progress visualization
- [ ] Responsive Liquid Glass UI implementation

#### Instructor Features (Week 5)
- [ ] Instructor dashboard with analytics
- [ ] Cohort management (create, enroll, assign)
- [ ] Manual grading interface with rubrics
- [ ] Student monitoring and at-risk detection
- [ ] Grade export and reporting

#### Code Submission & Review (Week 6)
- [ ] Deferred to Phase 3 future enhancements (tracked below)

#### Communication & Collaboration (Week 7)
- [ ] Discussion forums (module-specific)
- [ ] Forum posts, replies, upvoting
- [ ] Built-in AI learning assistant
- [ ] Notification system
- [ ] Email notifications (configurable)

#### Gamification & Engagement (Week 8)
- [ ] Achievement and badge system (20+ badges)
- [ ] Student portfolio showcase
- [ ] Leaderboard (opt-in, privacy-focused)
- [ ] Advanced analytics for students and instructors

#### AI Trading Bot Integration (Week 9)
- [ ] Bot configuration interface
- [ ] Backtesting system with historical data
- [ ] Paper trading simulation
- [ ] Performance analytics dashboard
- [ ] Strategy comparison tools

#### Polish & Content (Weeks 10-12)
- [ ] Create 170 assessment questions
- [ ] Import all curriculum content
- [ ] Comprehensive testing (unit, integration, E2E)
- [ ] UI/UX refinement across all screens
- [ ] Accessibility audit (WCAG 2.1 AA)
- [ ] Beta testing with real students
- [ ] Documentation completion

### 🚀 Phase 3: Future Enhancements
- [ ] GitHub integration for code submissions
- [ ] Code viewer with syntax highlighting
- [ ] Instructor code review tools with inline comments
- [ ] Rubric-based grading for coding tasks
- [ ] Peer review system (anonymous, structured)
- [ ] Submission versioning and revision workflow
- Coding assessments continue to be reviewed externally per curriculum design.

### 🚀 Phase 3: Deployment - UPCOMING
- [ ] CI/CD pipeline setup
- [ ] Production environment configuration
- [ ] Performance optimization
- [ ] Security audit
- [ ] Documentation finalization
- [ ] Beta testing with students
- [ ] Production deployment

## 📚 Documentation Quick Links

### Getting Started
- [Project Scope](docs/PROJECT_SCOPE.md) - Application purpose and scope
- [Development Workflow](docs/guides/development-workflow.md) - Git workflow and best practices

### Architecture & Design
- [Database Schema](docs/architecture/database-schema.md) - Complete database design (16 tables) and ERD
- [Educational Framework](docs/architecture/educational-framework.md) - Multi-instructor/student pedagogy and features
- [Component Hierarchy](docs/architecture/component-hierarchy.md) - React component structure
- [API Endpoints](docs/api/endpoints.md) - Complete API reference
- [Development Checklist](docs/DEVELOPMENT_CHECKLIST.md) - Complete 20-week development plan

### Configuration
- [Frontend .env Template](docs/templates/frontend.env.example) - Frontend environment variables
- [Backend .env Template](docs/templates/backend.env.example) - Backend environment variables

### Curriculum
- [Curriculum Outline](curriculum/blockchain%20curriculum%20outline.md) - Complete course structure
- [Module 17 Code Examples](curriculum/code-examples/module-17/) - AI trading bot examples

### AI Agent System
- [AI Agent System Guide](cursor/AI_AGENT_SYSTEM.md) - How to use the development agents

---

## 🤝 Contributing

This project is developed for Universal Tech Movement in Austin, TX.

**Repository:** https://github.com/TCoder920/crypto-curriculum

**Workflow:**
1. Fork the repository
2. Create a feature branch from `development`
3. Make your changes
4. Submit a pull request
5. See [Development Workflow Guide](docs/guides/development-workflow.md) for details

**Questions or contributions:** Please create an issue on GitHub.

## 📄 License

[To be determined based on organization requirements]

## 🙏 Acknowledgments

- **Universal Tech Movement** - Austin, TX non-profit organization
- **Target Audience** - Complete beginners with no technical background
- **Educational Focus** - Comprehensive, accessible, practical learning

---

**Built with ❤️ for the next generation of blockchain developers**
