import re


class ResumeCleaner:

    def clean(self, text):

        if not text:
            return ""

        # Replace punctuation that is not useful
        text = re.sub(
            r"[^\w\s@.+#/-]",
            " ",
            text
        )

        # Remove repeated # characters
        text = re.sub(
            r"#{2,}",
            " ",
            text
        )

        # Normalize multiple spaces
        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()