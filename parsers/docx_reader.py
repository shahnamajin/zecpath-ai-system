from docx import Document


class DOCXReader:

    def extract_text(self, file_path: str):

        doc = Document(file_path)

        text = ""

        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"

        return text