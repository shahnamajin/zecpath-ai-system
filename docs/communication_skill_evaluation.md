# Day 35 – Communication Skill Evaluation

## Objective

Evaluate candidate communication skills objectively using transparent, normalized signals.

## Metrics

1. Fluency – sentence continuity and manageable sentence length.
2. Grammar Quality – conservative detection of sentence-level grammar issues.
3. Vocabulary Range – unique-word ratio with length-aware handling.
4. Clarity – sentence length and filler-aware clarity signal.
5. Answer Structure – sentence count and organization markers.
6. Filler Control – filler frequency normalized per 100 words.

## Filler Detection

The model detects common filler expressions such as:

- um
- uh
- erm
- hmm
- like
- basically
- actually
- you know
- sort of
- kind of

## Scoring Formula

Communication Score =

`Fluency × 0.20`
`+ Grammar Quality × 0.20`
`+ Vocabulary Range × 0.15`
`+ Clarity × 0.20`
`+ Answer Structure × 0.15`
`+ Filler Control × 0.10`

The component weights sum to 1.00.

## Normalization

To reduce bias from answer length and filler frequency:

- Scores are clamped to 0–100.
- Filler frequency is measured per 100 words.
- Very short responses receive an evidence factor because they provide less observable communication evidence.
- Component scores use bounded ranges.
- The model does not use candidate identity, education, location, gender, accent, or other demographic attributes.

Evidence factors:

| Word Count | Factor |
|---|---:|
| 0–4 | 0.70 |
| 5–7 | 0.85 |
| 8+ | 1.00 |

Final score = weighted component score × evidence factor.

## Interpretation Bands

| Score | Band |
|---|---|
| 80–100 | Strong |
| 65–79.99 | Good |
| 50–64.99 | Moderate |
| 0–49.99 | Needs Improvement |

These bands are descriptive categories for the model output, not a claim about a candidate's overall suitability.

## Sample Outputs

The demo produces component-level scores, filler counts, normalized filler rates, evidence factors, and the final communication score.

## Project Files

- `data/communication_evaluation/scoring_parameters.json`
- `data/communication_evaluation/communication_test_cases.json`
- `interview_ai/communication_analyzer.py`
- `interview_ai/communication_scorer.py`
- `interview_ai/demo_communication_scoring.py`
- `tests/test_communication_evaluation.py`
- `docs/communication_skill_evaluation.md`

## Testing

The Day 35 test suite covers metric ranges, filler detection, normalization, scoring behavior, evidence adjustment, and weight validation.

## Limitations

This is a transparent heuristic baseline. Grammar and fluency are approximated from transcript text and should not be treated as a complete linguistic assessment. For production use, the model can later be extended with stronger NLP/LLM-based linguistic analysis while retaining the same normalized scoring interface.
