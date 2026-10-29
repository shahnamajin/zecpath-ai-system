import re


class EducationExtractor:

    def extract(self, text):

        education = []

        if not text.strip():
            return education

        lines = [line.strip() for line in text.split("\n") if line.strip()]

        i = 0

        while i < len(lines):

            line = lines[i]

            degree_match = re.search(
                r"(Bachelor|Master|BCA|MCA|B\.Tech|M\.Tech|BSc|MSc).*",
                line,
                re.IGNORECASE
            )

            if degree_match:

                degree = line
                institution = ""
                graduation_year = ""
                field_of_study = ""

                year_match = re.search(
                    r"(\d{4})\s*[–-]\s*(Present|\d{4})",
                    line
                )

                if year_match:
                    graduation_year = year_match.group(2)

                field_match = re.search(
                    r"\((.*?)\)",
                    line
                )

                if field_match:
                    field_of_study = field_match.group(1)

                if i + 1 < len(lines):
                    institution = lines[i + 1]

                education.append({

                    "degree_type": degree.split("(")[0].strip(),

                    "field_of_study": field_of_study,

                    "institution": institution,

                    "graduation_year": graduation_year

                })

            i += 1

        return education