# ZECPath AI — HR Interview Developer Handbook

## 1. Purpose

This handbook explains the current HR Interview Python modules, scoring interface, local development workflow, and the boundary between the Python engine and the FastAPI application.

## 2. Prerequisites

The project environment recorded for development is:

- Windows 11
- Python 3.10
- PowerShell
- Project virtual environment: `venv`

Use the project's existing dependency files and environment setup. Do not install packages globally unless the project requires it.

## 3. Start from the repository root

```powershell
cd C:\Users\kcher\Desktop\intership\Project\zecpath-ai
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use the execution-policy approach approved for your machine or run the environment's Python executable directly.

## 4. Important files

| Path | Purpose |
|---|---|
| `interview_ai/hr_interview_scoring_engine.py` | Score validation, response averaging, weighted score and band |
| `interview_ai/hr_score_report.py` | Structured dictionary and JSON report |
| `data/hr_interview_scoring/scoring_weights.json` | Runtime scoring weights |
| `data/hr_interview_scoring/sample_hr_interview.json` | Sample scoring input (verify current contents before use) |
| `interview_ai/demo_hr_interview_scoring.py` | Scoring demonstration |
| `tests/test_hr_interview_scoring.py` | Scoring engine tests |
| `api/main.py` | FastAPI application and router registration |

Other HR interview modules include question generation, interview flow/state, follow-up handling, communication analysis, confidence analysis, behavioral signals, contradiction detection, and summary generation.

## 5. Run the scoring demonstration

From the repository root:

```powershell
python -m interview_ai.demo_hr_interview_scoring
```

The demo is expected to use the sample scoring data and write a report under `data/hr_interview_scoring/` according to the demo implementation. Check the script before relying on exact output filenames.

## 6. Run focused tests

```powershell
python -m pytest tests/test_hr_interview_scoring.py -v
```

Run the complete test suite before merging changes:

```powershell
python -m pytest -q
```

Record the actual test count and result from the current run. Do not copy a previous run's test count into a new release note.

## 7. Use the scoring engine from Python

```python
from interview_ai.hr_interview_scoring_engine import HRInterviewScoringEngine
from interview_ai.hr_score_report import HRScoreReport

engine = HRInterviewScoringEngine()

responses = [
    {
        "answer_relevance": 90,
        "communication": 85,
        "confidence": 80,
        "consistency": 92,
    }
]

result = engine.score_interview(
    candidate_id="CAND_1001",
    job_id="JOB_2001",
    session_id="SESSION_3001",
    job_title="Python Developer",
    responses=responses,
)

report = HRScoreReport()
report_dict = report.to_dict(result)
report_json = report.to_json(result)

print(report_json)
```

The identifiers and scores above are sample values only.

## 8. Scoring behavior

- Each response must contain all four required components.
- Every component must be between 0 and 100.
- At least one response is required.
- Each component is averaged across responses using the arithmetic mean.
- The configured component weights must sum to 1.0 within a tolerance of 0.0001.
- The final score is clamped to 0–100 and rounded to two decimal places.
- Bands are `strong`, `moderate`, `developing`, and `needs_improvement`.

Always inspect `data/hr_interview_scoring/scoring_weights.json` when changing or explaining the active weights.

## 9. FastAPI integration

The current `api/main.py` registers resume, ATS scoring, shortlisting, and jobs routers. It does not currently register an HR interview router in the inspected source.

To expose HR scoring over HTTP, implement and test a dedicated router and schemas, then register the router in `api/main.py`. Follow the proposed contract in `api_specification.md`; do not assume that the proposed route is live before implementation.

## 10. Development checklist

- [ ] Confirm the scoring configuration and its weights.
- [ ] Validate input shape and numeric ranges.
- [ ] Add or update unit tests for scoring behavior.
- [ ] Test empty responses and missing component keys.
- [ ] Test values below 0 and above 100.
- [ ] Test configuration weights that do not sum to 1.
- [ ] Verify report output and JSON serialization.
- [ ] Run the full test suite.
- [ ] Review privacy, authorization, audit, and retention requirements before API deployment.
- [ ] Update documentation when interfaces or scoring behavior change.

## 11. Human review and responsible use

The scoring engine aggregates upstream signals; it does not establish that those signals are valid measures of job performance. Recruiters should review the underlying evidence and context. Do not use a low confidence or communication signal as an automatic rejection criterion without appropriate validation and human oversight.
