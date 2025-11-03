# API Endpoints Reference

Base URL: `http://localhost:8000/api/v1`

## Authentication

All authenticated endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <token>
```

---

## Auth Endpoints

### POST `/auth/register`
Register a new user account.

**Request:**
```json
{
  "email": "student@example.com",
  "username": "student123",
  "password": "SecurePass123!",
  "full_name": "John Doe"
}
```

**Response (201 Created):**
```json
{
  "id": "uuid",
  "email": "student@example.com",
  "username": "student123",
  "full_name": "John Doe",
  "role": "student",
  "created_at": "2025-11-01T12:00:00Z"
}
```

---

### POST `/auth/login`
Authenticate and receive JWT token.

**Request:**
```json
{
  "email": "student@example.com",
  "password": "SecurePass123!"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "id": "uuid",
    "email": "student@example.com",
    "username": "student123",
    "role": "student"
  }
}
```

---

### GET `/auth/me`
Get current authenticated user info.

**Headers:** Requires authentication

**Response (200 OK):**
```json
{
  "id": "uuid",
  "email": "student@example.com",
  "username": "student123",
  "full_name": "John Doe",
  "role": "student",
  "created_at": "2025-11-01T12:00:00Z"
}
```

---

## Modules Endpoints

### GET `/modules`
Get all curriculum modules.

**Query Parameters:**
- `track` (optional) - Filter by track: 'user', 'power-user', 'developer', 'architect'
- `published_only` (optional) - Boolean, default true

**Response (200 OK):**
```json
{
  "modules": [
    {
      "id": 1,
      "title": "Blockchain Technology",
      "description": "Introduction to blockchain fundamentals",
      "track": "user",
      "duration_hours": 2.0,
      "order_index": 1,
      "is_published": true,
      "prerequisites": []
    },
    {
      "id": 2,
      "title": "Web3 Wallets & Security",
      "track": "user",
      "duration_hours": 3.0,
      "order_index": 2,
      "prerequisites": [1]
    }
  ],
  "total": 17
}
```

---

### GET `/modules/{module_id}`
Get detailed module information with lessons and assessments.

**Headers:** Requires authentication

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Blockchain Technology",
  "description": "Introduction to blockchain fundamentals",
  "track": "user",
  "duration_hours": 2.0,
  "lessons": [
    {
      "id": "uuid",
      "title": "What is a Ledger?",
      "content": "# What is a Ledger?\n\n...",
      "lesson_type": "reading",
      "order_index": 1,
      "estimated_minutes": 15
    }
  ],
  "assessments": [
    {
      "id": "uuid",
      "question_text": "What is a distributed ledger?",
      "question_type": "multiple-choice",
      "options": {
        "A": "A centralized database",
        "B": "A shared database across multiple nodes",
        "C": "A private ledger",
        "D": "None of the above"
      },
      "points": 10
    }
  ],
  "user_progress": {
    "status": "in-progress",
    "progress_percent": 45.5,
    "started_at": "2025-11-01T10:00:00Z"
  }
}
```

---

## Progress Endpoints

### GET `/progress`
Get authenticated user's progress across all modules.

**Headers:** Requires authentication

**Response (200 OK):**
```json
{
  "user_id": "uuid",
  "overall_progress": 35.5,
  "modules_completed": 6,
  "modules_in_progress": 2,
  "total_time_minutes": 480,
  "progress_by_module": [
    {
      "module_id": 1,
      "module_title": "Blockchain Technology",
      "status": "completed",
      "progress_percent": 100.0,
      "completed_at": "2025-10-15T14:30:00Z",
      "time_spent_minutes": 120
    },
    {
      "module_id": 2,
      "status": "in-progress",
      "progress_percent": 60.0,
      "started_at": "2025-10-20T09:00:00Z"
    }
  ]
}
```

---

### PUT `/progress/{module_id}`
Update progress for a specific module.

**Headers:** Requires authentication

**Request:**
```json
{
  "status": "in-progress",
  "progress_percent": 75.5
}
```

