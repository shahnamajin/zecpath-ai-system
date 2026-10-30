# Behavioral Analysis Framework – ZECPath AI (Day 48)

## A. Workflow

1. **Candidate notice and consent**
   - Explain each signal and purpose in plain language.
   - Ask for separate, explicit opt-in.
   - Provide a non-video alternative with no penalty.
   - Allow withdrawal.

2. **Capture and quality assessment**
   - Use only interview-session video with consent.
   - Check frame rate, lighting, camera availability, occlusion and tracking confidence.
   - Do not identify the person or build a face template.

3. **Feature extraction**
   - Estimate coarse gaze direction (optional).
   - Estimate head pose and temporal movement.
   - Measure face visibility / tracking continuity.
   - Repetitive movement remains experimental.

4. **Temporal aggregation**
   - Aggregate by response interval, not isolated frames.
   - Calculate rates only over valid tracked time.
   - Record missingness and quality metadata.

5. **Quality gate**
   - If tracking coverage < 0.60 or confidence < 0.70, mark the signal unavailable.
   - These are provisional engineering gates, not validated thresholds.
   - Never turn missing data into a low candidate score.

6. **Observation generation**
   - Produce neutral, factual descriptions.
   - Attach confidence, coverage, limitations, and model version.
   - Do not infer psychological traits.

7. **Human review and governance**
   - Keep observations separate from candidate ranking and selection scores.
   - Provide candidate access, correction, deletion, and accommodation route.
   - Audit reliability and disparate missingness before any pilot.

## B. Indicator definitions

| Indicator | Formula / method | Unit |
|---|---|---|
| Tracking coverage | valid tracked frames / eligible frames | ratio |
| Screen-region gaze ratio | in-region valid gaze samples / valid gaze samples | ratio |
| Gaze event rate | sustained direction changes / valid tracked minutes | events/min |
| Head movement event rate | pose-change events / valid tracked minutes | events/min |
| Face visibility coverage | usable face frames / eligible frames | ratio |
| Repeated movement count | validated repeated-motion events | count |

## C. Signal-to-insight examples

| Observation | Allowed wording |
|---|---|
| Screen-region gaze ratio = 0.72 | "Estimated gaze was within the calibrated screen region for 72% of valid samples." |
| Head movement event rate = 3.1/min | "An average of 3.1 head-pose changes per valid tracked minute were detected." |
| Face tracking coverage = 0.54 | "Face tracking was available for 54% of eligible frames; this indicator is unavailable due to insufficient coverage." |
| Repeated motion count = 5 | "Five repeated movement events were detected; no psychological interpretation is assigned." |

## D. Non-invasive principles

- Data minimization and purpose limitation.
- Explicit opt-in and equivalent alternative.
- No emotion recognition, identity recognition, or demographic inference.
- No default retention of raw video, face embeddings, or biometric templates.
- Encryption, access control, retention limits, deletion process, and audit logging.
- Accessibility testing and accommodations.
- No automated candidate rejection or ranking from visual signals.

## E. Review checklist

- [ ] Candidate notice and opt-in are implemented.
- [ ] Non-video alternative is equivalent and penalty-free.
- [ ] Low-quality signals are suppressed.
- [ ] Every output has a definition, confidence, coverage, and limitation.
- [ ] No psychological labels appear in UI or report.
- [ ] Behavioral output is technically isolated from ranking/scoring services.
- [ ] Raw video / biometric data are not retained by default.
- [ ] Accessibility and subgroup testing completed.
- [ ] Domain, privacy, and legal review completed before pilot.

## F. Status

This is a design framework only. It does not claim a working detector, calibrated threshold, validated score, or production-ready feature.
