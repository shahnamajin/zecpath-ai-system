import re


class AnswerExtractor:
    """
    Extracts structured information from candidate answers.
    """

    SKILL_PATTERNS = [
        "python",
        "java",
        "sql",
        "javascript",
        "react",
        "flask",
        "streamlit",
        "docker",
        "git",
        "aws",
        "azure",
        "gcp",
        "machine learning",
        "data analysis",
        "pandas",
        "numpy",
        "html",
        "css",
        "spring",
        "node",
        "node.js",
        "flutter",
    ]

    NUMBER_WORDS = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
    }

    def extract_skills(self, text):
        """
        Extract technical skills mentioned in the answer.
        """

        if not text:
            return []

        text_lower = text.lower()

        skills = []

        for skill in self.SKILL_PATTERNS:

            if skill in text_lower:
                skills.append(skill)

        return skills

    def extract_experience(self, text):
        """
        Extract work experience information.

        Supports:
        - 2 years
        - 2.5 years
        - two years
        - internship
        - projects
        - work experience
        """

        if not text:
            return {
                "years": None,
                "types": []
            }

        text_lower = text.lower()

        years = None

        # Numeric format:
        # 2 years
        # 2.5 years
        numeric_match = re.search(
            r"(\d+(?:\.\d+)?)\s*(?:years?|yrs?)",
            text_lower
        )

        if numeric_match:

            years = float(
                numeric_match.group(1)
            )

        else:

            # Written format:
            # two years
            word_pattern = (
                r"\b("
                + "|".join(self.NUMBER_WORDS.keys())
                + r")\s*(?:years?|yrs?)"
            )

            word_match = re.search(
                word_pattern,
                text_lower
            )

            if word_match:

                years = float(
                    self.NUMBER_WORDS[
                        word_match.group(1)
                    ]
                )

        experience_type = []

        if (
            "internship" in text_lower
            or "intern" in text_lower
        ):
            experience_type.append("internship")

        if "project" in text_lower:
            experience_type.append("project")

        if (
            "work" in text_lower
            or "worked" in text_lower
            or "experience" in text_lower
        ):
            experience_type.append("work")

        return {
            "years": years,
            "types": experience_type
        }

    def extract_availability(self, text):
        """
        Extract joining and notice-period information.
        """

        if not text:
            return {
                "immediately_available": False,
                "notice_period": None
            }

        text_lower = text.lower()

        immediate = (
            "immediately" in text_lower
            or "immediate" in text_lower
        )

        notice_period = None

        match = re.search(
            r"(\d+)\s*"
            r"(day|days|week|weeks|month|months)",
            text_lower
        )

        if match:

            number = match.group(1)
            unit = match.group(2)

            number_value = int(number)

            # Singular/plural normalization
            if number_value == 1:

                if unit.endswith("s"):
                    unit = unit[:-1]

            else:

                if not unit.endswith("s"):
                    unit += "s"

            notice_period = (
                f"{number} {unit}"
            )

        return {
            "immediately_available": immediate,
            "notice_period": notice_period
        }

    def extract_salary(self, text):
        """
        Extract salary-related numerical information.

        Examples:
        - 5 LPA
        - 6.5 LPA
        - 5 lakhs
        - ₹50000
        """

        if not text:
            return {
                "mentioned": False,
                "values": []
            }

        text_lower = text.lower()

        amounts = re.findall(
            r"(?:₹|rs\.?|inr)?\s*"
            r"(\d+(?:\.\d+)?)\s*"
            r"(lpa|lakhs?|lakh|k)?",
            text_lower
        )

        values = []

        for amount, unit in amounts:

            values.append({
                "value": float(amount),
                "unit": unit or "unspecified"
            })

        # Remove meaningless numerical matches
        salary_keywords = [
            "salary",
            "lpa",
            "lakhs",
            "lakh",
            "compensation",
            "package",
            "pay",
        ]

        if not any(
            keyword in text_lower
            for keyword in salary_keywords
        ):
            values = []

        return {
            "mentioned": len(values) > 0,
            "values": values
        }