import re


class HeaderExtractor:

    def extract(self, text):

        header = {
            "full_name": "",
            "email": "",
            "phone": "",
            "location": "",
            "linkedin": "",
            "github": ""
        }

        lines = [line.strip() for line in text.split("\n") if line.strip()]

        # ----------------------------
        # Name (First Line)
        # ----------------------------
        if lines:
            header["full_name"] = lines[0]

        # ----------------------------
        # Email
        # ----------------------------
        email = re.search(
            r'[\w\.-]+@[\w\.-]+\.\w+',
            text
        )

        if email:
            header["email"] = email.group()

        # ----------------------------
        # Phone Number
        # ----------------------------
        phone = re.search(
            r'(\+91[- ]?)?[6-9]\d{9}',
            text
        )

        if phone:
            header["phone"] = phone.group()

        # ----------------------------
        # LinkedIn
        # ----------------------------
        linkedin = re.search(
            r'(https?://)?(www\.)?linkedin\.com/[^\s]+',
            text,
            re.IGNORECASE
        )

        if linkedin:
            header["linkedin"] = linkedin.group()

        # ----------------------------
        # GitHub
        # ----------------------------
        github = re.search(
            r'(https?://)?(www\.)?github\.com/[^\s]+',
            text,
            re.IGNORECASE
        )

        if github:
            header["github"] = github.group()

        # ----------------------------
        # Location
        # ----------------------------
        if len(lines) >= 2:

            location = lines[1]

            # Remove phone if present
            location = re.sub(
                r'(\+91[- ]?)?[6-9]\d{9}',
                '',
                location
            )

            # Remove email if present
            location = re.sub(
                r'[\w\.-]+@[\w\.-]+\.\w+',
                '',
                location
            )

            location = location.replace("|", "").strip()

            header["location"] = location

        return header