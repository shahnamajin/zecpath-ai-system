from engines.eligibility_engine import EligibilityEngine
from config.eligibility_rules import ELIGIBILITY_RULES


engine = EligibilityEngine()

rules = ELIGIBILITY_RULES["Software Engineer"]


# ---------------------------------
# Candidate 1 - Eligible
# ---------------------------------

candidate_1 = {
    "candidate_id": "CAND-001",
    "ats_score": 85,
    "skills": ["Python", "SQL", "FastAPI"],
    "experience_years": 2,
    "location": "Kerala",
    "available": True
}

result_1 = engine.evaluate(candidate_1, rules)

print("\nCandidate 1")
print(result_1)


# ---------------------------------
# Candidate 2 - Review
# Missing mandatory skill
# ---------------------------------

candidate_2 = {
    "candidate_id": "CAND-002",
    "ats_score": 82,
    "skills": ["Python", "Java"],
    "experience_years": 2,
    "location": "Kerala",
    "available": True
}

result_2 = engine.evaluate(candidate_2, rules)

print("\nCandidate 2")
print(result_2)


# ---------------------------------
# Candidate 3 - Rejected
# ATS score too low
# ---------------------------------

candidate_3 = {
    "candidate_id": "CAND-003",
    "ats_score": 55,
    "skills": ["Python", "SQL"],
    "experience_years": 2,
    "location": "Kerala",
    "available": True
}

result_3 = engine.evaluate(candidate_3, rules)

print("\nCandidate 3")
print(result_3)


# ---------------------------------
# Basic Assertions
# ---------------------------------

assert result_1["eligibility"] == "Eligible"
assert result_2["eligibility"] == "Review"
assert result_3["eligibility"] == "Rejected"

print("\nAll eligibility tests passed.")