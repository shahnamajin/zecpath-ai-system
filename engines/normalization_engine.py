import re


class NormalizationEngine:

    def normalize_text(self, text):

        # Convert to lowercase
        text = text.lower()

        # Remove extra spaces
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    def normalize_resume(self, resume):

        normalized = {}

        for key, value in resume.items():

            if isinstance(value, str):
                normalized[key] = self.normalize_text(value)

            else:
                normalized[key] = value

        return normalized