from pprint import pprint

from parsers.resume_parser import ResumeParser
from parsers.section_extractor import SectionExtractor
from parsers.experience_extractor import ExperienceExtractor
from engines.experience_relevance import ExperienceRelevance

parser = ResumeParser()

text = parser.parse("data/resumes/sample_simple.pdf")

sections = SectionExtractor().extract(text)

experience = ExperienceExtractor().extract(
    sections.get("EXPERIENCE", "")
)

engine = ExperienceRelevance()

report = engine.generate(
    experience,
    "Software Engineer"
)

pprint(report)