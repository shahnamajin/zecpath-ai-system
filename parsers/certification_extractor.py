import re

from config.certification_categories import CERTIFICATION_CATEGORIES


class CertificationExtractor:

    def extract(self, text):

        certifications = []

        if not text.strip():
            return certifications

        lines = [line.strip() for line in text.split("\n") if line.strip()]

        for line in lines:

            if "certified" in line.lower() or "simulation" in line.lower():

                category = "Other"
                lower_line = line.lower()

                for keyword, value in CERTIFICATION_CATEGORIES.items():

                    if keyword in lower_line:
                        category = value
                        break

                date_match = re.search(
                    r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec).*?\d{4}",
                    line
                )

                date = date_match.group() if date_match else ""

                certifications.append({

                    "name": line,

                    "category": category,

                    "date": date

                })

        return certifications