# Day 40 – HR Interview Simulation

## Objective

Test the HR interview system end-to-end using multiple simulated interview sessions and compare AI-generated scores and decisions with manually defined evaluation results.

## Candidate Types

The simulation includes:

- Confident
- Hesitant
- Inexperienced
- Overqualified

Two sessions are included for each candidate type.

## Evaluation Flow

```text
Simulated Interview Session
        ↓
AI HR Score + Component Signals
        ↓
AI Decision
        ↓
Manual Evaluation
        ↓
Score Difference + Decision Agreement
        ↓
Accuracy Evaluation
        ↓
Scoring Inconsistency Analysis
        ↓
Improvement Recommendations
```

## Decision Thresholds

| AI Score | Decision |
|---|---|
| 80–100 | Continue |
| 60–79.99 | Clarify |
| Below 60 | Review |

These thresholds are configuration values for the simulation and are not presented as validated hiring thresholds.

## Accuracy Metrics

The simulation reports:

- Number of sessions tested
- Decision accuracy
- Percentage of scores within ±5 points of manual evaluation
- Mean absolute score difference
- Number of decision disagreements

## Manual Comparison

Each session contains a manually defined reference score and decision. These references are used only to test the simulation pipeline and should be replaced by independently reviewed human evaluations for production validation.

## Scoring Inconsistency Detection

The engine flags:

1. AI/manual decision disagreement.
2. Score differences exceeding the configured ±5-point tolerance.

## Improvement Recommendations

Recommendations are generated from observed mismatches. Candidate-type-specific review is included for hesitant and overqualified scenarios, while broader calibration is suggested when score differences exceed tolerance.

## Files

```text
data/hr_simulation/
├── simulation_sessions.json
├── evaluation_config.json
└── hr_interview_test_report.json

interview_ai/
├── hr_interview_simulator.py
└── demo_hr_interview_simulation.py

tests/
└── test_hr_interview_simulation.py

docs/
└── hr_interview_simulation.md
```

## Important Limitation

This is a simulation and validation framework. The manual scores included in the sample dataset are test reference values, not independent empirical ground truth. Production accuracy should be established using a larger set of independently reviewed interviews and a documented human-evaluation protocol.