**Response (200 OK):**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "module_id": 1,
  "status": "in-progress",
  "progress_percent": 75.5,
  "last_accessed": "2025-11-01T12:30:00Z"
}
```

---

### POST `/progress/{module_id}/complete`
Mark a module as completed.

**Headers:** Requires authentication

**Response (200 OK):**
```json
{
  "module_id": 1,
  "status": "completed",
  "progress_percent": 100.0,
  "completed_at": "2025-11-01T12:30:00Z",
  "certificate_eligible": true
}
```

---

## Assessment Endpoints

### POST `/assessments/{assessment_id}/submit`
Submit an answer to an assessment question.

**Headers:** Requires authentication

**Request:**
```json
{
  "user_answer": "B",
  "time_spent_seconds": 45
}
```

**Response (200 OK):**
```json
{
  "attempt_id": "uuid",
  "is_correct": true,
  "points_earned": 10,
  "review_status": "graded",
  "explanation": "Correct! A distributed ledger is a shared database...",
  "correct_answer": "B"
}
```

**Behavior:**
- For `multiple-choice` and `true-false` questions, responses auto-grade immediately and set `review_status` to `graded`.
- For `short-answer` and `coding-task` questions, responses capture `review_status = "pending"` until an instructor manually grades the attempt.

---

### GET `/assessments/module/{module_id}/results`
Get user's assessment results for a module.

**Headers:** Requires authentication

**Response (200 OK):**
```json
{
  "module_id": 1,
  "total_questions": 10,
  "attempted": 10,
  "correct": 8,
  "score_percent": 80.0,
  "points_earned": 80,
  "points_possible": 100,
  "attempts": [
    {
      "assessment_id": "uuid",
      "question_text": "What is a distributed ledger?",
      "user_answer": "B",
      "is_correct": true,
      "points_earned": 10
    }
  ]
}
```

---

## Cohort Management Endpoints

### POST `/cohorts`
Create a new cohort (instructor/admin only).

**Headers:** Requires authentication + instructor/admin role

**Request:**
```json
{
  "name": "Spring 2025 Cohort",
  "description": "Beginner-friendly blockchain cohort",
  "start_date": "2025-03-10",
  "end_date": "2025-06-30"
}
```

**Response (201 Created):**
```json
{
  "id": "uuid",
  "name": "Spring 2025 Cohort",
  "description": "Beginner-friendly blockchain cohort",
  "start_date": "2025-03-10",
  "end_date": "2025-06-30",
  "is_active": true,
  "created_at": "2025-02-15T14:05:00Z"
}
```

---

### GET `/cohorts`
List cohorts with optional filters.

**Headers:** Requires authentication

**Query Parameters:**
- `active_only` (optional, boolean)
- `role` (optional, string) - filter by role-specific visibility

**Response (200 OK):**
```json
{
  "cohorts": [
    {
      "id": "uuid",
      "name": "Spring 2025 Cohort",
      "description": "Beginner-friendly blockchain cohort",
      "start_date": "2025-03-10",
      "end_date": "2025-06-30",
      "is_active": true
    }
  ]
}
```

---

### GET `/cohorts/{id}`
Get cohort details, including members.

**Headers:** Requires authentication + cohort membership or instructor/admin role

**Response (200 OK):**
```json
{
  "id": "uuid",
  "name": "Spring 2025 Cohort",
  "description": "Beginner-friendly blockchain cohort",
  "start_date": "2025-03-10",
  "end_date": "2025-06-30",
  "is_active": true,
  "members": [
    {"user_id": "student-uuid", "role": "student"},
    {"user_id": "instructor-uuid", "role": "instructor"}
  ]
}
```

---

### POST `/cohorts/{id}/members`
Enroll a member in a cohort (instructor/admin only).

**Headers:** Requires authentication + instructor/admin role

**Request:**
```json
{
  "user_id": "student-uuid",
  "role": "student"
}
```

**Response (201 Created):**
```json
{
  "id": "uuid",
  "cohort_id": "cohort-uuid",
  "user_id": "student-uuid",
  "role": "student",
  "joined_at": "2025-02-15T14:20:00Z"
}
```

---

### DELETE `/cohorts/{id}/members/{user_id}`
Remove a member from a cohort (instructor/admin only).

**Headers:** Requires authentication + instructor/admin role

**Response (204 No Content):** Empty body

---

### POST `/cohorts/{id}/deadlines`
Create a cohort deadline (instructor/admin only).

**Headers:** Requires authentication + instructor/admin role

**Request:**
```json
{
  "module_id": 4,
  "deadline_date": "2025-04-01",
  "is_mandatory": true,
  "description": "Complete Module 4 assessments"
}
```

**Response (201 Created):**
```json
{
  "id": "uuid",
  "cohort_id": "cohort-uuid",
  "module_id": 4,
  "deadline_date": "2025-04-01",
  "is_mandatory": true,
  "description": "Complete Module 4 assessments",
  "created_by": "instructor-uuid",
  "created_at": "2025-02-15T14:25:00Z"
}
```

---

### GET `/cohorts/{id}/deadlines`
List deadlines for a cohort.

**Headers:** Requires authentication + cohort membership or instructor/admin role

**Response (200 OK):**
```json
{
  "deadlines": [
    {
      "id": "uuid",
      "module_id": 4,
      "deadline_date": "2025-04-01",
      "is_mandatory": true,
      "description": "Complete Module 4 assessments"
    }
  ]
}
```

---

## Announcement Endpoints

### POST `/announcements`
Create an announcement (instructor/admin only).

**Headers:** Requires authentication + instructor/admin role

**Request:**
```json
{
  "cohort_id": null,
  "title": "Platform Maintenance",
  "content": "We will deploy updates this weekend.",
  "priority": "high",
  "is_pinned": true
}
```

**Response (201 Created):**
```json
{
  "id": "uuid",
  "cohort_id": null,
  "title": "Platform Maintenance",
  "content": "We will deploy updates this weekend.",
  "priority": "high",
  "is_pinned": true,
  "author_id": "instructor-uuid",
  "created_at": "2025-02-15T14:30:00Z",
  "updated_at": "2025-02-15T14:30:00Z"
}
```

---

### GET `/announcements`
List announcements with optional filters.

**Headers:** Requires authentication

**Query Parameters:**
- `cohort_id` (optional, UUID)
- `user_id` (optional, UUID) - filter announcements relevant to a user

**Response (200 OK):**
```json
{
  "announcements": [
    {
      "id": "uuid",
      "cohort_id": null,
      "title": "Platform Maintenance",
      "priority": "high",
      "is_pinned": true,
      "created_at": "2025-02-15T14:30:00Z"
    }
  ]
}
```

---

### PATCH `/announcements/{id}`
Update an announcement (author or admin only).

**Headers:** Requires authentication + author/admin role

**Request:**
```json
{
  "title": "Platform Maintenance - Schedule Update",
  "content": "Maintenance will occur Sunday evening.",
  "priority": "urgent",
  "is_pinned": true
}
```

**Response (200 OK):**
```json
{
  "id": "uuid",
  "title": "Platform Maintenance - Schedule Update",
  "content": "Maintenance will occur Sunday evening.",
  "priority": "urgent",
  "is_pinned": true,
  "updated_at": "2025-02-16T09:00:00Z"
}
```

---

### DELETE `/announcements/{id}`
Delete an announcement (author or admin only).

**Headers:** Requires authentication + author/admin role

**Response (204 No Content):** Empty body

---

## Analytics Endpoints

### GET `/analytics/cohort/{id}`
Get analytics for a cohort (instructor/admin only).

**Headers:** Requires authentication + instructor/admin role

**Response (200 OK):**
```json
{
  "total_students": 42,
  "active_students_7d": 30,
  "modules_completed_total": 210,
  "avg_completion_rate": 68.5,
  "avg_assessment_scores": 82.3,
  "popular_modules": [
    {"module_id": 2, "title": "Blockchain Basics", "completions": 40}
  ]
}
```

---

### GET `/analytics/student/{id}`
Get analytics for a student (self, instructor, or admin).

**Headers:** Requires authentication + appropriate access (student for self, instructor/admin for others)

**Response (200 OK):**
```json
{
  "overall_progress": 0.55,
  "modules_completed": 7,
  "avg_score": 88.5,
  "time_spent_minutes": 420,
  "engagement_metrics": {
    "forum_posts": 12,
    "ai_assistant_uses": 5
  }
}
```

---

### GET `/analytics/module/{id}`
Get analytics for a module (instructor/admin only).

**Headers:** Requires authentication + instructor/admin role

**Response (200 OK):**
```json
{
  "module_id": 3,
  "total_completions": 55,
  "avg_score": 81.2,
  "pass_rate": 0.78,
  "avg_time_minutes": 95,
  "common_wrong_answers": [
    {
      "assessment_id": "uuid",
      "question_text": "Explain proof-of-stake consensus.",
      "wrong_answer": "It uses mining rigs."
    }
  ]
}
```

---

## Grading Endpoints

### GET `/grading/queue`
Get pending grading queue (instructor/admin only).

**Headers:** Requires authentication + instructor/admin role

**Query Parameters:**
- `module_id` (optional, integer)
- `limit` (optional, integer, default 20)
- `offset` (optional, integer)

**Response (200 OK):**
```json
{
  "pending_attempts": [
    {
      "attempt_id": "uuid",
      "assessment_id": "assessment-uuid",
      "module_id": 3,
      "module_title": "Smart Contracts",
      "question_type": "short-answer",
      "student": {"id": "student-uuid", "full_name": "Casey Learner"},
      "attempted_at": "2025-02-15T13:45:00Z"
    }
  ]
}
```

---

### POST `/grading/{attempt_id}`
Grade a submission (instructor/admin only).

**Headers:** Requires authentication + instructor/admin role

**Request:**
```json
{
  "is_correct": true,
  "points_earned": 8,
  "feedback": "Strong explanation. Mention consensus finality.",
  "partial_credit": true
}
```

**Response (200 OK):**
```json
{
  "attempt_id": "uuid",
  "review_status": "graded",
  "graded_by": "instructor-uuid",
  "graded_at": "2025-02-15T14:45:00Z",
  "feedback": "Strong explanation. Mention consensus finality.",
  "points_earned": 8,
  "partial_credit": true
}
```

---

### GET `/grading/history`
Get grading history (instructor/admin only).

**Headers:** Requires authentication + instructor/admin role

**Query Parameters:**
- `user_id` (optional, UUID)
- `module_id` (optional, integer)
- `date_range` (optional, ISO 8601 range)

**Response (200 OK):**
```json
{
  "graded_attempts": [
    {
      "attempt_id": "uuid",
      "user_id": "student-uuid",
      "module_id": 3,
      "assessment_id": "assessment-uuid",
      "question_type": "short-answer",
      "graded_by": "instructor-uuid",
      "graded_at": "2025-02-14T11:05:00Z",
      "points_earned": 9,
      "feedback": "Excellent work!"
    }
  ]
}
```

---

## Notification Endpoints

### GET `/notifications`
List notifications for the authenticated user.

**Headers:** Requires authentication

**Query Parameters:**
- `is_read` (optional, boolean)
- `limit` (optional, integer, default 20)
- `offset` (optional, integer)

**Response (200 OK):**
```json
{
  "notifications": [
    {
      "id": "uuid",
      "title": "Assessment graded",
      "message": "Your Module 3 essay has been graded.",
      "type": "assessment_graded",
      "is_read": false,
      "created_at": "2025-02-15T15:00:00Z"
    }
  ]
}
```

---

### PATCH `/notifications/{id}/read`
Mark a notification as read.

**Headers:** Requires authentication (owner only)

**Response (200 OK):**
```json
{
  "id": "uuid",
  "is_read": true,
  "read_at": "2025-02-15T15:05:00Z"
}
```

---

### DELETE `/notifications/{id}`
Delete a notification.

**Headers:** Requires authentication (owner only)

**Response (204 No Content):** Empty body

---

**Note:** Module 17 (AI Trading Bot) is curriculum content only. Students learn concepts in the platform, then build their bots externally using Cursor/VS Code and the provided code examples in `curriculum/code-examples/module-17/`.

---

## Admin Endpoints

### GET `/admin/users`
Get all users (admin only).

**Headers:** Requires authentication + admin role

**Response (200 OK):**
```json
{
  "users": [
    {
      "id": "uuid",
      "email": "student@example.com",
      "username": "student123",
      "role": "student",
      "is_active": true,
      "created_at": "2025-11-01T10:00:00Z"
    }
  ],
  "total": 1
}
```

---

### GET `/admin/analytics`
Get platform analytics (admin/instructor only).

**Headers:** Requires authentication + admin/instructor role

**Response (200 OK):**
```json
{
  "total_students": 150,
  "active_students_7d": 42,
  "modules_completed_total": 890,
  "avg_completion_rate": 62.5,
  "popular_modules": [
    {"module_id": 1, "title": "Blockchain Technology", "completions": 145},
    {"module_id": 17, "title": "AI Agent Development", "completions": 12}
  ]
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Validation error",
  "errors": [
    {"field": "email", "message": "Invalid email format"}
  ]
}
```

### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

### 403 Forbidden
```json
{
  "detail": "Insufficient permissions"
}
```

### 404 Not Found
```json
{
  "detail": "Module not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error",
  "error_id": "uuid"
}
```

---

## Forum Endpoints

### GET `/forums/modules/{module_id}/posts`
Get forum posts for a module.

**Query Parameters:**
- `sort` (optional) - 'recent', 'popular', 'unsolved'
- `limit` (optional) - Default 20
- `offset` (optional) - For pagination

**Response (200 OK):**
```json
{
  "posts": [
    {
      "id": "uuid",
      "title": "Question about smart contract gas fees",
      "content": "I don't understand why...",
      "author": {
        "username": "student123",
        "role": "student"
      },
      "upvotes": 5,
      "reply_count": 3,
      "is_solved": false,
      "is_pinned": false,
      "created_at": "2025-11-01T10:00:00Z"
    }
  ],
  "total": 45
}
```

---

### POST `/forums/posts`
Create a new forum post.

**Headers:** Requires authentication

**Request:**
```json
{
  "module_id": 1,
  "title": "Question about consensus mechanisms",
  "content": "Can someone explain the difference between..."
}
```

**Response (201 Created):**
```json
{
  "id": "uuid",
  "module_id": 1,
  "title": "Question about consensus mechanisms",
  "created_at": "2025-11-01T12:00:00Z"
}
```

---

### POST `/forums/posts/{post_id}/replies`
Reply to a forum post.

**Headers:** Requires authentication

**Request:**
```json
{
  "content": "Great question! PoW uses computational work..."
}
```

**Response (201 Created):**
```json
{
  "id": "uuid",
  "parent_post_id": "parent-uuid",
  "content": "Great question! PoW uses...",
  "created_at": "2025-11-01T12:05:00Z"
}
```

---

### POST `/forums/posts/{post_id}/vote`
Upvote or downvote a post.

**Headers:** Requires authentication

**Request:**
```json
{
  "vote_type": "upvote"
}
```

**Response (200 OK):**
```json
{
  "post_id": "uuid",
  "upvotes": 6,
  "your_vote": "upvote"
}
```

---

## Chat Assistant Endpoint

### POST `/chat/ask`
Get help from AI learning assistant.

**Headers:** Requires authentication

**Request:**
```json
{
  "message": "I don't understand gas fees",
  "context": {
    "current_module": 3,
    "current_lesson": "uuid"
  }
}
```

**Response (200 OK):**
```json
{
  "response": "Gas fees are like postage stamps for transactions...",
  "suggested_lessons": [
    {
      "module_id": 3,
      "lesson_id": "uuid",
      "title": "Understanding Gas Fees"
    }
  ],
  "escalate_to_instructor": false
}
```

---

## Rate Limiting

- **Unauthenticated endpoints:** 100 requests/hour per IP
- **Authenticated endpoints:** 1000 requests/hour per user
- **AI chat endpoint:** 50 requests/hour per user (LLM API costs)

---

## Versioning

- Current version: `v1`
- All endpoints prefixed with `/api/v1`
- Breaking changes will result in new version (`v2`)
- Old versions supported for 6 months after deprecation

---

**Last Updated:** 2025-02-15
