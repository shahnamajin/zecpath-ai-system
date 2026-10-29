import re


class ExperienceExtractor:

    def __init__(self):
        pass

    def extract(self, text):

        experiences = []

        if not text.strip():
            return experiences

        lines = [
            line.strip()
            for line in text.split("\n")
            if line.strip()
        ]

        i = 0

        while i < len(lines):

            line = lines[i]

            # -----------------------------------------
            # Match:
            # Software Engineer - Infosys
            # Senior Software Engineer - Paytm Labs (2022 - Present)
            # -----------------------------------------

            match = re.match(
                r"^(.+?)\s+[-–]\s+(.+)$",
                line
            )

            if not match:
                i += 1
                continue

            designation = match.group(1).strip()

            company_text = match.group(2).strip()

            company = company_text

            start_date = ""
            end_date = ""
            duration = ""

            responsibilities = []

            # -----------------------------------------
            # Extract date from same line
            # Example:
            # Paytm Labs (2022 - Present)
            # -----------------------------------------

            date_match = re.search(
                r"\((\d{4})\s*[-–]\s*(Present|\d{4})\)",
                company_text
            )

            if date_match:

                start_date = date_match.group(1)

                end_date = date_match.group(2)

                duration = f"{start_date} - {end_date}"

                company = re.sub(
                    r"\(\d{4}\s*[-–]\s*(Present|\d{4})\)",
                    "",
                    company_text
                ).strip()

            # -----------------------------------------
            # If no date found,
            # check next line
            # -----------------------------------------

            elif i + 1 < len(lines):

                date_line = lines[i + 1]

                date_match = re.search(

                    r"([A-Za-z]{3,9}\s+\d{4}|\d{4})"

                    r"\s*[-–]\s*"

                    r"(Present|[A-Za-z]{3,9}\s+\d{4}|\d{4})",

                    date_line

                )

                if date_match:

                    start_date = date_match.group(1)

                    end_date = date_match.group(2)

                    duration = f"{start_date} - {end_date}"

                    i += 1

            # -----------------------------------------
            # Collect bullet responsibilities
            # -----------------------------------------

            j = i + 1

            while j < len(lines):

                current = lines[j]

                # Next job starts
                if re.match(
                    r"^(.+?)\s+[-–]\s+(.+)$",
                    current
                ):
                    break

                if current.startswith("•"):

                    responsibilities.append(

                        current.lstrip("•").strip()

                    )

                elif current.startswith("-"):

                    responsibilities.append(

                        current.lstrip("-").strip()

                    )

                j += 1

            experiences.append(

                {

                    "designation": designation,

                    "company": company,

                    "employment_type": "",

                    "location": "",

                    "start_date": start_date,

                    "end_date": end_date,

                    "duration": duration,

                    "responsibilities": responsibilities

                }

            )

            i = j

        return experiences