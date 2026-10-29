from pprint import pprint

from parsers.education_extractor import EducationExtractor
from engines.education_relevance import EducationRelevance

text = """
Master of Computer Applications (MCA) – Pursuing 2025 – Present
LEAD College of Management (Autonomous), Palakkad
"""

education = EducationExtractor().extract(text)

report = EducationRelevance().evaluate(
    education,
    "Software Engineer"
)

pprint(report)