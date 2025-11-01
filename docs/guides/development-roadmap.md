# Development Roadmap

Complete development plan incorporating educational framework requirements for multi-instructor, multi-student platform.

---

## 🎯 Phase 2: Application Development

### Stage 1: Foundation (Weeks 1-2)

#### 1.1 Environment Setup
- [ ] Initialize frontend (Vite + React + TypeScript + MUI v7 + Tailwind + Framer Motion)
- [ ] Initialize backend (FastAPI + SQLAlchemy + PostgreSQL)
- [ ] Set up development database
- [ ] Configure environment variables from templates
- [ ] Test local development workflow

#### 1.2 Core Database Schema
- [ ] Implement all SQLAlchemy models (17 tables)
  - Users, Modules, Lessons, Assessments
  - UserProgress, QuizAttempts
  - Cohorts, CohortMembers
  - CodeSubmissions, PeerReviews
  - ForumPosts, ForumVotes
  - BotConfigurations, TradingStrategies
  - Achievements, UserAchievements, LearningResources
- [ ] Create initial Alembic migration
- [ ] Seed database with curriculum data (17 modules)
- [ ] Create sample data for testing

#### 1.3 Authentication System
- [ ] JWT authentication implementation
- [ ] User registration endpoint
- [ ] Login endpoint with token generation
- [ ] Password hashing (bcrypt)
- [ ] Role-based access control (student, instructor, admin)
- [ ] Protected route middleware

**Deliverable:** Users can register, login, and access role-specific features

---

### Stage 2: Student Core Features (Weeks 3-4)

#### 2.1 Module & Lesson Display
- [ ] API endpoints for modules and lessons
- [ ] Frontend module list with glass card design
- [ ] Lesson content viewer (Markdown rendering)
- [ ] Navigation between lessons
- [ ] Prerequisite checking and enforcement
- [ ] Responsive design (mobile-first)

#### 2.2 Progress Tracking
- [ ] Track lesson completion
- [ ] Calculate module progress percentage
- [ ] Update last accessed timestamp
- [ ] Track time spent per module
- [ ] Student progress dashboard
- [ ] Visual progress indicators (circular progress, badges)

#### 2.3 Assessment System - Auto-Graded
- [ ] Multiple choice questions
- [ ] True/False questions
- [ ] Auto-grading logic
- [ ] Immediate feedback display
- [ ] Show correct answers with explanations
- [ ] Track attempt count and scores
- [ ] Prevent progression if score < 70%

**Deliverable:** Students can view content, track progress, and complete auto-graded assessments

---

### Stage 3: Instructor Features (Week 5)

#### 3.1 Instructor Dashboard
- [ ] View assigned cohorts
- [ ] Student list with progress overview
- [ ] At-risk student detection (inactive, failing)
- [ ] Grading queue (pending manual reviews)
- [ ] Cohort analytics (average scores, completion rates)

#### 3.2 Cohort Management
- [ ] Create cohorts (name, dates, description)
- [ ] Enroll students in cohorts
- [ ] Assign instructors to cohorts
- [ ] View cohort member list
- [ ] Remove students from cohorts

#### 3.3 Manual Grading System
- [ ] Short answer question grading interface
- [ ] Rubric-based grading for coding tasks
- [ ] Provide written feedback
- [ ] Grade tracking and history
- [ ] Bulk grading tools
- [ ] Export grades to CSV

**Deliverable:** Instructors can manage cohorts and grade student submissions

---

### Stage 4: Code Submission & Review (Week 6)

#### 4.1 Code Submission System
- [ ] GitHub URL submission interface
- [ ] File upload system (fallback)
- [ ] Support multiple file types (.sol, .py, .js, .zip)
- [ ] Submission versioning (resubmit capability)
- [ ] Syntax-highlighted code viewer
- [ ] Download/clone functionality

#### 4.2 Code Review Features
- [ ] Instructor code review interface
- [ ] Inline commenting on code
- [ ] Rubric-based evaluation
  - Functionality scoring
  - Code quality scoring
  - Security assessment
  - Documentation scoring
- [ ] Grade calculation from rubric
- [ ] Revision request workflow

#### 4.3 Peer Review System
- [ ] Anonymous peer assignment (2-3 reviewers per submission)
- [ ] Peer review interface with simplified rubric
- [ ] Comment system
- [ ] Peer feedback aggregation
- [ ] Instructor review of peer reviews
- [ ] Engagement tracking (peer reviews completed)

