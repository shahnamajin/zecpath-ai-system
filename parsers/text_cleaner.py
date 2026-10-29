import re


class TextCleaner:

    def clean(self, text: str) -> str:
        # Remove tabs
        text = text.replace("\t", " ")

        # Remove extra spaces (but keep newlines)
        text = re.sub(r"[ ]+", " ", text)

        # Remove extra blank lines
        text = re.sub(r"\n\s*\n+", "\n\n", text)

        return text.strip()