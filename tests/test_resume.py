from parsers.resume_parser import ResumeParser

parser = ResumeParser()

text = parser.parse("data/resumes/sample_simple.pdf")

print(text)