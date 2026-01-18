# API Documentation - Mental Health Risk Detection System

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication

All protected endpoints require a Bearer token in the Authorization header:

```
Authorization: Bearer <access_token>
```

---

## Endpoints

### Authentication Endpoints

#### Register User
```
POST /auth/register

Request Body:
{
  "email": "user@example.com",
  "username": "john_doe",
  "password": "secure_password",
  "full_name": "John Doe",
  "age": 30,
  "gender": "male"
}

Response (201):
{
  "id": "uuid",
  "email": "user@example.com",
  "username": "john_doe",
  "full_name": "John Doe",
  "age": 30,
  "gender": "male",
  "created_at": "2026-01-18T10:30:00Z"
}
```

#### Login
```
POST /auth/login

Request Body:
{
  "email": "user@example.com",
  "password": "secure_password"
}

Response (200):
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "username": "john_doe",
    ...
  }
}
```

#### Get Current User
```
GET /auth/me

Headers:
Authorization: Bearer <token>

Response (200):
{
  "id": "uuid",
  "email": "user@example.com",
  "username": "john_doe",
  "full_name": "John Doe",
  "age": 30,
  "gender": "male",
  "created_at": "2026-01-18T10:30:00Z"
}
```

---

### Assessment Endpoints

#### Get All Questionnaires
```
GET /assessment/questionnaires

Response (200):
[
  {
    "id": "q-uuid-1",
    "name": "PHQ-9 Depression Screening",
    "description": "Patient Health Questionnaire-9 for depression severity assessment",
    "version": "1.0",
    "questions": [
      {
        "id": "q1",
        "text": "Little interest or pleasure in doing things",
        "type": "rating",
        "scale": [0, 3, 6, 9],
        "labels": ["Not at all", "Several days", "More than half the days", "Nearly every day"]
      },
      ...
    ]
  },
  ...
]
```

#### Get Specific Questionnaire
```
GET /assessment/questionnaires/{questionnaire_id}

Response (200):
{
  "id": "q-uuid-1",
  "name": "PHQ-9 Depression Screening",
  "description": "...",
  "version": "1.0",
  "questions": [...]
}
```

#### Start Assessment
```
POST /assessment/start

Headers:
Authorization: Bearer <token>

Request Body:
{
  "questionnaire_id": "q-uuid-1"
}

Response (200):
{
  "id": "assessment-uuid",
  "user_id": "user-uuid",
  "questionnaire_id": "q-uuid-1",
  "responses": {},
  "status": "in_progress",
  "started_at": "2026-01-18T10:30:00Z",
  "completed_at": null
}
```

#### Submit Assessment
```
POST /assessment/submit

Headers:
Authorization: Bearer <token>

Request Body:
{
  "questionnaire_id": "q-uuid-1",
  "responses": {
    "q1": 3,
    "q2": 6,
    "q3": 0,
    "q4": 3,
    "q5": 6,
    "q6": 9,
    "q7": 3,
    "q8": 0,
    "q9": 6
  }
}

Response (200):
{
  "assessment_id": "assessment-uuid",
  "status": "completed",
  "risk_level": "high",
  "risk_score": 72.5
}
```

---

### Results Endpoints

#### Get Risk Score for Assessment
```
GET /results/assessment/{assessment_id}

Headers:
Authorization: Bearer <token>

Response (200):
{
  "id": "score-uuid",
  "assessment_id": "assessment-uuid",
  "user_id": "user-uuid",
  "risk_level": "high",
  "risk_score": 72.5,
  "contributing_factors": [
    "hopelessness",
    "concentration_issues",
    "sleep_disturbance"
  ],
  "recommendations": [
    "Schedule an appointment with a therapist or counselor",
    "Reach out to trusted friends or family members",
    "Consider professional mental health support",
    "Explore crisis support resources"
  ],
  "ml_model_used": "RandomForest + Feature Analysis",
  "confidence_score": 0.85,
  "calculated_at": "2026-01-18T10:35:00Z"
}
```

