# Day 28 – AI Screening Report Generator

## Objective

Transform structured AI screening evaluations into recruiter-friendly and explainable reports.

## Inputs

- Answer Understanding output
- Screening Scoring output
- Confidence and Sentiment output
- Candidate metadata
- Job metadata

## Report Sections

- Candidate information
- Final screening score
- Key answers
- Confirmed skills
- Salary expectation
- Availability
- Strengths
- Risks
- Missing data
- Behavioral signals
- Recruiter summary

## Export Formats

The report formatter supports:

1. JSON
2. Plain text

JSON is suitable for API responses and database storage.

Plain text can be used for recruiter-facing previews and logs.

## Explainability

The report preserves question IDs and extracted answers.

The system does not invent missing candidate information. Missing information is explicitly listed so that recruiters can follow up.