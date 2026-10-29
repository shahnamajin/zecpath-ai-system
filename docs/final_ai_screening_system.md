# ZecPath AI - Final AI Screening System

## 1. Overview

The ZecPath AI Screening System is an AI-powered candidate screening
pipeline designed to automate the initial hiring screening process.

The system processes candidate responses, analyzes their quality and
meaning, handles edge cases, calculates screening scores, and produces
a final screening result.

---

## 2. Complete Screening Pipeline

The complete screening process is:

Candidate
↓
HR Screening Questions
↓
Candidate Response
↓
Transcript Processing
↓
Answer Understanding
↓
Confidence Analysis
↓
Sentiment Analysis
↓
Screening Scoring
↓
Conversation Flow
↓
Edge Case Handling
↓
Screening Optimization
↓
AI Screening Report
↓
Final Screening Decision

---

## 3. Major System Components

### 3.1 HR Screening Dataset

The system contains a structured question dataset for HR screening.

Question categories include:

- Introduction
- Education
- Experience
- Skills
- Location
- Salary
- Notice Period

The question selection system selects questions according to the
candidate's job role.

---

### 3.2 Transcript Architecture

The transcript system stores candidate screening interactions.

Each transcript contains information such as:

- Transcript ID
- Candidate ID
- Job ID
- Session ID
- Question
- Candidate response
- Interaction metadata

---

### 3.3 Speech-to-Text and Cleaning

The speech processing component converts spoken responses into text.

The transcript cleaning system handles:

- Filler words
- Extra whitespace
- Punctuation
- Interrupted speech
- Partial answers
- Silence

The current implementation uses simulated/local test data for screening
demonstration.

---

### 3.4 Answer Understanding

The answer understanding engine determines the intent of a candidate's
response.

Supported intents include:

- Introduction
- Education
- Experience
- Skills
- Availability
- Salary expectation
- Location
- Off-topic
- Vague
- Missing

The system also extracts useful information from candidate responses.

---

### 3.5 Screening Scoring

The screening scoring engine evaluates candidate responses using:

- Clarity
- Relevance
- Completeness
- Consistency

The weighted scoring model is:

Question Score =
Clarity × 0.25 +
Relevance × 0.30 +
Completeness × 0.25 +
Consistency × 0.20

The final screening score is calculated from the evaluated responses.

---

### 3.6 Confidence and Sentiment Analysis

The system analyzes behavioral signals from candidate responses.

Signals include:

- Hesitation
- Response length
- Response pace
- Positive sentiment
- Negative sentiment
- Uncertainty
- Contradiction
- Communication strength

These signals provide additional information about the candidate's
communication during screening.

---

### 3.7 AI Screening Report

The screening report generator converts AI analysis into a
recruiter-friendly report.

The report can contain:

- Candidate information
- Job information
- Final screening score
- Confirmed skills
- Strengths
- Risks
- Missing information
- Availability
- Salary expectations
- Screening decision

---

### 3.8 Conversation Flow

The conversation flow controls the state of the AI screening session.

The system supports states such as:

- START
- ASKING
- WAITING_FOR_RESPONSE
- PROCESSING_RESPONSE
- CLARIFICATION
- RETRY
- FALLBACK
- NEXT_QUESTION
- COMPLETED
- FAILED

This allows the screening process to respond dynamically to candidate
answers.

---

### 3.9 Screening Optimization

The screening optimization system tests the screening decisions and
helps reduce unnecessary rejection.

Current decision thresholds are:

- 70-100 → Continue
- 45-69 → Clarify
- 20-44 → Retry
- Below 20 → Clarification before rejection

Special conditions such as missing, vague, and off-topic responses are
handled before final rejection.

---

### 3.10 Edge Case and Failure Handling

The system handles abnormal screening situations such as:

- Poor audio
- Background noise
- Language mixing
- Missing answers
- Very short responses
- Repeated failures

Possible actions include:

- Continue
- Clarify
- Retry
- Safe fallback

The system also limits repeated retries and clarifications.

---

## 4. End-to-End Screening Process

The final screening demo performs the following sequence:

1. Initialize candidate and job information.
2. Initialize screening components.
3. Ask the screening question.
4. Receive the candidate response.
5. Check for edge cases.
6. Detect response intent.
7. Analyze confidence.
8. Analyze sentiment.
9. Calculate screening score.
10. Make a screening decision.
11. Continue to the next question.
12. Generate the final screening result.

---

## 5. Final Demo

The final end-to-end demo was executed using:

Candidate ID:

CAND_1001

Job ID:

JOB_2001

Session ID:

SESSION_3001

Job Title:

Python Developer

The demo processed four screening questions.

---

## 6. Final Demo Result

Total Questions:

4

Continue:

4

Clarify:

0

Retry:

0

Final Score:

95.00 / 100

Status:

SCREENING COMPLETED

---

## 7. Detected Skills

The final screening demo detected:

- Flask
- Machine Learning
- Pandas
- Python
- SQL

---

## 8. Edge Case Handling

The edge-case testing demonstrated handling for:

- Normal responses
- Poor audio
- Background noise
- Language mixing
- Missing answers

The edge-case test suite completed successfully.

---

## 9. Testing

The screening system contains automated tests covering:

- HR screening questions
- Transcript architecture
- Speech-to-text cleaning
- Answer understanding
- Screening scoring
- Confidence and sentiment analysis
- Screening report generation
- Conversation flow
- Screening optimization
- Edge-case handling

---

## 10. Final System Status

The ZecPath AI Screening System has completed the local end-to-end
screening demonstration.

The final demo successfully processed candidate responses and generated
a completed screening result.

The system is structured so that the individual AI components can later
be integrated into production APIs and the complete ZecPath hiring
platform.