# Project Scope & Purpose

## 🎯 Application Purpose

The **Crypto Curriculum Platform** is a **Learning Management System (LMS)** designed to deliver cryptocurrency and blockchain education content to students of Universal Tech Movement (Austin, TX).

### What This Application IS:
✅ **Content Delivery Platform** - Display curriculum lessons and materials  
✅ **Assessment System** - Quiz students on their understanding  
✅ **Progress Tracker** - Monitor student advancement through modules  
✅ **Discussion Forum** - Allow students to ask questions and collaborate  
✅ **Instructor Dashboard** - Enable instructors to monitor and grade students  
✅ **AI Learning Assistant** - Provide instant help and guidance  

### What This Application IS NOT:
❌ **Code Development Environment** - Students code in external IDEs (Cursor, VS Code)  
❌ **Code Hosting Platform** - No GitHub integration or code storage  
❌ **Project Submission System** - Projects managed outside the platform  
❌ **Code Review Tool** - Instructors review code on their own computers  

---

## 🎓 Student Learning Workflow

```
1. Student logs into platform
   ↓
2. Views module content (lessons, videos, diagrams)
   ↓
3. Completes auto-graded assessments (multiple choice, true/false)
   ↓
4. Answers short-answer questions (instructor-graded in platform)
   ↓
5. Progress tracked automatically
   ↓
6. For coding modules (11-17):
   - Reads lesson explaining concepts in platform
   - Completes quiz on concepts in platform
   - Opens Cursor/VS Code on their own computer
   - Writes code following curriculum guide
   - Tests code locally
   - Shows code to instructor (in person, Zoom, or email)
   - Instructor grades manually outside platform
   ↓
7. Moves to next module
```

---

## 💻 Technical Development Outside Platform

### Modules 11-13 (Developer Track)
**In Platform:** Lessons explaining Solidity, smart contracts, dApp development  
**Outside Platform:** Students write and test smart contracts in Cursor/VS Code  
**Assessment:** Short answer questions + instructor reviews code offline

### Modules 14-17 (Architect Track)
**In Platform:** Lessons on building tokens, NFTs, blockchains, AI bots  
**Outside Platform:** Students build actual projects in their own development environment  
**Assessment:** Knowledge quizzes + instructor evaluates projects offline

---

## 🏗️ Application Architecture

```
┌─────────────────────────────────────────────┐
│         Crypto Curriculum Platform          │
│              (LMS Application)              │
└─────────────────────────────────────────────┘
                      │
        ┌─────────────┴─────────────┐
        │                           │
┌───────▼────────┐        ┌────────▼────────┐
│   STUDENTS     │        │  INSTRUCTORS    │
│                │        │                 │
│  Read Lessons  │        │  Monitor        │
│  Take Quizzes  │        │  Grade Quizzes  │
│  Ask Questions │        │  Answer Forums  │
│  Track Progress│        │  View Analytics │
└───────┬────────┘        └────────┬────────┘
        │                          │
        │                          │
   FOR CODING:                FOR CODING:
        │                          │
        ▼                          ▼
┌────────────────┐        ┌─────────────────┐
│  Cursor/VS Code│        │ Review Offline  │
│  (Student PC)  │───────→│ (Zoom/Email)    │
│                │ share  │                 │
│  Write Code    │  code  │  Provide        │
│  Test Locally  │        │  Feedback       │
└────────────────┘        └─────────────────┘
```

---

## 🎨 Design Reference

**UI Design:** The platform's visual design should mirror the structure and aesthetic of:
- **Primary Reference:** `UI-examples/part 1 webpage example.html` ← **MIRROR THIS LAYOUT**
- **Additional Reference:** `UI-examples/part 1 infographic example.html`
- **Design System:** Apple Liquid Glass UI with adaptive materials

