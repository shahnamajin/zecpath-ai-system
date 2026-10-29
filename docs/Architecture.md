# Zecpath AI ATS – System Architecture

## 1. System Overview

Zecpath AI is an AI-powered Applicant Tracking System that processes resumes, extracts candidate information, evaluates candidates against job requirements, calculates ATS scores, ranks candidates, and supports automated shortlisting.

## 2. ATS Processing Flow

Resume Upload
        ↓
Text Extraction
        ↓
Section Extraction
        ↓
Candidate Information Extraction
        ↓
Skill / Education / Experience / Project / Certification Extraction
        ↓
ATS Scoring
        ↓
Fairness & Normalization
        ↓
Candidate Ranking
        ↓
Shortlisting
        ↓
Recruiter Output

## 3. Main Components

### API

Provides backend access to ATS functionality using FastAPI.

### Parsers

Extract structured information from resumes.

### Engines

Perform scoring, semantic matching, fairness, ranking, and shortlisting.

### Utils

Provide reusable utilities such as logging, ID generation, and resume cleaning.

### Tests

Validate accuracy, performance, fairness, ranking, noisy resume handling, and system stability.

## 4. Final Output

The ATS produces:

- Candidate information
- ATS score
- Score breakdown
- Recommendation
- Candidate rank
- Shortlist / Review / Reject status