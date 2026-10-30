# ZECPath AI – Malpractice & Integrity Detection Framework
## Day 49: Design Specification

**Status:** Design only – not implemented, calibrated, or production validated  
**Purpose:** Identify interview-session events that may warrant a neutral clarification or human review. The system must not automatically conclude that a candidate cheated.

## 1. Objective and scope

Design a consent-based integrity monitoring framework for remote interviews. The framework records limited, observable session events, evaluates event quality and context, and assigns a review priority. It distinguishes technical interruptions and ambiguous behavior from corroborated policy-relevant events.

**Core rule:** A signal is not proof of malpractice. No single signal, including tab switching, loss of focus, external audio, or gaze direction, is sufficient to label a candidate as cheating.

## 2. Signal inventory

| Signal | Observable event | Possible benign explanations | Design treatment |
|---|---|---|---|
| Tab/window switching | Browser visibility changes or window blur/focus events | Reading permitted notes, accessibility tools, system dialogs, accidental click | Record event count and duration; compare with interview rules |
| Loss of screen focus | Page visibility hidden, window blur, or focus lost | OS notification, call, browser permission prompt, device issue | Separate page-hidden from window-blur; avoid claiming what the candidate viewed |
| External voice / additional speaker | Audio activity or a possible second voice in an opted-in audio stream | Household member, TV, background conversation, echo, noise, shared room | Experimental, privacy-sensitive; do not identify speaker or transcribe background conversation |
| Repeated looking away | Repeated gaze-direction changes, only if a validated opt-in visual feature exists | Thinking, reading, cultural style, disability, camera placement, notes | Context-only observation; never a standalone malpractice signal |
| Reconnection / interruption | Network drop, microphone/camera interruption, browser reconnect | Connectivity and hardware problems | Technical event, not an integrity event |

### 2.1 Tab switching frequency
Use browser-level visibility and focus events only where the platform can legitimately observe them. Browser visibility APIs can report that the interview page became hidden; they cannot reliably establish which application or content the candidate opened. Do not install hidden monitoring software or inspect unrelated applications.

Suggested event fields:
- `event_type`: `page_hidden`, `page_visible`, `window_blur`, `window_focus`
- `occurred_at`
- `duration_ms` (when measurable)
- `question_id` / `interview_phase`
- `capture_source`
- `technical_quality`

### 2.2 Loss of screen focus
Keep page visibility and window focus as separate signals. A browser tab becoming hidden is more concrete than a window blur event. A blur event can occur due to operating-system dialogs, notifications, assistive technology, or normal device behavior.

### 2.3 External voice detection
This is the highest privacy-risk signal in this design. Do not record or analyze the surrounding room by default. If an audio-based second-speaker detector is ever considered:
- require explicit, separate opt-in and clear notice;
- process only the interview audio stream, with no ambient-room capture beyond what is necessary;
- do not identify, name, or profile speakers;
- do not retain raw audio or voiceprints by default;
- do not transcribe background speech;
- suppress results when audio quality is poor or overlap/echo is likely;
- offer a non-audio alternative without penalty.
A possible second voice is only a prompt for human clarification, not evidence of assistance.

### 2.4 Repeated looking away
Do not classify gaze changes as cheating. If the candidate has opted into a visual feature, the system may describe gaze-direction event counts and coverage neutrally. It must not infer distraction, reading answers, deception, or external assistance from gaze alone.

## 3. Event normalization and quality gates

Every event must include:
- pseudonymous `session_id`;
- `event_id` and event type;
- timestamp and duration where available;
- relevant interview phase / question identifier;
- source and detector version;
- confidence and data-quality status;
- consent and policy configuration version;
- benign-context / accommodation marker when provided;
- review status and reviewer rationale.

Quality handling:
- Missing or low-quality data becomes `unavailable`, not a positive flag.
- Deduplicate repeated browser events caused by rapid focus transitions.
- Ignore events during declared breaks, setup, reconnect, or approved accommodations.
- Do not infer event duration if the platform cannot measure it reliably.
- Keep raw media separate from event metadata; minimize retention.

## 4. Detection logic

### 4.1 Threshold-based event indicators

Initial values below are **configurable pilot defaults for workflow testing only**, not validated cheating thresholds.

| Indicator | Provisional trigger | Action |
|---|---|---|
| Short focus changes | 3 or more focus/visibility transitions within 60 seconds | Log event cluster; no candidate-facing accusation |
| Sustained page-hidden interval | Page hidden for more than 10 seconds while a timed question is active | Neutral clarification prompt or review note, depending on interview policy |
| Repeated page-hidden intervals | 2 or more intervals over 10 seconds in one interview section | Raise review priority if not explained by a technical event or permitted workflow |
| Possible second voice | Detector confidence meets a separately validated threshold and audio quality is adequate | Mark `needs_human_review`; never label as confirmed assistance |
| Repeated gaze changes | Measurement available and tracking quality adequate | Context-only observation; does not increase integrity risk by itself |

Thresholds must be configurable by interview type and disclosed in candidate instructions. The system should not count ordinary window-blur events as equivalent to page-hidden events.

### 4.2 Pattern recognition

A pattern may be raised only when multiple independent, policy-relevant event types occur in a defined time window and the underlying measurements pass quality checks.

Example:
- multiple sustained page-hidden events during active questions; plus
- a separately validated possible additional-speaker event; plus
- no known technical interruption or permitted workflow explanation.

Even this combination is a **review trigger**, not proof. Repeated gaze changes do not corroborate cheating and must not be used as an independent pattern feature.

