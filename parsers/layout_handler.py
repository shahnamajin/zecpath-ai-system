class LayoutHandler:

    def normalize(self, text: str):

        text = text.replace("\t", " ")
        text = text.replace("\r", "")

        while "  " in text:
            text = text.replace("  ", " ")

        return text.strip()