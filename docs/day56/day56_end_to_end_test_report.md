# ZECPath Day 56 - End-to-End Simulation Report

- Generated: 2026-11-04T07:31:29.046126+00:00
- Candidate: Arjun Menon (C001)
- Target role: Backend Python Developer

## Stage scores

| Stage | Score | Input provenance |
|---|---:|---|
| Ats | 46.00 | Existing parsed resume mapped to ATS input schema |
| Screening | 90.75 | Sample structured answer supplied to the existing rule-based screening engine |
| Hr Interview | 88.00 | Predefined HR simulation fixture SIM_001; not a real interview record for C001 |
| Technical Interview | 75.00 | Sample evaluator-provided ratings; not autonomous raw-answer evaluation |
| Machine Test | 75.00 | Sample evaluator-provided ratings calculated using the design-only machine-test rubric; no coding task executed |

## Unified scoring

- Role configuration: technical
- Hiring Fit Score: 73.51
- Evaluation status: completed

## Final recommendation

- Recommendation: Hold / Review
- Human review required: True

## HR simulation comparison

- Sessions: 8
- Decision agreement: 50.0%
- Mean absolute score difference: 4.88

These are comparisons against predefined stored manual judgments, not independent real-world validation.

## Incomplete evaluation check

- Test passed: True
- Missing stages: machine_test
- Recommendation: Hold / Review

## Performance

- Single-run execution time: 3.059 ms
- This is a local single-run measurement, not a load or production benchmark.

## Limitations

- The HR session is a predefined fixture and is not a real interview for candidate C001.
- HR manual comparisons use stored dataset judgments, not newly collected independent human evaluations.
- Technical scores are sample evaluator-provided ratings.
- Machine-test score is a sample calculation; no coding task was executed.
- The machine-test rubric is design-only and unvalidated.
- ATS score uses the available parsed resume fields; missing projects and certifications are treated as empty lists.
- This simulation is not evidence of production readiness or validated hiring accuracy.

## Improvement recommendations

- Collect independent human-reviewed examples before reporting hiring accuracy.
- Validate ATS field mapping and scoring against approved job-specific criteria.
- Validate screening rules against diverse, reviewed answer samples.
- Obtain subject-matter approval for technical questions and scoring rubrics.
- Implement and validate machine-test execution before treating it as a live stage.
- Connect each candidate's actual interview records to the unified pipeline.
- Run repeated and load tests before drawing performance conclusions.

## Decision safeguard

The final recommendation is decision support only. Human review remains necessary; this report does not establish autonomous employment decision capability.


