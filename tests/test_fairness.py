from pprint import pprint

from engines.normalization_engine import NormalizationEngine
from engines.fairness_engine import FairnessEngine


resume_text = """
SHAHNA MAJI
Email: shahnamaji@gmail.com
Phone: +91 9876543210
Female
Married
Python   Django   SQL   Python   Python
"""

resume = {
    "name": "SHAHNA MAJI",
    "summary": "Python   Django   SQL   Python   Python"
}


# Normalization
normalizer = NormalizationEngine()
normalized_resume = normalizer.normalize_resume(resume)

print("\nNormalized Resume:\n")
pprint(normalized_resume)


# Fairness and bias reduction
fairness = FairnessEngine()

masked = fairness.mask_personal_attributes(resume_text)

print("\nMasked Resume Text:\n")
print(masked)


bias = fairness.evaluate_bias_indicators(resume_text)

print("\nBias Indicators:\n")
pprint(bias)


penalty = fairness.keyword_penalty(skill_count=25)

print("\nKeyword Penalty:\n")
print(penalty)


score = fairness.normalize_score(108)

print("\nNormalized Score:\n")
print(score)