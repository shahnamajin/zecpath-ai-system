# ZECPath AI – Behavioral AI Design Document
## Day 48: Behavioral AI Research & Design

**Status:** Design specification (not an implemented or validated production model)  
**Purpose:** Define a privacy-conscious framework for describing observable interview-video signals.

## 1. Objective and scope

The system may measure limited, observable video interaction patterns to support interview-session diagnostics and optional recruiter context. It must not infer a candidate's honesty, personality, confidence, emotional state, motivation, intelligence, or job suitability from facial or body signals.

Behavioral observations must never override technical answers, work samples, structured interview ratings, or job-related evidence. The feature must not be used as an automatic rejection, ranking, or hiring-decision mechanism.

## 2. Research summary

Research indicates that nonverbal cues can influence interviewers' judgments. A meta-analysis of 63 studies (N=4,868) found associations between some nonverbal cues and interview ratings, while also reporting moderation effects, including gender-related differences for certain cues. These findings do not establish that a camera-derived cue is a valid measure of job performance or an individual's internal state.

Research on automated video interviews highlights the need to assess reliability, validity, generalizability, and bias rather than assuming that machine-extracted behaviors are objective.

Employment AI can disadvantage applicants with disabilities. U.S. DOJ/EEOC guidance specifically discusses risks from facial and voice analysis and the need to assess whether hiring technology screens out qualified people with disabilities. This is used here as a design-risk reference, not as a statement of legal advice or a claim of compliance in every jurisdiction.

## 3. Observable signal inventory

### 3.1 Eye movement and gaze stability
Potential observations:
- Estimated face-relative gaze direction, only if the camera quality supports it.
- Proportion of valid tracked frames in which gaze is approximately toward the screen/camera.
- Count and duration of sustained gaze-direction changes away from the screen region.

Limitations:
- Webcam gaze estimation is approximate and sensitive to camera position, glasses, lighting, head pose, and calibration.
- Looking away may be normal thinking behavior, reading notes, using assistive technology, or a communication preference.
- Do not describe gaze as honesty, confidence, attentiveness, or engagement.

### 3.2 Head movement
Potential observations:
- Head-pose availability and tracking continuity.
- Magnitude and frequency of head-pose changes within a response.
- Long periods with no reliable pose estimate (which may indicate tracking failure, not candidate behavior).

Limitations:
- Natural movement, camera framing, mobility differences, and device placement affect measurements.
- Nodding or stillness must not be interpreted as agreement, understanding, confidence, or nervousness.

### 3.3 Facial engagement
Potential observations:
- Whether a face is detectable and trackable, if the candidate has opted into video analysis.
- Face visibility / tracking coverage.
- Coarse motion activity in the face region, only as a descriptive signal.

Limitations:
- Do not classify emotions (happy, sad, angry, fearful), personality, sincerity, enthusiasm, or motivation.
- Do not penalize neutral expressions, atypical facial movement, facial differences, or disability-related movement patterns.

### 3.4 Attention patterns
Potential observations:
- Time coverage for which the face/gaze estimate is technically valid.
- Time intervals with detected gaze-direction changes, described neutrally.
- Technical interruptions such as camera loss or low-confidence tracking.

Limitations:
- Visual direction is not a reliable measure of mental attention or listening.
- Do not label a person distracted or inattentive based on gaze alone.

### 3.5 Repetitive movement / gestures
Potential observations:
- Repeated motion events in a defined region, if a future validated detector exists.
- Event count and duration, with confidence and data-quality flags.

Limitations:
- Do not infer nervousness, anxiety, deception, discomfort, or intent.
- This signal is excluded from candidate scoring and should remain experimental until validated.

## 4. Measurable indicators

All indicators are session-level descriptive statistics, not personality or employability scores.

| Indicator | Definition | Output |
|---|---|---|
| Tracking coverage | Valid tracked frames / eligible frames | 0–1 ratio |
| Screen-region gaze estimate | Valid gaze samples within a broad calibrated screen region / valid gaze samples | 0–1 ratio; optional |
| Gaze-direction event rate | Number of sustained direction-change events / valid tracked minutes | events/min; optional |
| Head-motion event rate | Number of pose-change events above a calibrated threshold / valid tracked minutes | events/min |
| Face visibility coverage | Frames with usable face detection / eligible frames | 0–1 ratio |
| Repeated-motion event count | Candidate-neutral movement events per session, only if validated | integer; experimental |
| Data-quality status | Camera, lighting, occlusion, tracking confidence and coverage checks | valid / limited / unavailable |

Do not convert these measurements into a candidate quality, personality, focus, distraction, confidence, or nervousness score.

