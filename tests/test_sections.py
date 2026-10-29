from parsers.resume_parser import ResumeParser
from parsers.section_extractor import SectionExtractor

parser = ResumeParser()
extractor = SectionExtractor()

text = parser.parse("data/resumes/Shahna_Majin_Resume .pdf")

sections = extractor.extract(text)

for section, content in sections.items():

    print("=" * 60)
    print(section)
    print("=" * 60)
    print(content)