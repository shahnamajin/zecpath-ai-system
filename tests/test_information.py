from parsers.resume_parser import ResumeParser
from parsers.information_extractor import InformationExtractor
from utils.file_writer import FileWriter

parser = ResumeParser()
extractor = InformationExtractor()
writer = FileWriter()

text = parser.parse("data/resumes/Shahna_Majin_Resume .pdf")

candidate = extractor.extract(text)

writer.save(
    candidate,
    "data/parsed_resumes/shahna_resume .json"
)

print(candidate)