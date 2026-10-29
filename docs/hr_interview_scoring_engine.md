# Day 37 – HR Interview Scoring Engine

## Objective
Combine HR interview responses and communication/behavioral signals into a structured, explainable HR interview score.

## Parameters
| Parameter | Weight |
|---|---:|
| Answer Relevance | 35% |
| Communication | 25% |
| Confidence | 20% |
| Consistency | 20% |

## Formula
`HR Interview Score = Relevance × 0.35 + Communication × 0.25 + Confidence × 0.20 + Consistency × 0.20`

All components use a 0–100 scale.

## Interview-Length Normalization
The engine averages each component across all evaluated responses before applying the weights. Therefore, adding more questions does not automatically increase a candidate's score.

## Explainable Breakdown
Every result contains each component's score, configured weight, weighted contribution, final score, and descriptive band.

## Score Bands
80–100: Strong  
60–79.99: Moderate  
40–59.99: Developing  
0–39.99: Needs Improvement

## Candidate Report Format
Candidate information → interview summary → final score → component scores → explainable breakdown.

## Integration
The engine is designed to consume upstream HR response analysis, communication evaluation, confidence/behavioral signals, and consistency/contradiction analysis.

## Files
- `data/hr_interview_scoring/scoring_weights.json`
- `data/hr_interview_scoring/sample_hr_interview.json`
- `interview_ai/hr_interview_scoring_engine.py`
- `interview_ai/hr_score_report.py`
- `interview_ai/demo_hr_interview_scoring.py`
- `tests/test_hr_interview_scoring.py`

## Limitation
This module is an aggregation layer; final score quality depends on the validity of upstream component scores.
