# Day 36 – Confidence & Stress Indicators

## Objective

Assess observable candidate confidence-related behavioral signals from interview responses.

> The implementation summarizes textual/conversational indicators. It is not a psychological, medical, or definitive emotional-state assessment.

## 1. Hesitation Detection

The confidence analyzer detects:

- Filler/hesitation markers: `um`, `uh`, `erm`, `hmm`, `mmm`
- Pausing markers in transcript text: `...`, `--`
- Hesitation rate per 100 words

Hesitation levels:

| Rate | Level |
|---|---|
| 0–4 | Low |
| >4–10 | Moderate |
| >10 | High |

## 2. Uncertainty Detection

The system detects phrases such as:

- I think
- maybe
- probably
- perhaps
- I guess
- I'm not sure
- I don't know
- possibly
- might be
- could be

## 3. Repeated Words

Adjacent repeated words are detected as a hesitation/disfluency signal.

Example:

`I worked worked on a project.`

## 4. Sentiment Analysis

The sentiment engine uses a transparent positive/negative indicator vocabulary and returns:

- sentiment: positive / neutral / negative
- normalized sentiment score from -1 to +1
- positive indicators
- negative indicators

## 5. Contradiction Detection

The baseline detector identifies simple contradiction patterns, especially conflicting numeric claims in the same response.

Example:

`I have two years of experience. I have five years of experience.`

This is flagged as a possible numeric conflict.

## 6. Behavioral Confidence Score

The score uses the following components:

| Component | Weight |
|---|---:|
| Hesitation Control | 25% |
| Uncertainty Control | 20% |
| Repetition Control | 15% |
| Contradiction Control | 20% |
| Sentiment Signal | 10% |
| Response Stability | 10% |

Formula:

`Behavioral Confidence =`
`Hesitation Control × 0.25`
`+ Uncertainty Control × 0.20`
`+ Repetition Control × 0.15`
`+ Contradiction Control × 0.20`
`+ Sentiment Signal × 0.10`
`+ Response Stability × 0.10`

## 7. Confidence Bands

| Score | Band |
|---|---|
| 80–100 | High behavioral confidence |
| 60–79.99 | Moderate behavioral confidence |
| 40–59.99 | Low behavioral confidence |
| 0–39.99 | Very low behavioral confidence |

## 8. Stress Indicators

The system flags observable indicators when present:

- High hesitation
- High/moderate uncertainty
- Repeated words
- Negative sentiment
- Contradictory response
- Very short response

These are **signals for interview analysis**, not proof that a candidate is stressed.

## 9. Conversation / Response Inputs

The analyzer accepts optional response duration so speaking pace can be calculated as WPM. If duration is unavailable, pace is reported as unavailable rather than inferred.

## 10. Files

- `data/confidence_stress/signal_parameters.json`
- `data/confidence_stress/confidence_test_cases.json`
- `interview_ai/confidence_analyzer.py`
- `interview_ai/sentiment_scoring_engine.py`
- `interview_ai/contradiction_detector.py`
- `interview_ai/behavioral_signal_engine.py`
- `interview_ai/demo_confidence_stress.py`
- `tests/test_confidence_stress.py`

## 11. Limitations

This is a transparent heuristic baseline. Transcript text alone cannot establish a person's actual emotional state or psychological condition. Production use should treat these outputs as supporting behavioral signals and combine them with broader interview evidence rather than making high-stakes decisions from a single score.