## 5. Signal-to-insight policy

Permitted output language:
- "Gaze estimate available for 72% of eligible frames."
- "Four sustained gaze-direction changes were detected during the response."
- "Head-pose tracking was unavailable for 18% of the response."
- "Video quality was insufficient for this indicator."

Prohibited output language:
- "Candidate is dishonest / nervous / distracted / not confident."
- "Candidate has poor focus."
- "Candidate is not interested."
- "Candidate should be rejected due to body language."

The product UI must label these as **observations**, include confidence and coverage, and show a caution that visual observations are not evidence of internal state.

## 6. Non-invasive analysis approach

1. Explain the feature before the interview and obtain explicit, separate opt-in consent.
2. Offer an equivalent non-video route without penalty. The interview must remain accessible if consent is declined.
3. Process only the minimum video frames required for approved technical observations.
4. Prefer on-device or transient processing where feasible; do not store raw video or face embeddings by default.
5. Do not perform face identification, emotion recognition, demographic inference, or biometric identity matching.
6. Suppress an indicator when tracking coverage or confidence is below a configured threshold.
7. Keep observations separate from ATS score, technical score, HR score, ranking, and automated decision workflows.
8. Make outputs visible to the candidate and recruiter with an explanation of what was measured and what was not inferred.
9. Provide correction, review, deletion, and accommodation workflows.
10. Conduct documented accessibility, subgroup, reliability, and job-related validity testing before any operational use.

## 7. Proposed architecture

**Video input (consent-gated)**  
→ Frame sampling / quality checks  
→ Face landmark and head-pose estimation (no identity recognition)  
→ Optional gaze approximation  
→ Temporal event aggregation  
→ Data-quality and confidence gate  
→ Neutral observation summary  
→ Human-readable session report

The observation service must not call the candidate ranking or recommendation service. It must not emit a hire/reject recommendation.

## 8. Data model

Each observation should include:
- session_id (pseudonymous)
- signal_name
- measurement_name
- value
- unit
- time_window_start / time_window_end
- confidence
- tracking_coverage
- quality_status
- model_version
- consent_version
- created_at
- limitations_note

Do not persist raw frames, face templates, or identity embeddings in the default design. Apply retention and deletion rules to any derived data.

## 9. Validation plan

Before pilot:
- Define intended use and prohibited uses in product requirements.
- Test camera, lighting, glasses, skin tone, head pose, bandwidth and device variation.
- Test with diverse participants, including people with disabilities and neurodivergent participants, through accessible and voluntary research.
- Measure tracking error, missingness, false event rates, calibration, and test-retest stability.
- Check whether missing data disproportionately affects any group.
- Validate whether each indicator adds any job-related value; if not, do not expose it to recruiters.
- Have privacy, accessibility, legal, and domain reviewers approve the intended use.
- Provide a non-video alternative and verify it does not reduce candidate opportunity.

## 10. Acceptance criteria for a future implementation

- No output infers emotion, honesty, personality, anxiety, confidence, or mental attention.
- No behavioral observation changes ATS, technical, HR, rank, or hiring decisions.
- Consent can be declined or withdrawn without penalty.
- Low-quality tracking produces "unavailable", not a low score.
- Every displayed value includes its definition, coverage, confidence, and limitation.
- Raw video and biometric identifiers are not retained by default.
- Accessibility and fairness validation is documented before pilot.

## 11. Research references

1. Martín-Raugh et al. (2023), "Speaking without words: A meta-analysis of over 70 years of research on the power of nonverbal cues in job interviews", *Journal of Organizational Behavior*. https://doi.org/10.1002/job.2670
2. Hickman et al. (2025), "Are automated video interviews smart enough? Behavioral modes, reliability, validity, and bias of machine learning cognitive ability assessments", *Journal of Applied Psychology*. https://pubmed.ncbi.nlm.nih.gov/39325374/
3. U.S. Department of Justice, "Algorithms, Artificial Intelligence, and Disability Discrimination in Hiring" (2022). https://www.ada.gov/resources/ai-guidance/
4. U.S. EEOC, "Visual Disabilities in the Workplace and the Americans with Disabilities Act". https://www.eeoc.gov/laws/guidance/visual-disabilities-workplace-and-americans-disabilities-act
5. Landers (2026), "Hiring People in Organizations: The State and Future of the Science", *Annual Review of Organizational Psychology and Organizational Behavior*. https://doi.org/10.1146/annurev-orgpsych-020924-072127

---
**Implementation status:** This is a research and design deliverable. No computer-vision model, scoring pipeline, or production integration is claimed as implemented or validated.
