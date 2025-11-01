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
  "explanation": "Correct! A distributed ledger is a shared database...",
  "correct_answer": "B"
}
```

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

## AI Trading Bot Endpoints

### GET `/bot/configurations`
Get user's trading bot configurations.

**Headers:** Requires authentication

**Response (200 OK):**
```json
{
  "configurations": [
    {
      "id": "uuid",
      "name": "My First Bot",
      "llm_provider": "anthropic",
      "llm_model": "claude-3-5-sonnet-20241022",
      "is_active": false,
      "is_paper_trading": true,
      "created_at": "2025-11-01T10:00:00Z"
    }
  ]
}
```

---

### POST `/bot/configurations`
Create a new bot configuration.

**Headers:** Requires authentication

**Request:**
```json
{
  "name": "My Trading Bot",
  "llm_provider": "anthropic",
  "llm_model": "claude-3-5-sonnet-20241022",
  "is_paper_trading": true,
  "max_position_size_percent": 10.0,
  "stop_loss_percent": 5.0,
  "config_json": {
    "weights": {
      "technical": 0.35,
      "sentiment": 0.20,
      "onchain": 0.25
    },
    "data_sources": ["binance", "coingecko", "twitter"]
  }
}
```

**Response (201 Created):**
```json
{
  "id": "uuid",
  "name": "My Trading Bot",
  "llm_provider": "anthropic",
  "is_active": false,
  "created_at": "2025-11-01T12:30:00Z"
}
```

---

### POST `/bot/configurations/{config_id}/backtest`
Run backtest on historical data.

**Headers:** Requires authentication

**Request:**
```json
{
  "symbol": "bitcoin",
  "start_date": "2024-01-01",
  "end_date": "2024-12-31",
  "initial_capital": 10000
}
```

**Response (200 OK):**
```json
{
  "backtest_id": "uuid",
  "results": {
    "total_return_percent": 25.5,
    "sharpe_ratio": 1.8,
    "max_drawdown_percent": -12.3,
    "win_rate": 0.65,
    "total_trades": 42,
    "profitable_trades": 27,
    "final_capital": 12550.00
  },
  "completed_at": "2025-11-01T12:35:00Z"
}
```

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
Get platform analytics (admin/teacher only).

**Headers:** Requires authentication + admin/teacher role

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

## Rate Limiting

- **Unauthenticated endpoints:** 100 requests/hour per IP
- **Authenticated endpoints:** 1000 requests/hour per user
- **Bot backtest endpoints:** 10 requests/hour per user (computationally expensive)

---

## Versioning

- Current version: `v1`
- All endpoints prefixed with `/api/v1`
- Breaking changes will result in new version (`v2`)
- Old versions supported for 6 months after deprecation

---

**Last Updated:** 2025-11-01

