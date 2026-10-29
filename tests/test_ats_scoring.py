from pprint import pprint

from engines.ats_scoring_engine import ATSScoringEngine


engine = ATSScoringEngine()

# -----------------------------------
# Test Candidate Scoring
# -----------------------------------

report = engine.calculate(

    role="Software Engineer",

    skill_match=95,

    experience_relevance=70,

    education_alignment=100,

    semantic_similarity=64.2

)

print("\nATS Scoring Report:\n")

pprint(report)