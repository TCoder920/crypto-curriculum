# Development Workflow Guide

This guide outlines the development workflow for contributing to the Crypto Curriculum Platform.

## Branch Strategy

### Main Branches

**`main`** - Production-ready code
- Stable, tested releases
- Protected branch (requires PR and approval)
- Direct pushes forbidden
- Deploy to production

**`development`** - Integration branch (DEFAULT)
- Latest features and fixes
- All feature branches merge here first
- Protected branch (requires PR)
- Deploy to staging

### Feature Branches

**Naming Convention:**
```
feature/short-description
bugfix/short-description
hotfix/critical-issue
refactor/component-name
docs/documentation-update
```

**Examples:**
- `feature/liquid-glass-navigation`
- `bugfix/quiz-scoring-error`
- `hotfix/security-patch`
- `refactor/api-service-layer`
- `docs/api-endpoints`

---

## Development Workflow

### 1. Start New Feature

```bash
# Make sure you're on development branch
git checkout development

# Pull latest changes
git pull origin development

# Create feature branch
git checkout -b feature/your-feature-name
```

### 2. Make Changes

```bash
# Make your changes
# Test locally
# Ensure code quality

# Stage changes
git add .

# Commit with conventional commit message
git commit -m "feat: add liquid glass navigation component"
```

### 3. Push Feature Branch

```bash
# Push to GitHub
git push origin feature/your-feature-name
```

### 4. Create Pull Request

On GitHub:
1. Go to repository
2. Click "Pull requests" → "New pull request"
3. Base: `development` ← Compare: `feature/your-feature-name`
4. Fill out PR template
5. Request reviewers
6. Submit PR

### 5. Code Review

- Address reviewer feedback
- Make requested changes
- Push additional commits to same branch
- Request re-review

### 6. Merge

Once approved:
- Squash and merge (recommended for features)
- Delete feature branch after merge

---

## Commit Message Convention

We use **Conventional Commits** for clear commit history.

### Format
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks (dependencies, config)
- `ci`: CI/CD changes

### Examples

**Feature:**
```bash
git commit -m "feat(frontend): add liquid glass card component

- Implemented GlassCard with adaptive material
- Added lensing effect on hover
- Includes light/dark theme support"
```

**Bug Fix:**
```bash
git commit -m "fix(api): correct quiz scoring calculation

Fixes issue where partial credit wasn't awarded properly"
```

**Documentation:**
```bash
git commit -m "docs(architecture): add component hierarchy diagram"
```

**Breaking Change:**
```bash
git commit -m "feat(api)!: change authentication to JWT

BREAKING CHANGE: old session-based auth no longer supported"
```

---

## Code Review Guidelines

### As a Reviewer

**Check for:**
- ✅ Code follows project style
- ✅ No security vulnerabilities
- ✅ Proper error handling
- ✅ Tests included/updated
- ✅ Documentation updated
- ✅ No console logs or debug code
- ✅ Responsive design (if UI)
- ✅ Accessibility considerations

**Provide:**
- Constructive feedback
- Specific suggestions
- Praise for good work
- Questions if unclear

### As an Author

**Prepare:**
- Self-review before requesting review
- Add comments for complex logic
- Update documentation
- Ensure all tests pass
- Check for console errors

**Respond:**
- Address all feedback
- Ask questions if unclear
- Make requested changes promptly
- Thank reviewers

---

## Testing Requirements

### Before Creating PR

**Frontend:**
```bash
npm run lint          # ESLint checks
npm run type-check    # TypeScript checks
npm run test          # Unit tests
npm run build         # Ensure build succeeds
```

**Backend:**
```bash
pytest                # Run all tests
pytest --cov=app      # Check coverage
ruff check .          # Linting
mypy .                # Type checking
```

### Minimum Coverage
- Unit tests: 70% coverage
- Integration tests for all API endpoints
- E2E tests for critical user flows

---

## Release Process

### Development → Main (Release)

**When:**
- After sprint completion
- When feature set is stable
- After thorough testing on staging

**Process:**
1. Create release PR: `development` → `main`
2. Update version number (in package.json, __init__.py)
3. Update CHANGELOG.md
4. Full regression testing
5. Get approval from project lead
6. Merge to main
7. Tag release: `git tag v1.0.0`
8. Deploy to production

---

## Hotfix Process

For critical production bugs:

```bash
# Branch from main
git checkout main
git pull origin main
git checkout -b hotfix/critical-issue

# Fix the issue
# Test thoroughly

# Commit and push
git commit -m "hotfix: fix critical security issue"
git push origin hotfix/critical-issue

# Create PR to main
# After merge to main, also merge to development
```

---

## Local Development Setup

### First Time Setup

```bash
# Clone repository
git clone https://github.com/TCoder920/crypto-curriculum.git
cd crypto-curriculum

# Checkout development branch
git checkout development

# Frontend setup
cd app/frontend
npm install
cp ../../docs/templates/frontend.env.example .env.local
npm run dev

# Backend setup (new terminal)
cd app/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp ../../docs/templates/backend.env.example .env
# Edit .env with your database credentials
alembic upgrade head
uvicorn main:app --reload

# Database setup (new terminal)
createdb crypto_curriculum
```

---

## Daily Development

### Starting Work

```bash
# Get latest changes
git checkout development
git pull origin development

# Create/switch to feature branch
git checkout -b feature/my-feature

# Start services
npm run dev          # Frontend
uvicorn main:app --reload  # Backend
```

### During Work

- Commit frequently with meaningful messages
- Push to remote regularly (backup)
- Run tests before committing
- Keep PR scope focused (one feature)

### End of Day

```bash
# Push your work
git push origin feature/my-feature

# If ready, create PR
# Otherwise, continue tomorrow
```

---

## Best Practices

### General
- Write self-documenting code
- Add comments for complex logic
- Keep functions small and focused
- Follow DRY principle
- Handle errors gracefully

### Frontend
- Use TypeScript strictly
- Prefer functional components
- Use hooks appropriately
- Memoize expensive operations
- Keep components under 200 lines

### Backend
- Use async/await consistently
- Validate inputs with Pydantic
- Use proper HTTP status codes
- Log important events
- Write docstrings

### Git
- Commit early and often
- Write descriptive commit messages
- Keep commits focused (one logical change)
- Don't commit secrets or .env files
- Review your own diff before committing

---

## Troubleshooting

### Common Issues

**"Merge conflict"**
```bash
git checkout development
git pull origin development
git checkout feature/your-branch
git merge development
# Resolve conflicts
git commit
git push
```

**"Branch is behind"**
```bash
git pull origin development
git push
```

**"Accidentally committed to wrong branch"**
```bash
# If not pushed yet
git reset HEAD~1  # Undo last commit, keep changes
git stash
git checkout correct-branch
git stash pop
git commit
```

---

## Getting Help

1. Check this documentation
2. Ask in team chat/Slack
3. Review existing code for patterns
4. Consult official docs (React, FastAPI, etc.)
5. Use AI assistants (ChatGPT, Gemini) for learning
6. Create issue for bugs or feature requests

---

**Last Updated:** 2025-11-01

