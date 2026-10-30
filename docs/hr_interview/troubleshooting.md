# ZECPath AI — HR Interview Troubleshooting

This guide covers issues implied by the current scoring implementation and common local development checks. It does not claim that every issue has already occurred.

## 1. `FileNotFoundError` for scoring weights

**Likely cause:** The configured JSON file is missing or the project is being run from an unexpected checkout.

**Check:**

```powershell
Test-Path .\data\hr_interview_scoring\scoring_weights.json
```

**Resolution:** Restore the expected configuration file from the project repository. If passing a custom `config_path`, confirm that it points to a valid JSON file.

## 2. `KeyError: 'weights'`

**Likely cause:** The configuration JSON does not contain the `weights` object.

**Resolution:** Check the JSON structure and ensure it contains all required component names:

- `answer_relevance`
- `communication`
- `confidence`
- `consistency`

## 3. `ValueError: Scoring weights must sum to 1.0`

**Likely cause:** The configured weights do not total 1.0 within the engine's tolerance.

**Resolution:** Correct the values in `data/hr_interview_scoring/scoring_weights.json`. Use decimal weights, such as `0.35`, rather than percentage integers such as `35`. Confirm all four values sum to 1.0.

## 4. `At least one interview response is required`

**Likely cause:** `responses` is an empty list or another empty value.

**Resolution:** Ensure the session has at least one evaluated response before calling `score_interview()`.

## 5. `Missing scoring component: ...`

**Likely cause:** A response dictionary does not contain one of the four required component keys.

**Resolution:** Include all required component fields in every response. Check spelling and underscore placement.

## 6. Component score validation error

**Likely cause:** A component value cannot be converted to a number or falls outside 0–100.

**Resolution:** Supply numeric values in the inclusive range 0–100. Check for `None`, text labels, and percentage values expressed as strings.

## 7. Report generation raises a key error

**Likely cause:** The report formatter received a result that did not come from the expected scoring result structure, or required metadata is missing.

**Resolution:** Pass the result returned by `HRInterviewScoringEngine.score_interview()` to `HRScoreReport.to_dict()` or `to_json()`. Ensure candidate ID, job ID, session ID, and job title are supplied.

## 8. Import errors when running a demo

**Likely cause:** The command was run from inside a subfolder or the project virtual environment is not active.

**Resolution:** Run from the repository root:

```powershell
python -m interview_ai.demo_hr_interview_scoring
```

Confirm that the expected project package and virtual environment are available.

## 9. HR endpoint returns 404

**Likely cause:** The current FastAPI application does not register an HR interview router.

**Resolution:** This is an integration gap in the inspected application, not necessarily a server failure. Implement the HR router, include it in `api/main.py`, restart the app, and verify the route in `/docs`.

## 10. Score seems unexpected

**Checks:**

1. Inspect the raw response component scores.
2. Confirm each response is being averaged as intended.
3. Inspect the active `scoring_weights.json`.
4. Recalculate the weighted sum.
5. Confirm that the expected band thresholds are being applied.

Remember that the engine averages each component across responses before weighting. It does not weight longer interviews more heavily simply because they contain more responses.

## 11. Tests fail

Run the focused test first:

```powershell
python -m pytest tests/test_hr_interview_scoring.py -v
```

Then run the full suite:

```powershell
python -m pytest -q
```

Read the first failing assertion and traceback. Avoid changing scoring logic just to make a test pass without checking whether the expected behavior is correct.
