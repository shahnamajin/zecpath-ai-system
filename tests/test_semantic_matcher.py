from pprint import pprint

from engines.semantic_matcher import SemanticMatcher


matcher = SemanticMatcher()

# -----------------------------------
# Overall Resume ↔ JD Matching
# -----------------------------------

resume_text = """
MCA student skilled in Python, SQL, Django,
REST APIs, Flutter, and Machine Learning.
Built healthcare and crop recommendation projects.
"""


job_description = """
Looking for a Python Developer with knowledge of
Django, REST APIs, SQL, and Machine Learning.
Experience in application development is preferred.
"""


print("\nOverall Matching:\n")

overall_result = matcher.match(
    resume_text,
    job_description
)

pprint(overall_result)

# -----------------------------------
# Section-wise Matching
# -----------------------------------

print("\nSection-wise Matching:\n")

section_result = matcher.section_match(

    resume_skills="Python SQL Django REST APIs Machine Learning",

    jd_skills="Python Django REST APIs SQL Machine Learning",

    resume_exp="Built web and mobile applications using Python and Flutter",

    jd_exp="Experience in Python application development and backend APIs",

    resume_projects="Healthcare prediction system and crop recommendation project",

    jd_projects="Machine learning healthcare application project"

)

pprint(section_result)