from parsers.pdf_reader import PDFReader
from parsers.docx_reader import DOCXReader
from parsers.layout_handler import LayoutHandler
from parsers.text_cleaner import TextCleaner


class ResumeParser:

    def __init__(self):
        self.pdf = PDFReader()
        self.docx = DOCXReader()
        self.layout = LayoutHandler()
        self.cleaner = TextCleaner()

    def parse(self, file_path):

        if file_path.endswith(".pdf"):
            text = self.pdf.extract_text(file_path)

        elif file_path.endswith(".docx"):
            text = self.docx.extract_text(file_path)

        else:
            raise Exception("Unsupported File")

        text = self.layout.normalize(text)
        text = self.cleaner.clean(text)

        return text