### 4.3 Risk calculation

Use a transparent event-based review-priority score, not a candidate integrity or honesty score.

Provisional event weights:
- `page_hidden_sustained`: 2
- `page_hidden_repeated`: 2
- `window_blur_cluster`: 1
- `possible_additional_voice`: 2 (experimental; only if separately validated)
- `repeated_gaze_change`: 0 (context-only)
- `network_or_device_interruption`: 0 (technical context)

Apply deduplication and cap repeated events per type per time window. Exclude events during breaks, setup, approved accommodation, or known technical incidents.

Review priority:
- 0–1: `no_integrity_flag`
- 2–3: `low_review_priority`
- 4–5: `medium_review_priority`
- 6+: `high_review_priority`

These bands only prioritize human review. They must not be presented as a probability of cheating, candidate trustworthiness, or a hiring score. They require validation and calibration before any pilot.

## 5. Warning and flagging system

### Candidate-facing warnings
Warnings should be neutral, factual, and non-accusatory. Examples:
- "Your interview page appears to have lost focus. If this was accidental or caused by a device notification, you may continue."
- "We detected a possible audio interruption. Please check your microphone before continuing."
- "If you need to use an approved accessibility tool or permitted notes, follow the interview instructions or contact the interviewer."

Do not display "cheating detected", "suspicious candidate", or a numeric risk score to the candidate.

### Recruiter-facing flags
Recruiter UI should show:
- event type and timestamp;
- duration / count;
- detector confidence and data-quality status;
- question / interview phase;
- applicable interview policy;
- candidate explanation, if provided;
- review state: `unreviewed`, `clarification_requested`, `explained`, `not_actionable`, `escalated`;
- reviewer notes and audit trail.

Do not display a definitive malpractice label. Require human review before any action that could affect the candidate.

## 6. Integration with Day 48 Behavioral AI

Day 48 visual observations and Day 49 integrity events must remain distinct.

| Day 48 behavioral observation | Day 49 integrity treatment |
|---|---|
| Gaze-direction changes | Context only; zero risk weight |
| Head movement | Context only; zero risk weight |
| Face visibility / tracking loss | Data-quality state, not risk |
| Repeated movement | Not an integrity feature |
| Visual tracking unavailable | No penalty; mark unavailable |

Only direct session events (e.g., browser page visibility changes) and any future separately validated audio event may contribute to review priority. Do not combine gaze, facial movement, head movement, or emotion inference into a malpractice score.

## 7. Proposed architecture

Candidate notice / consent / interview policy  
→ Browser session event collector (visibility and focus only)  
→ Optional, separately consented audio event module (future / experimental)  
→ Event normalization and deduplication  
→ Technical-quality and accommodation filters  
→ Rule engine and time-window pattern evaluator  
→ Review-priority tag  
→ Candidate clarification / recruiter review queue  
→ Audited human disposition

The service must be isolated from ATS ranking, resume scoring, technical scoring, and automated hiring decisions.

## 8. Data model

`IntegrityEvent`:
- `event_id`
- `session_id`
- `event_type`
- `started_at`
- `duration_ms`
- `question_id`
- `source`
- `confidence`
- `quality_status`
- `policy_version`
- `consent_version`
- `context_tags`
- `deduplication_key`

`IntegrityReview`:
- `review_id`
- `session_id`
- `review_priority`
- `triggered_event_ids`
- `status`
- `candidate_explanation`
- `reviewer_id`
- `reviewer_notes`
- `decision_rationale`
- `created_at`
- `updated_at`

## 9. Privacy, fairness, and candidate rights

- Provide clear advance notice of monitored events and why they are collected.
- Collect only the events needed for the stated interview-integrity purpose.
- Do not use covert screen recording, keystroke logging, process inspection, or hidden monitoring.
- Do not record or retain room audio by default.
- Provide accommodations and a non-audio / non-video alternative where relevant.
- Allow candidates to explain interruptions and request review.
- Set retention periods and deletion controls; restrict access and audit all reviews.
- Test false-positive rates across devices, operating systems, network conditions, and accessibility workflows.
- Do not use risk flags as the sole basis for rejection or adverse decisions.

## 10. Validation and rollout plan

1. Offline simulation with synthetic browser events and test audio clips; no real candidate decisions.
2. Measure event detection precision, recall, duplicate rate, and false flags.
3. Test notifications, OS dialogs, accessibility tools, screen readers, reconnects, and permitted notes.
4. Conduct privacy, accessibility, security, and legal review.
5. Run a voluntary shadow pilot where flags do not affect hiring outcomes.
6. Review false positives with candidate feedback and independent reviewers.
7. Only after documented approval consider limited human-review workflow deployment.

## 11. Acceptance criteria

- A single signal never produces a confirmed malpractice finding.
- Gaze and movement observations contribute zero integrity-risk weight.
- Browser events are limited to page visibility / focus state; no hidden device surveillance.
- Audio detection is off by default and requires separate consent and validation.
- Technical failures and low-quality signals are marked unavailable or technical context.
- Every flag includes event evidence, quality metadata, policy context, and human disposition.
- No automated rejection, ranking, or candidate integrity score is produced.
- Candidate notice, explanation, accommodation, review, and deletion workflows are specified.

## 12. Implementation boundary

This document defines a design. It does not claim that browser event collection, voice detection, pattern recognition, warning UI, or risk scoring has been implemented. The numeric thresholds and weights are provisional design parameters and must be tested and approved before use.
