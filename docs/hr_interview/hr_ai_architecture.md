# ZECPath AI — HR Interview AI Architecture

**Document status:** Day 44 documentation  
**Scope:** Current Python HR interview modules and their integration boundary with the FastAPI application.

## 1. Purpose

The HR Interview AI supports structured, AI-assisted HR interviews. It is designed for fresher and experienced candidates and technical and non-technical roles. The engine supports question generation, interview state, candidate responses, follow-up eligibility, communication and behavioral signal analysis, scoring, and summary/report generation.

## 2. Current module layout

The confirmed implementation is under `interview_ai/`.

| Module | Responsibility |
|---|---|
| `question_generator.py` | Generates interview questions from the question bank and interview context. |
| `interview_flow.py` | Coordinates the interview flow. |
| `interview_state.py` | Maintains interview state. |
| `adaptive_question_engine.py` | Supports adaptive question selection. |
| `dynamic_follow_up_engine.py` | Determines and generates dynamic follow-up questions. |
| `follow_up_handler.py` | Handles follow-up behavior. |
| `communication_analyzer.py` | Extracts communication features from a text response. |
| `communication_scorer.py` | Produces a communication score from extracted features. |
| `confidence_analyzer.py` | Analyzes confidence/hesitation signals. |
| `behavioral_signal_engine.py` | Produces a behavioral confidence signal from transcript observations. |
| `sentiment_scoring_engine.py` | Provides sentiment scoring functionality. |
| `contradiction_detector.py` | Detects possible inconsistencies in responses. |
| `hr_interview_scoring_engine.py` | Aggregates response-level component scores into an interview score. |
| `hr_score_report.py` | Converts the scoring result into a structured report or JSON. |
| `interview_summary_generator.py` | Produces an interview summary. |
| `summary_report_formatter.py` | Formats summary/report output. |
| `hr_interview_simulator.py` | Runs stored simulation sessions and compares configured AI results with reference evaluations. |

The exact runtime call sequence between every analyzer is not established by the files inspected for this document. Treat this table as a module responsibility map, not proof that every module is wired into one live pipeline.

## 3. High-level data flow

```text
Question bank + candidate/job context
                |
                v
       Question generation
                |
                v
     Interview flow and state
                |
                v
       Candidate responses
                |
                v
  Response analysis / follow-ups
       |       |       |
       v       v       v
 Communication Confidence Consistency
       \       |       /
        \      |      /
         Component scores
                |
                v
       HR scoring aggregation
                |
                v
       Explainable score report
                |
                v
      Interview summary / review
```

This diagram describes the intended logical flow. The HR scoring engine is confirmed to accept response records containing four component scores; it does not itself derive those scores from raw audio or text.

## 4. HR score aggregation

The scoring engine is `interview_ai/hr_interview_scoring_engine.py`.

Required component keys for every response:

- `answer_relevance`
- `communication`
- `confidence`
- `consistency`

Each component must be numeric and between 0 and 100. At least one response is required.

For each component, the engine calculates the arithmetic mean across responses:

`component_average = mean(response_component_scores)`

It then calculates the weighted total:

`final_score = Σ(component_average × configured_weight)`

The scoring weights are loaded from:

`data/hr_interview_scoring/scoring_weights.json`

The existing scoring design document records the intended weights as relevance 35%, communication 25%, confidence 20%, and consistency 20%. Confirm the JSON configuration before relying on those values in a deployment.

### Score bands

| Score | Band |
|---:|---|
| 80–100 | `strong` |
| 60–79.99 | `moderate` |
| 40–59.99 | `developing` |
| 0–39.99 | `needs_improvement` |

Scores are clamped/rounded to a 0–100 range with two decimal places.

## 5. Report structure

`HRScoreReport.to_dict()` returns:

- `candidate`: candidate ID, job ID, session ID, job title
- `interview_summary`: responses evaluated and normalization method
- `score`: final score and band
- `component_scores`: averaged component scores
- `explainable_breakdown`: score, weight, and weighted contribution per component

`to_json()` serializes this structure as indented JSON.

## 6. FastAPI integration boundary

The application entry point is `api/main.py`. It creates a FastAPI application titled **Zecpath AI ATS API**, version `1.0.0`, and registers the resume, ATS scoring, shortlisting, and jobs routers.

The inspected route scan found no dedicated HR interview router or HR scoring endpoint. The HR interview scoring engine is therefore documented as a Python module, not as an already exposed HTTP API. See `api_specification.md` for a clearly labelled integration proposal.

## 7. Important limitations and safeguards

- The aggregation engine depends on the quality and validity of upstream component scores.
- Confidence, hesitation, sentiment, and communication signals should not be treated as definitive measures of candidate ability.
- A score or band should support recruiter review, not replace a human hiring decision.
- The simulator uses stored session/reference values; its comparisons are not independent proof of real-world accuracy.
- The scoring module does not, by itself, provide authentication, authorization, persistence, consent capture, or data-retention enforcement.
