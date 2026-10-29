from pprint import pprint

from parsers.resume_parser import ResumeParser
from parsers.section_extractor import SectionExtractor
from parsers.experience_extractor import ExperienceExtractor

parser = ResumeParser()

text = parser.parse("data/resumes/sample_simple.pdf")

sections = SectionExtractor().extract(text)

experience = ExperienceExtractor().extract(
    sections.get("EXPERIENCE", "")
)

pprint(experience)