from parsers.resume_parser import ResumeParser
from parsers.information_extractor import InformationExtractor


class PipelineManager:

    def __init__(self):

        self.parser = ResumeParser()
        self.extractor = InformationExtractor()

    def process_resume(self, resume_path):

        text = self.parser.parse(resume_path)

        candidate = self.extractor.extract(text)

        return candidate