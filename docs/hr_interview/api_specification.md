# ZECPath AI — HR Interview API Specification

**Status: Proposed integration contract — not currently implemented as an HTTP route.**

## 1. Current API status

The FastAPI application is defined in `api/main.py`. It currently registers routers for:

- `api.routes.resume`
- `api.routes.scoring`
- `api.routes.shortlisting`
- `api.routes.jobs`

The inspected route scan found no HR interview router. The existing HR scoring implementation is a Python class in `interview_ai/hr_interview_scoring_engine.py`.

Do not describe the proposed endpoints below as live endpoints until they are implemented, registered, and tested.

## 2. Proposed endpoint

### `POST /api/hr-interviews/score`

**Purpose:** Accept pre-evaluated response component scores and return an aggregated HR interview score and explainable report.

**Request body (illustrative):**

```json
{
  "candidate_id": "CAND_1001",
  "job_id": "JOB_2001",
  "session_id": "SESSION_3001",
  "job_title": "Python Developer",
  "responses": [
    {
      "answer_relevance": 90,
      "communication": 85,
      "confidence": 80,
      "consistency": 92
    },
    {
      "answer_relevance": 88,
      "communication": 87,
      "confidence": 82,
      "consistency": 90
    }
  ]
}
```

The sample identifiers and scores are illustrative only.

### Successful response (illustrative)

```json
{
  "success": true,
  "candidate": {
    "candidate_id": "CAND_1001",
    "job_id": "JOB_2001",
    "session_id": "SESSION_3001",
    "job_title": "Python Developer"
  },
  "interview_summary": {
    "responses_evaluated": 2,
    "normalization_method": "response_average"
  },
  "score": {
    "final": 86.0,
    "band": "strong"
  },
  "component_scores": {
    "answer_relevance": 89.0,
    "communication": 86.0,
    "confidence": 81.0,
    "consistency": 91.0
  },
  "explainable_breakdown": {
    "answer_relevance": {
      "score": 89.0,
      "weight": 0.35,
      "weighted_score": 31.15
    }
  }
}
```

This is a shape example, not a guaranteed exact response. The complete breakdown should contain all four components. The illustrative final score must be recalculated from the active `scoring_weights.json` before using this sample as a test fixture.

## 3. Validation rules inherited from the engine

| Field | Rule |
|---|---|
| `candidate_id` | Required identifier |
| `job_id` | Required identifier |
| `session_id` | Required identifier |
| `job_title` | Required string |
| `responses` | Must contain at least one response |
| `answer_relevance` | Required numeric value, 0–100 |
| `communication` | Required numeric value, 0–100 |
| `confidence` | Required numeric value, 0–100 |
| `consistency` | Required numeric value, 0–100 |

The Python engine raises `ValueError` when responses are missing, a component is absent, a component is outside the permitted range, or configured weights do not sum to 1.0 within the engine's tolerance.

## 4. Suggested HTTP status mapping

These are proposed API conventions, not current HR route behavior.

| Status | Meaning |
|---:|---|
| `200` | Score successfully calculated |
| `400` | Invalid request or scoring validation error |
| `401` | Missing/invalid authentication, if authentication is added |
| `403` | Caller is not authorized to access the candidate/session |
| `404` | Candidate, job, or session not found, if persistence lookup is added |
| `422` | Request body fails FastAPI/Pydantic schema validation |
| `500` | Unexpected server-side failure |

Avoid returning stack traces or sensitive internal exception details to clients.

## 5. Proposed additional endpoints

These endpoints may be considered if the product requires a complete HR interview lifecycle. They are not confirmed as implemented.

| Method and path | Purpose |
|---|---|
| `POST /api/hr-interviews/sessions` | Create an interview session |
| `GET /api/hr-interviews/sessions/{session_id}` | Retrieve session status/details |
| `POST /api/hr-interviews/sessions/{session_id}/responses` | Submit a response |
| `POST /api/hr-interviews/sessions/{session_id}/complete` | Complete a session and trigger final evaluation |
| `GET /api/hr-interviews/sessions/{session_id}/report` | Retrieve the generated report |

Before implementation, define authentication, authorization, persistence, idempotency, request limits, audit logging, and consent handling.

## 6. Integration outline

A future router could:

1. Define Pydantic request/response schemas in `api/schemas.py` or a dedicated HR schema module.
2. Instantiate `HRInterviewScoringEngine`.
3. Call `score_interview(candidate_id, job_id, session_id, job_title, responses)`.
4. Convert the result with `HRScoreReport.to_dict()`.
5. Return the structured result.
6. Map validation errors to safe HTTP errors.
7. Register the router in `api/main.py`.

## 7. API documentation access

FastAPI normally provides interactive OpenAPI documentation at `/docs` and schema output at `/openapi.json` when enabled by the application configuration. Confirm the running app and route registration before sharing these URLs with integrators.