#### Get Latest Assessment
```
GET /results/user/latest

Headers:
Authorization: Bearer <token>

Response (200):
{
  "id": "score-uuid",
  "assessment_id": "assessment-uuid",
  "user_id": "user-uuid",
  "risk_level": "high",
  "risk_score": 72.5,
  ...
}
```

#### Get Assessment History
```
GET /results/user/history?limit=10

Headers:
Authorization: Bearer <token>

Response (200):
{
  "count": 3,
  "assessments": [
    {
      "id": "assessment-uuid-1",
      "questionnaire_id": "q-uuid-1",
      "responses": {...},
      "status": "completed",
      "completed_at": "2026-01-18T10:35:00Z"
    },
    ...
  ]
}
```

#### Get Personalized Resources
```
GET /results/resources/{risk_level}

Headers:
Authorization: Bearer <token>

Parameters:
- risk_level: "low" | "medium" | "high" | "critical"

Response (200):
{
  "risk_level": "high",
  "resources": [
    {
      "id": "kn_001",
      "title": "Finding a Therapist",
      "content": "Guide to finding mental health professionals...",
      "category": "therapy",
      "relevance_score": 0.92
    },
    {
      "id": "kn_003",
      "title": "Crisis Support Resources",
      "content": "In crisis situations, contact...",
      "category": "crisis",
      "relevance_score": 0.88
    },
    ...
  ]
}
```

---

### Admin Endpoints

#### Create Questionnaire
```
POST /admin/questionnaire/create

Headers:
Authorization: Bearer <admin_token>

Request Body:
{
  "name": "Custom Assessment",
  "description": "Custom mental health assessment",
  "questions": [
    {
      "id": "c1",
      "text": "How are you feeling today?",
      "type": "rating",
      "scale": [0, 1, 2, 3, 4, 5],
      "labels": [...]
    }
  ]
}

Response (201):
{
  "id": "q-uuid-new",
  "name": "Custom Assessment",
  "description": "...",
  "version": "1.0",
  "questions": [...]
}
```

#### Get Audit Logs
```
GET /admin/audit-logs?limit=50

Headers:
Authorization: Bearer <admin_token>

Response (200):
{
  "count": 50,
  "logs": [
    {
      "id": "log-uuid",
      "user_id": "user-uuid",
      "action": "assessment_submitted",
      "resource": "Assessment",
      "details": {...},
      "timestamp": "2026-01-18T10:35:00Z",
      "ip_address": "192.168.1.1"
    },
    ...
  ]
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request parameters"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Not authorized"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Rate Limiting

All endpoints are rate-limited to **100 requests per minute** per IP address.

Response headers include:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
X-RateLimit-Reset: 1642491000
```

---

## Pagination

For list endpoints, use query parameters:

```
?limit=20&offset=0
```

---

## Response Format

All responses are in JSON format with the following structure:

**Success (2xx)**:
```json
{
  "data": {...},
  "status": "success"
}
```

**Error (4xx, 5xx)**:
```json
{
  "detail": "Error message",
  "status": "error"
}
```

---

## Examples

### Complete Assessment Flow

```bash
# 1. Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "john_doe",
    "password": "password123",
    "full_name": "John Doe",
    "age": 30,
    "gender": "male"
  }'

# 2. Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'

# 3. Get questionnaires
curl -X GET http://localhost:8000/api/v1/assessment/questionnaires

# 4. Submit assessment
curl -X POST http://localhost:8000/api/v1/assessment/submit \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "questionnaire_id": "q-uuid-1",
    "responses": {"q1": 3, "q2": 6, ...}
  }'

# 5. Get results
curl -X GET http://localhost:8000/api/v1/results/assessment/<assessment_id> \
  -H "Authorization: Bearer <token>"
```

---

**API Version**: 1.0.0
**Last Updated**: January 2026