**Key Elements from HTML Example:**
- Sticky sidebar navigation (responsive mobile/desktop)
- Card-based content layout
- Clean, modern "Learning Hub" aesthetic
- Professional color scheme (#0d6efd primary)
- Smooth scroll interactions
- Responsive design patterns

**Liquid Glass Enhancements:**
- Translucent glass surfaces with backdrop blur
- Adaptive opacity on scroll
- Fluid motion with spring physics (Framer Motion)
- Lensing effects on hover
- Concentric geometry (rounded corners: 12px, 16px, 24px)

---

## 📚 Content Structure

### 17 Modules (No Time Constraints)
- **Part 1 (Modules 1-7):** User Track - Foundations
- **Part 2 (Modules 8-10):** Power User/Analyst Track
- **Part 3 (Modules 11-13):** Developer Track (concepts only, coding done externally)
- **Part 4 (Modules 14-17):** Architect Track (concepts + AI bot guide, building done externally)

### Per Module:
- **Lessons:** Text content (Markdown), analogies, step-by-step guides
- **Assessments:** 10 questions/tasks
  - 3-4 Multiple choice (auto-graded)
  - 2-3 True/False (auto-graded)
  - 2-3 Short answer (instructor-graded in platform)
  - 2-3 Practical tasks (instructor-graded offline for coding modules)

---

## 🛠️ Tech Stack (Finalized)

### Frontend
- **Framework:** React 18.3 with TypeScript
- **Build Tool:** Vite 5.4
- **UI Library:** Material-UI (MUI) v7
- **Design:** Apple Liquid Glass UI (translucent, adaptive, fluid)
- **Styling:** Tailwind CSS + Emotion (CSS-in-JS)
- **Animation:** Framer Motion (spring physics, morphing)
- **Routing:** React Router v6
- **State:** React Query (TanStack Query)
- **API Client:** Axios

### Backend
- **Framework:** FastAPI (Python 3.11+)
- **Database ORM:** SQLAlchemy 2.0 (async)
- **Database:** PostgreSQL 15+
- **Migrations:** Alembic
- **Validation:** Pydantic v2
- **Auth:** JWT with bcrypt
- **Testing:** Pytest

### Hosting (Google Cloud Platform)
- **Compute:** Cloud Run (containerized apps)
- **Database:** Cloud SQL (managed PostgreSQL)
- **Storage:** Cloud Storage (profile pics, images)
- **CDN:** Cloud CDN (fast global delivery)
- **Monitoring:** Cloud Logging + Cloud Monitoring
- **Secrets:** Secret Manager
- **Domain:** Custom domain with Cloud DNS
- **Email:** SendGrid or Cloud-native solution

### External Services
- **Email Delivery:** SendGrid (Google partner)
- **AI Assistant:** OpenAI or Anthropic (for chatbot)
- **Analytics:** Google Analytics 4
- **Error Tracking:** Google Cloud Error Reporting

---

## 💰 Cost Structure (Google Cloud)

### Google for Nonprofits Benefits
- **$3,000/year** Google Cloud credits
- **$10,000/month** Google Ads grant
- **Free/discounted** Google Workspace
- **Support** for educational institutions

### Estimated Monthly Costs (After Setup)

**With Non-Profit Credits (Year 1):**
```
Google Cloud Run (frontend + backend): $30/month
Cloud SQL PostgreSQL (10GB): $20/month
Cloud Storage: $5/month
Cloud CDN: $10/month
Logging & Monitoring: $5/month
---
Subtotal GCP: $70/month
Minus credits: -$70/month
Net GCP Cost: $0/month

External:
- Domain: $15/year ($1.25/month)
- SendGrid: Free tier (100 emails/day)
- LLM API (chatbot): ~$10-20/month

TOTAL YEAR 1: ~$10-20/month
```

**After Credits (Year 2+):**
```
GCP Services: $70/month
Domain: $1.25/month
Email: $0-15/month (if exceed free tier)
LLM API: $10-20/month

TOTAL: ~$80-100/month
```

**At Scale (200+ students):**
- Upgrade Cloud SQL: +$30/month
- Add backend replicas: +$30/month
- Increased bandwidth: +$20/month
- **TOTAL: ~$150-180/month**

---

## 📊 Success Criteria

### Launch Criteria (Minimum)
- ✅ All 17 modules content loaded
- ✅ 170 assessment questions created
- ✅ Authentication working
- ✅ Students can read content and take quizzes
- ✅ Instructors can see progress and grade
- ✅ Hosted on Google Cloud with custom domain
- ✅ Privacy Policy and Terms of Service posted
- ✅ HTTPS enabled
- ✅ Backup system working

### Success Metrics (Post-Launch)
- **Engagement:** >80% of enrolled students active weekly
- **Completion:** >60% complete their chosen track
- **Satisfaction:** >4.5/5 student rating
- **Performance:** <2 second page loads
- **Uptime:** >99.5% availability
- **Support:** <24 hour response time

---

## 🔄 Development vs. Operations

### Development (You're Building)
- The LMS platform application
- Content delivery system
- Assessment and grading tools
- Progress tracking
- Forums and communication

### Operations (After Launch)
- Content updates (add new modules, update existing)
- User management (enroll students, assign instructors)
- Monitor performance
- Respond to support tickets
- Review analytics and improve

### NOT Building
- Code development tools for students
- IDE integrations
- GitHub classroom features
- Automated code testing
- Project hosting

---

## 📋 Next Steps

See comprehensive development checklist in: **`docs/DEVELOPMENT_CHECKLIST.md`** (to be created)

---

**Last Updated:** 2025-11-01  
**Status:** Planning Complete, Ready for Development
