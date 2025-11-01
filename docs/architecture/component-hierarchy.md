# Frontend Component Hierarchy

This document outlines the React component structure for the Crypto Curriculum Platform.

## Component Architecture

```
App (Root)
├── ThemeProvider (MUI + Liquid Glass)
├── Router
│
├── Layout Components
│   ├── AppLayout
│   │   ├── GlassNavigation (Sticky sidebar)
│   │   ├── Header (Fluid shrinking header)
│   │   └── MainContent (Content area)
│   │
│   └── AuthLayout (For login/register pages)
│
├── Page Components (Routes)
│   ├── HomePage
│   ├── DashboardPage
│   ├── ModulePage
│   ├── LessonPage
│   ├── AssessmentPage
│   ├── TradingBotPage
│   ├── ProfilePage
│   ├── LoginPage
│   └── RegisterPage
│
├── Feature Components
│   ├── Modules
│   │   ├── ModuleCard (Glass card with module info)
│   │   ├── ModuleList (Grid of modules)
│   │   ├── ModuleProgress (Progress tracker)
│   │   └── ModuleDetails
│   │
│   ├── Lessons
│   │   ├── LessonContent (Markdown renderer)
│   │   ├── LessonNavigation (Previous/Next)
│   │   └── LessonProgress
│   │
│   ├── Assessments
│   │   ├── QuestionCard
│   │   ├── MultipleChoice
│   │   ├── TrueFalse
│   │   ├── ShortAnswer
│   │   ├── CodingTask
│   │   └── QuizResults
│   │
│   ├── TradingBot
│   │   ├── BotDashboard
│   │   ├── BotConfiguration
│   │   ├── BacktestResults
│   │   ├── LiveTradingView
│   │   └── StrategyEditor
│   │
│   └── Progress
│       ├── OverallProgress (Circular progress)
│       ├── TrackProgress (By curriculum track)
│       └── CertificateDisplay
│
└── Shared Components (Glass UI Library)
    ├── GlassCard
    ├── GlassButton
    ├── GlassSidebar
    ├── GlassModal
    ├── GlassInput
    ├── FluidNavigation
    └── LoadingSpinner
```

## Component Responsibilities

### Layout Components

**`AppLayout`**
- Main application shell
- Provides navigation, header, and content area
- Handles theme toggling
- Manages responsive breakpoints

**`GlassNavigation`**
- Sticky sidebar navigation
- Module list with completion status
- Fluid collapse on scroll
- Translucent glass effect

**`Header`**
- User profile dropdown
- Theme toggle
- Notifications
- Shrinks on scroll (fluid motion)

---

### Page Components

**`DashboardPage`**
- Overview of all modules
- Progress summary
- Recent activity
- Quick actions

**`ModulePage`**
- Module overview
- List of lessons
- Assessment access
- Prerequisites check

**`LessonPage`**
- Lesson content (Markdown)
- Navigation controls
- Progress tracking
- Related resources

**`AssessmentPage`**
- Quiz interface
- Question navigation
- Timer (optional)
- Results display

**`TradingBotPage`**
- Bot configuration
- Backtest interface
- Live trading (paper only for students)
- Performance analytics

---

### Feature Components

**`ModuleCard`**
- Glass card displaying module info
- Progress ring
- Duration badge
- Lock icon (if prerequisites not met)
- Hover effects (lensing, elevation)

**`QuestionCard`**
- Question display
- Answer input (type-specific)
- Submit button
- Feedback display
- Explanation panel

**`BotConfiguration`**
- LLM provider selection
- Strategy parameters
- Data source toggles
- Risk management settings
- Save/load configurations

---

### Shared Components (Glass UI)

All shared components follow the Apple Liquid Glass design:
- **Adaptive Material:** Opacity changes on scroll
- **Translucency:** Backdrop blur and saturation
- **Fluid Motion:** Spring animations, morphing shapes
- **Concentric Geometry:** Consistent border radius (12px, 16px, 24px, full)

**`GlassCard`**
```tsx
<GlassCard elevated={true} className="p-6">
  {children}
</GlassCard>
```

**`GlassButton`**
```tsx
<GlassButton variant="primary" onClick={handleClick}>
  Submit
</GlassButton>
```

---

## State Management

