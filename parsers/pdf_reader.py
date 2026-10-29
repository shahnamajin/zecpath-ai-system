import pdfplumber


class PDFReader:
    def extract_text(self, file_path: str) -> str:
        text = ""

        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()

                if extracted:
                    text += extracted + "\n"

        return text