# Day 41 - Unified Scoring Engine

## Objective
Combine ATS, AI screening, and HR interview scores into a
single hiring-fit percentage.

## Inputs
- ATS score: 0-100
- Screening score: 0-100
- HR interview score: 0-100

## Default weights
- ATS: 40%
- Screening: 25%
- HR interview: 35%

## Role-based adjustments
- Default: 40%, 25%, 35%
- Technical: 45%, 30%, 25%
- Non-technical: 25%, 30%, 45%

All weight configurations must total 100%.

## Outputs
- Candidate and job identifiers
- Individual round scores
- Applied weights
- Weighted contributions
- Hiring-fit percentage
- Creation timestamp

## Limitation
The hiring-fit percentage is a configurable aggregate score,
not a guarantee of candidate suitability. Weights and decision
thresholds require validation against representative,
human-reviewed hiring data.