### Local State (useState)
- Component-specific UI state
- Form inputs
- Modal open/close

### Context API
- Theme (light/dark mode)
- Auth (current user)
- Module progress (global)

### React Query (TanStack Query)
- API data fetching
- Caching
- Optimistic updates
- Background refetching

**Example:**
```tsx
const { data: modules } = useQuery({
  queryKey: ['modules'],
  queryFn: () => api.getModules()
});
```

---

## Data Flow

```
User Action
    ↓
Component Event Handler
    ↓
API Service Layer (axios)
    ↓
Backend API (/api/v1/...)
    ↓
Response
    ↓
React Query Cache Update
    ↓
Component Re-render
    ↓
UI Update (with fluid animations)
```

---

## Routing Structure

```
/                           → HomePage
/dashboard                  → DashboardPage (requires auth)
/modules                    → ModulesListPage
/modules/:id                → ModulePage
/modules/:id/lessons/:lessonId → LessonPage
/modules/:id/assessment     → AssessmentPage
/trading-bot                → TradingBotPage (Module 17 only)
/trading-bot/backtest       → BacktestPage
/profile                    → ProfilePage
/login                      → LoginPage
/register                   → RegisterPage

/admin/users                → AdminUsersPage (admin only)
/admin/analytics            → AdminAnalyticsPage (admin/teacher)
```

---

## Styling Approach

### Tailwind CSS (Utility Classes)
```tsx
<div className="rounded-3xl p-6 bg-white dark:bg-dark-surface">
```

### MUI Components (Pre-built)
```tsx
<Button variant="contained" color="primary">
```

### Emotion (CSS-in-JS for complex styles)
```tsx
const StyledCard = styled.div`
  backdrop-filter: blur(20px);
  background: rgba(255, 255, 255, 0.7);
`;
```

### Framer Motion (Animations)
```tsx
<motion.div
  whileHover={{ scale: 1.02 }}
  transition={{ type: "spring" }}
>
```

---

## Performance Considerations

### Code Splitting
- Lazy load pages: `const ModulePage = lazy(() => import('./pages/ModulePage'))`
- Lazy load heavy components (code editor, charts)

### Memoization
- `useMemo` for expensive calculations
- `useCallback` for event handlers passed to children
- `React.memo` for pure components

### Virtual Scrolling
- Use `react-window` for long lists (module list, lesson list)

### Image Optimization
- Use Next/Image or similar for curriculum images
- Lazy load images below fold
- Serve appropriate sizes (responsive)

---

## Accessibility

### ARIA Labels
- All interactive elements labeled
- Role attributes for custom components
- Skip navigation links

### Keyboard Navigation
- Tab order logical
- Focus indicators visible
- Escape to close modals

### Screen Reader Support
- Semantic HTML
- Alt text for images
- Live region announcements for dynamic content

---

## File Organization

```
src/
├── components/
│   ├── layout/
│   │   ├── AppLayout.tsx
│   │   ├── GlassNavigation.tsx
│   │   └── Header.tsx
│   │
│   ├── modules/
│   │   ├── ModuleCard.tsx
│   │   ├── ModuleList.tsx
│   │   └── ModuleProgress.tsx
│   │
│   ├── lessons/
│   │   └── LessonContent.tsx
│   │
│   ├── assessments/
│   │   ├── QuestionCard.tsx
│   │   └── QuizResults.tsx
│   │
│   ├── trading-bot/
│   │   └── BotDashboard.tsx
│   │
│   └── shared/
│       ├── GlassCard.tsx
│       ├── GlassButton.tsx
│       └── LoadingSpinner.tsx
│
├── pages/
│   ├── HomePage.tsx
│   ├── DashboardPage.tsx
│   └── ModulePage.tsx
│
├── hooks/
│   ├── useAuth.ts
│   ├── useProgress.ts
│   └── useTheme.ts
│
├── services/
│   ├── api.ts
│   ├── auth.ts
│   └── modules.ts
│
├── types/
│   ├── user.ts
│   ├── module.ts
│   └── assessment.ts
│
├── theme/
│   ├── theme.ts
│   └── glass.css
│
└── utils/
    ├── formatters.ts
    └── validators.ts
```

---

**Last Updated:** 2025-11-01

