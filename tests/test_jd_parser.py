from parsers.jd_parser import JobDescriptionParser
from pprint import pprint


jd_text = """
We are hiring a Software Engineer.

Required Skills:
Python, Django, SQL, Docker and AWS.

Experience:
Minimum 2+ years of software development experience.

Education:
B.Tech, BCA, MCA or Computer Science background.
"""


parser = JobDescriptionParser()

result = parser.parse(jd_text)


print("\nJOB DESCRIPTION PARSING RESULT")
print("=" * 50)

pprint(result)