**Deliverable:** Students can submit code, receive instructor feedback, and participate in peer reviews

---

### Stage 5: Communication & Collaboration (Week 7)

#### 5.1 Discussion Forums
- [ ] Module-specific forum boards
- [ ] Create posts and replies
- [ ] Markdown support in posts
- [ ] Code blocks with syntax highlighting
- [ ] Upvote/downvote system
- [ ] Mark questions as solved
- [ ] Pin important posts (instructor only)
- [ ] Search and filter posts

#### 5.2 Real-Time Features
- [ ] Notification system (new feedback, forum replies)
- [ ] Email notifications (configurable)
- [ ] Activity feed
- [ ] Online status indicators (optional)

#### 5.3 AI Learning Assistant
- [ ] Built-in chat interface
- [ ] Context-aware responses (knows student's current module)
- [ ] Suggest relevant curriculum sections
- [ ] Block direct assessment answers
- [ ] Log interactions for instructor review
- [ ] Escalation to human instructor

**Deliverable:** Students can ask questions, collaborate, and get instant AI assistance

---

### Stage 6: Gamification & Engagement (Week 8)

#### 6.1 Achievement System
- [ ] Define achievements (20+ badges)
- [ ] Achievement criteria evaluation
- [ ] Award achievements automatically
- [ ] Achievement display on profile
- [ ] Badge showcase
- [ ] Points system

#### 6.2 Leaderboard (Optional, Opt-In)
- [ ] Cohort leaderboard
- [ ] Multiple categories (progress, scores, engagement)
- [ ] Privacy controls
- [ ] Anonymous option
- [ ] Top performers showcase

#### 6.3 Student Portfolio
- [ ] Project showcase page
- [ ] Link GitHub repos
- [ ] Add project descriptions
- [ ] Screenshot/demo uploads
- [ ] Public portfolio option (shareable URL)
- [ ] Portfolio export (PDF/website)

**Deliverable:** Engagement features to motivate students and showcase their work

---

### Stage 7: Advanced Features (Week 9)

#### 7.1 Learning Analytics
- [ ] Student performance analytics
- [ ] Module difficulty analysis
- [ ] Completion time tracking
- [ ] Learning pattern detection
- [ ] Personalized recommendations
- [ ] Predict at-risk students

#### 7.2 Instructor Collaboration
- [ ] Shared grading (multiple instructors per cohort)
- [ ] Grading workload distribution
- [ ] Instructor notes on students (private)
- [ ] Instructor-to-instructor messaging
- [ ] Shared resource library

#### 7.3 Content Management (Admin)
- [ ] Edit curriculum content
- [ ] Add/modify assessments
- [ ] Upload new lessons
- [ ] Version control for content
- [ ] Preview changes before publishing
- [ ] Rollback capability

**Deliverable:** Advanced analytics and management tools for instructors and admins

---

### Stage 8: AI Trading Bot Integration (Week 10)

#### 8.1 Bot Configuration Interface
- [ ] LLM provider selection (OpenAI, Anthropic, Ollama)
- [ ] Strategy parameter configuration
- [ ] Data source toggles
- [ ] Risk management settings (position size, stop-loss)
- [ ] Save/load configurations

#### 8.2 Backtesting System
- [ ] Historical data integration
- [ ] Run backtest with student's strategy
- [ ] Display performance metrics
  - Total return, Sharpe ratio, max drawdown
  - Win rate, total trades
  - Equity curve visualization
- [ ] Compare strategies
- [ ] Strategy leaderboard

#### 8.3 Paper Trading Simulation
- [ ] Real-time price feeds (CoinGecko API)
- [ ] Simulated portfolio
- [ ] Order execution simulation
- [ ] Portfolio tracking
- [ ] Trade history
- [ ] Performance dashboard

**Deliverable:** Fully functional AI trading bot framework for Module 17

---

### Stage 9: Polish & Testing (Week 11)

#### 9.1 UI/UX Refinement
- [ ] Apple Liquid Glass UI implementation across all components
- [ ] Fluid animations and transitions
- [ ] Responsive design testing (mobile, tablet, desktop)
- [ ] Accessibility audit (WCAG 2.1 AA)
- [ ] Dark mode polish
- [ ] Loading states and error handling
- [ ] Empty states

#### 9.2 Testing
- [ ] Unit tests (frontend components)
- [ ] Unit tests (backend endpoints)
- [ ] Integration tests (API + database)
- [ ] E2E tests (critical user flows)
- [ ] Load testing (multiple concurrent users)
- [ ] Security testing

#### 9.3 Documentation
- [ ] API documentation (auto-generated from code)
- [ ] Component documentation (Storybook)
- [ ] User guide for students
- [ ] Instructor guide
- [ ] Admin guide
- [ ] Deployment guide

**Deliverable:** Production-ready application with comprehensive testing

---

### Stage 10: Content Integration (Week 12)

#### 10.1 Curriculum Import
- [ ] Create 170 assessment questions (10 per module)
- [ ] Import all 4 curriculum parts into database
- [ ] Create lesson entries for each section
- [ ] Link assessments to modules
- [ ] Set up prerequisite chains
- [ ] Verify all content displays correctly

#### 10.2 Resource Library
- [ ] Add external resources per module
- [ ] Video tutorials
- [ ] Official documentation links
- [ ] Community resources
- [ ] Bonus materials

#### 10.3 Sample Content
- [ ] Create demo cohort
- [ ] Seed sample students with progress
- [ ] Create sample forum discussions
- [ ] Set up achievement examples
- [ ] Generate sample analytics data

**Deliverable:** Platform loaded with complete curriculum and ready for beta testing

---

## 📊 Database Schema Additions

### Additional Tables (Beyond Original Plan)

**For Multi-Instructor Support:**
- ✅ `cohorts` - Class groupings
- ✅ `cohort_members` - Student/instructor assignments

**For Code Submissions:**
- ✅ `code_submissions` - GitHub links or file uploads
- ✅ `peer_reviews` - Peer feedback system

**For Collaboration:**
- ✅ `forum_posts` - Discussion threads
- ✅ `forum_votes` - Upvote/downvote

**For Engagement:**
- ✅ `achievements` - Badge definitions
- ✅ `user_achievements` - Earned badges
- ✅ `learning_resources` - Curated external links

**Total Tables:** 17 (up from original 7)

See `docs/architecture/database-schema.md` for complete schema.

---

## 🎓 Educational Considerations

### Assessment Strategy

**Module 1-10 (Non-Coding):**
- 3-4 Multiple choice
- 2-3 True/False
- 2-3 Short answer
- 1-2 Conceptual tasks

**Module 11-17 (Coding):**
- 2-3 Multiple choice (concepts)
- 1-2 True/False (best practices)
- 1-2 Short answer (explain code)
- 3-4 Coding tasks (hands-on)

### Grading Workload Distribution

**Auto-Graded (60%):**
- Multiple choice
- True/False
- Pattern-matched short answer

**Manual Grading (40%):**
- Open-ended short answer
- Code submissions
- Project reviews

**Time Estimates:**
- Auto-graded: Instant
- Short answer: 2-3 min/question
- Coding task: 10-15 min/submission
- Project review: 20-30 min/project

**For 25 Students:**
- ~40 hours/month instructor time (grading only)
- Distribute across multiple instructors
- Use peer review to reduce load

### Preventing Cheating

**Strategies:**
1. **Randomize Question Order** - Each student sees different order
2. **Question Pools** - Draw from larger pool, each student gets subset
3. **Plagiarism Detection** - Basic code similarity checking
4. **Timed Assessments** - Optional time limits
5. **Proctoring** - Lockdown browser (optional, for certificates)
6. **Unique Projects** - Encourage customization in coding tasks

### Accessibility & Inclusion

**Must Support:**
- Screen readers (ARIA labels, semantic HTML)
- Keyboard navigation
- High contrast mode
- Font size adjustment
- Mobile access
- Slow internet connections (progressive enhancement)

**Language Support (Future):**
- English (primary)
- Spanish (high priority for Texas)
- Multi-language content framework

---

## 🔄 Iterative Development Approach

### Sprint Structure (2-week sprints)

**Sprint 1-2:** Foundation + Student Core
**Sprint 3:** Instructor Features
**Sprint 4:** Code Submission & Review
**Sprint 5:** Communication Tools
**Sprint 6:** Gamification & Analytics
**Sprint 7:** AI Trading Bot
**Sprint 8:** Polish & Testing
**Sprint 9:** Content Integration & Beta

### User Testing Checkpoints

**After Sprint 2:** Student beta (5 volunteers)
- Test: Module viewing, progress tracking, auto-graded assessments
- Collect: UI/UX feedback, bug reports

**After Sprint 4:** Instructor beta (2 instructors)
- Test: Cohort management, grading, analytics
- Collect: Workflow feedback, feature requests

**After Sprint 6:** Full cohort beta (25 students, 2 instructors)
- Test: Complete learning experience
- Collect: Performance metrics, engagement data

**After Sprint 9:** Production-ready
- Final testing with real cohort
- Instructor training
- Official launch

---

## 📋 Feature Prioritization Matrix

### Must Have (MVP)
1. ✅ User authentication (student, instructor, admin roles)
2. ✅ Module and lesson display
3. ✅ Progress tracking
4. ✅ Auto-graded assessments
5. ✅ Manual grading interface
6. ✅ Cohort management
7. ✅ Student dashboard
8. ✅ Instructor dashboard
9. ✅ Code submission (GitHub URL)

### Should Have (Enhanced MVP)
10. Discussion forums
11. AI learning assistant
12. Peer review system
13. Achievement system
14. Basic analytics
15. GitHub integration for code review
16. Email notifications

### Nice to Have (Future Enhancements)
17. Advanced analytics and ML predictions
18. Leaderboards
19. Study groups
20. Office hours scheduling
21. Portfolio export
22. Video integration
23. Mobile app
24. Multi-language support

---

## 🛠️ Technical Implementation Notes

### GitHub Integration

**For Code Submissions:**
```python
# Backend endpoint
@router.post("/submissions")
async def submit_code(
    github_url: str,
    assessment_id: UUID,
    current_user: User
):
    # Validate GitHub URL
    # Extract repo info (user/repo)
    # Optionally: Clone and run basic checks
    # Store submission
    # Notify instructor
```

**Frontend:**
```tsx
<CodeSubmissionForm>
  <Input 
    label="GitHub Repository URL"
    placeholder="https://github.com/username/project-name"
  />
  <Button onClick={submitCode}>Submit Project</Button>
</CodeSubmissionForm>
```

### Real-Time Updates

**Use WebSockets for:**
- Forum post notifications
- New feedback available
- Instructor messages
- Cohort announcements

**Technology:** FastAPI WebSockets + React hooks

### Analytics Pipeline

**Data Collection:**
- User actions logged (page views, time spent, clicks)
- Assessment attempts and scores
- Progress updates
- Engagement metrics

**Processing:**
- Daily aggregation jobs
- Weekly cohort reports
- Monthly platform stats
- ML models for predictions (future)

---

## 📊 Success Metrics

### Student Success
- **Completion Rate:** >70% of enrolled students complete their track
- **Assessment Scores:** Average >80%
- **Engagement:** Average >3 sessions/week
- **Satisfaction:** >4.5/5 rating

### Instructor Efficiency
- **Grading Time:** <10 min per code submission
- **Response Time:** Feedback within 48 hours
- **Workload:** Max 30 students per instructor
- **Satisfaction:** >4/5 rating

### Platform Performance
- **Page Load:** <2 seconds
- **API Response:** <200ms average
- **Uptime:** >99.5%
- **Concurrent Users:** Support 100+ simultaneous

---

## 🚀 Development Workflow

### Using AI Agents in Cursor

**Stage 1-2 (Foundation):**
```
@masterOrchestrator Initialize frontend and backend projects
@frontendComponentAgent Create React app with Liquid Glass UI theme
@backendApiAgent Set up FastAPI with all database models
@databaseSchemaAgent Create migrations for all 17 tables
```

**Stage 2-3 (Student Features):**
```
@frontendComponentAgent Build ModuleCard and ModuleList components
@backendApiAgent Create module and lesson CRUD endpoints
@frontendComponentAgent Implement progress tracking dashboard
```

**Stage 3-4 (Instructor Tools):**
```
@frontendComponentAgent Build instructor dashboard with cohort view
@backendApiAgent Create grading endpoints and analytics
@frontendComponentAgent Implement code review interface
```

**Stage 5+ (Advanced Features):**
```
@tradingBotAgent Build AI trading bot backend framework
@frontendComponentAgent Create bot configuration UI
@backendApiAgent Implement forum system with WebSockets
```

### Testing Strategy

**Per Feature:**
1. Unit tests first (TDD approach)
2. Integration tests
3. Manual testing
4. User acceptance testing

**Before Each Sprint Demo:**
- Full regression testing
- Performance testing
- Security scan
- Accessibility audit

---

## 📅 Recommended Timeline

### 12-Week Development Plan

| Week | Focus | Deliverable |
|------|-------|-------------|
| 1-2  | Foundation | Database + Auth working |
| 3-4  | Student Core | Students can learn and test |
| 5    | Instructor Tools | Teachers can manage cohorts |
| 6    | Code System | Code submission working |
| 7    | Collaboration | Forums and AI assistant |
| 8    | Engagement | Achievements and analytics |
| 9    | Trading Bot | Module 17 features complete |
| 10   | Polish | UI refinement and testing |
| 11   | Content Import | All curriculum loaded |
| 12   | Beta Testing | Ready for first cohort |

**Total:** 3 months from start to production-ready

### Quick Start (4-Week MVP)

If you need to launch faster, focus on:
- Weeks 1-2: Foundation
- Week 3: Student Core (no forums, no peer review)
- Week 4: Basic instructor tools

**Launch with:**
- Content viewing
- Auto-graded assessments
- Manual grading (simple)
- Basic progress tracking

**Add later:**
- Peer review
- Forums
- AI assistant
- Trading bot
- Advanced analytics

---

## 🎯 Next Steps (Immediate Actions)

### 1. Project Initialization
```bash
# Frontend
@frontendComponentAgent Initialize Vite + React 18.3 + TypeScript + MUI v7 
+ Tailwind CSS + Framer Motion with Apple Liquid Glass UI design system

# Backend
@backendApiAgent Initialize FastAPI + SQLAlchemy + PostgreSQL with complete 
database schema including all 17 tables for multi-instructor/student support
```

### 2. Database Setup
```bash
# Create database
createdb crypto_curriculum

# Run migrations
@databaseSchemaAgent Create all SQLAlchemy models and initial Alembic migration 
for 17 tables including cohorts, code submissions, peer reviews, forums, and achievements
```

### 3. Core Authentication
```bash
@backendApiAgent Implement JWT authentication with role-based access control 
(student, instructor, admin) including registration, login, and protected routes
```

### 4. Essential Student Features
```bash
@frontendComponentAgent Build student dashboard with module list, progress tracking, 
and lesson viewer using Liquid Glass UI design

@backendApiAgent Create module/lesson endpoints with prerequisite checking and 
progress tracking
```

### 5. Essential Instructor Features
```bash
@frontendComponentAgent Build instructor dashboard with cohort management, 
student list, and grading queue

@backendApiAgent Create cohort management endpoints and grading system with 
rubric support
```

### 6. Code Submission System
```bash
@frontendComponentAgent Build code submission form with GitHub URL input and 
file upload fallback

@backendApiAgent Create code submission endpoints with GitHub integration 
and grading workflow
```

### 7. Create Assessment Questions
```bash
Create 170 assessment questions (10 per module):
- 3-4 multiple choice per module
- 2-3 true/false per module  
- 2-3 short answer per module
- 2-3 coding/practical tasks per module (Modules 11-17)

Import into database via seed script
```

### 8. Discussion Forums
```bash
@backendApiAgent Implement forum system with posts, replies, voting, and 
module-specific boards

@frontendComponentAgent Build forum UI with thread view, post composer, 
and search functionality
```

### 9. AI Learning Assistant
```bash
@backendApiAgent Create AI chatbot endpoint with context awareness, curriculum 
section suggestions, and assessment answer blocking

@frontendComponentAgent Build chat interface with module context display
```

### 10. Achievement & Portfolio Systems
```bash
@backendApiAgent Implement achievement tracking with automatic badge awarding 
based on progress, scores, and engagement

@frontendComponentAgent Build student portfolio page with project showcase 
and achievement display
```

---

## 🎓 Educational Success Factors

### For Students
1. ✅ Clear learning path with prerequisites
2. ✅ Immediate feedback on auto-graded work
3. ✅ Timely feedback on manual-graded work (<48hrs)
4. ✅ Multiple attempts to master content
5. ✅ Peer collaboration opportunities
6. ✅ AI assistance for instant help
7. ✅ Portfolio to showcase work
8. ✅ Achievements for motivation

### For Instructors
1. ✅ Easy cohort management
2. ✅ Efficient grading tools with rubrics
3. ✅ Analytics to identify struggling students
4. ✅ Communication tools (forums, announcements)
5. ✅ Content management capabilities
6. ✅ Workload distribution across co-instructors
7. ✅ Automated tedious tasks (auto-grading)

### For Organization
1. ✅ Scalable to hundreds of students
2. ✅ Track outcomes and effectiveness
3. ✅ Multiple concurrent cohorts
4. ✅ Content versioning and updates
5. ✅ Data export and reporting
6. ✅ Integration with existing systems

---

**Last Updated:** 2025-11-01  
**Next Review:** After Phase 2 Sprint 1

