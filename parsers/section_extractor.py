from config.section_headings import SECTION_HEADINGS


class SectionExtractor:

    def __init__(self):

        self.sections = [
            "HEADER",
            "PROFILE",
            "SKILLS",
            "EXPERIENCE",
            "EDUCATION",
            "PROJECTS",
            "CERTIFICATIONS",
            "LANGUAGES"
        ]

    def get_section_name(self, line):

        line = line.strip().upper()

        for section, headings in SECTION_HEADINGS.items():

            if line in headings:
                return section

        return None

    def extract(self, text):

        # Initialize all sections
        extracted = {}

        for section in self.sections:
            extracted[section] = ""

        lines = [
            line.strip()
            for line in text.split("\n")
            if line.strip()
        ]

        current_section = "HEADER"

        profile_started = False

        for line in lines:

            section = self.get_section_name(line)

            # ----------------------------
            # New Section Found
            # ----------------------------
            if section:

                current_section = section

                if section == "PROFILE":
                    profile_started = True

                continue

            # ----------------------------
            # If PROFILE heading is missing
            # ----------------------------
            if (
                current_section == "HEADER"
                and not profile_started
            ):

                # If another section starts later,
                # everything after HEADER becomes PROFILE.
                if (
                    len(extracted["HEADER"]) > 0
                    and (
                        "@"
                        not in line
                        and "linkedin" not in line.lower()
                        and "github" not in line.lower()
                    )
                ):

                    current_section = "PROFILE"
                    profile_started = True

            extracted[current_section] += line + "\n"

        # Remove trailing newlines
        for section in extracted:

            extracted[section] = extracted[section].strip()
        extracted = {
    key: value
    for key, value in extracted.items()
    if value
}

        return extracted