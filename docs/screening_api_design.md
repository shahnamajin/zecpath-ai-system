# ZecPath AI Screening API Design

## 1. Overview

The ZecPath AI Screening API provides backend interfaces for conducting AI-powered candidate screening.

The API connects candidate information, job information, screening questions, candidate responses, AI analysis, scoring, and final screening results.

---

## 2. Screening Flow

Candidate
↓
Screening Session
↓
Question Selection
↓
Candidate Response
↓
Edge Case Analysis
↓
Intent Detection
↓
Answer Understanding
↓
Confidence Analysis
↓
Sentiment Analysis
↓
Screening Scoring
↓
Decision
↓
Screening Report

---

## 3. Start Screening

### Endpoint

POST `/api/screening/start`

### Purpose

Creates a new screening session for a candidate.

### Request

```json
{
  "candidate_id": "CAND_1001",
  "job_id": "JOB_2001"
}