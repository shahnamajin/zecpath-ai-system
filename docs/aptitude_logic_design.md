# Day 38 – Aptitude Logic Design

## Objective

Add cognitive and situational evaluation into the ZECPath AI HR Interview System using transparent reasoning and situational-judgment scoring.

## Reasoning Question Types

- Sequence and dependency reasoning
- Prioritization
- Problem-solving investigation

## Situational Judgment Framework

Scenarios evaluate observable response structure across:

- Problem identification
- Reasoning
- Decision quality
- Communication clarity
- Actionability

## Logical Reasoning Scoring Model

The reasoning baseline uses five components:

| Component | Weight |
|---|---:|
| Problem Identification | 20% |
| Reasoning | 30% |
| Decision Quality | 25% |
| Clarity | 15% |
| Actionability | 10% |

Formula:

```text
Logical Reasoning Score =
Problem Identification × 0.20
+ Reasoning × 0.30
+ Decision Quality × 0.25
+ Clarity × 0.15
+ Actionability × 0.10
```

## Scenario Evaluation

The situational evaluator checks for observable evidence such as:

- Identifying the problem
- Considering evidence and trade-offs
- Prioritizing impact
- Explaining a decision
- Communicating with stakeholders
- Defining actionable next steps
- Verifying the outcome

## Ideal Answer Structures

Reasoning answers are mapped to expected structures such as:

```text
Problem → Evidence → Analysis → Decision → Action → Verification
```

Scenario answers can use:

```text
Understand → Assess → Compare → Decide → Communicate → Follow Up
```

The framework evaluates structure rather than claiming to measure general intelligence.

## Overall Aptitude Score

The demo combines evaluated reasoning and scenario scores using a simple average:

```text
Overall Aptitude Score =
Average(all evaluated reasoning and scenario scores)
```

## Files

```text
data/aptitude_logic/
├── reasoning_questions.json
└── situational_scenarios.json

interview_ai/
├── logical_reasoning_scorer.py
├── scenario_evaluator.py
├── aptitude_logic_engine.py
└── demo_aptitude_logic.py

tests/
└── test_aptitude_logic.py

docs/
└── aptitude_logic_design.md
```

## Important Limitation

This is a transparent baseline scoring framework. It evaluates observable answer structure and reasoning signals supplied to the engine. It should not be interpreted as a validated measure of general intelligence, personality, or cognitive ability.
