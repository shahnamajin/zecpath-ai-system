# Day 47 — Technical Skill Scoring Model

**Status:** Initial scoring engine and report format. The ratings supplied to the engine must come from a trained human evaluator or a separately validated technical answer evaluator.

## Scoring dimensions

All four dimensions use a 0–4 scale:
- 0: no evidence
- 1: weak
- 2: partial
- 3: good
- 4: excellent

The question-type weights are stored in `data/technical_interview/technical_scoring_rubrics.json`:
- Conceptual: accuracy 40%, depth 30%, reasoning 20%, applicability 10%.
- Experience-based: accuracy 25%, depth 25%, reasoning 20%, applicability 30%.
- Scenario-based: accuracy 25%, depth 15%, reasoning 35%, applicability 25%.
- Introduction: accuracy 35%, depth 15%, reasoning 20%, applicability 30%.

## Shallow / deep classification

The engine labels an answer:
- Shallow: depth below 2, or expected-evidence coverage below 40%.
- Deep: depth and reasoning are each at least 3, and evidence coverage is at least 70% (if coverage is supplied).
- Developing: between those conditions.

Evidence coverage must be supplied by the evaluator; the engine does not infer semantic correctness from answer length.

## Difficulty normalization

Each dimension is rated against the expectation for that question's difficulty. The weighted score is converted to 0–100. There is no blanket hard-question bonus or penalty. This keeps the comparison tied to difficulty-specific expectations rather than arbitrary difficulty multipliers.

## Integration boundary

`TechnicalScoringEngine.score_answer()` accepts a question record, four dimension ratings, optional evidence coverage and evidence notes. It returns a question-level explainable score. `build_skill_breakdown()` aggregates by skill domain. `build_report()` creates a JSON evaluation report with human review required.

## Limitations

This engine aggregates evaluator-provided ratings. It does not itself determine whether a raw answer is technically correct. A validated evaluator, subject-matter-reviewed rubrics, calibration across evaluators, and human oversight are required before production use.
