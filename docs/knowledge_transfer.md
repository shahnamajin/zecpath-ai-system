# Zecpath AI ATS – Knowledge Transfer

## Purpose

This document provides an overview of the ATS system for developers who need to maintain or extend the project.

## Core Modules

### Parsers

Responsible for extracting candidate information from resumes.

### ATS Scoring Engine

Calculates the final candidate score.

### Semantic Matcher

Evaluates semantic similarity between candidate information and job requirements.

### Fairness Engine

Detects potential bias indicators and supports fairer evaluation.

### Normalization Engine

Normalizes resume and scoring information.

### Ranking Engine

Ranks candidates based on ATS scores.

### Shortlisting Engine

Classifies candidates into:

- Shortlist
- Review
- Reject

### API

Provides backend integration through REST endpoints.

## Testing

The system includes tests for:

- ATS scoring
- Candidate ranking
- Fairness
- ATS accuracy
- Performance
- Noisy resumes
- Stability

## Extension

When adding a new module:

1. Create the module.
2. Integrate it into the appropriate pipeline.
3. Add tests.
4. Run the tests.
5. Update documentation.