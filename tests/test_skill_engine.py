from parsers.resume_parser import ResumeParser
from parsers.section_extractor import SectionExtractor
from parsers.skill_extractor import SkillExtractor

parser = ResumeParser()

text = parser.parse("data/resumes/Shahna_Majin_Resume .pdf")

sections = SectionExtractor().extract(text)

skills = SkillExtractor().extract(
    sections.get("SKILLS", "")
)

from pprint import pprint

pprint(skills)