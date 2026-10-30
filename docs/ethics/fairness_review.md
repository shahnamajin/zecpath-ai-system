# ZECPath AI — Fairness Review

## 1. Objective
Review the hiring AI system for job relevance, consistent scoring,
demographic bias risks, and explainability.

## 2. Scoring components reviewed
The ATS scorer currently assigns:
- Skills: 40 points
- Education: 20 points
- Projects: 20 points
- Experience: 10 points
- Certifications: 10 points

The unified scoring engine combines ATS, screening, and HR interview
scores using configurable weights.

## 3. Demographic bias safeguards
The ethics policy identifies race, ethnicity, religion, sex, gender
identity, disability, date of birth, and marital status as attributes
to exclude from scoring.

The visible scoring code does not explicitly use these attributes.
However, the full data pipeline and upstream AI components still need
review for indirect signals and proxy variables.

Potential proxy signals include names, photographs, addresses,
graduation dates, and other information unrelated to job requirements.

## 4. Explainability
The ATS report records component scores, matched skills, missing skills,
and a recommendation. This supports basic explanations of the result.

Further review should verify that recruiters can understand the
unified score, its component weights, and the evidence behind
screening and interview scores.

## 5. Fairness validation plan
- Test equivalent candidate profiles with irrelevant demographic
  fields changed or removed.
- Confirm irrelevant attributes do not change scores.
- Review false rejection and selection rates across groups where
  lawful, appropriate, and supported by representative data.
- Document sample limitations and investigate disparities.
- Require human review before adverse hiring decisions.

## 6. Current status
Initial code review completed.
Full pipeline review and fairness tests remain outstanding.
No claim of validated fairness is made at this stage.
