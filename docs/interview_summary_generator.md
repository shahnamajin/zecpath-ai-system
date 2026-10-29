# Day 39 – Interview Summary Generator

## Objective

Convert AI interview analysis into recruiter-ready structured insights and a natural-language HR interview summary.

## Summary Sections

- Candidate strengths
- Weaknesses / development areas
- Cultural-fit indicators
- Risk flags
- Response inconsistencies
- Overall HR performance
- Natural-language summary

## Input Signals

The generator accepts the supplied HR interview analysis:

- HR interview score
- Aptitude / logic score
- Communication score
- Confidence score
- Consistency score
- Individual responses
- Consistency/inconsistency information

## Insight Rules

### Strengths

Configured rules identify positive indicators when component scores meet the defined thresholds.

### Weaknesses

Lower component scores are surfaced as areas requiring further review.

### Cultural Fit Indicators

The system only reports observable references in responses, such as teamwork, coordination, communication, responsibility, or ownership. It does not infer culture fit from unsupported information.

### Risk Flags

Risk flags can be generated from low component scores or detected response inconsistencies.

### Inconsistency Highlighting

Responses explicitly marked as inconsistent are preserved with their question ID and supplied explanation.

## Natural-Language Report

The generator combines the structured insights into a concise recruiter-oriented narrative.

## Report Structure

```text
Candidate Information
        ↓
Overall Performance
        ↓
Strengths
        ↓
Weaknesses
        ↓
Cultural Fit Indicators
        ↓
Risk Flags
        ↓
Inconsistencies
        ↓
Natural-Language Summary
```

## Files

```text
data/interview_summary/
├── sample_interview_analysis.json
├── summary_template.json
└── sample_hr_summary_report.json

interview_ai/
├── interview_summary_generator.py
├── summary_report_formatter.py
└── demo_interview_summary.py

tests/
└── test_interview_summary.py

docs/
└── interview_summary_generator.md
```

## Important Limitation

This generator summarizes the supplied AI analysis. It does not independently verify candidate claims and should be reviewed together with the underlying interview responses and component scores.
