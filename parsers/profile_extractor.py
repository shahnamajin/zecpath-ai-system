import re


class ProfileExtractor:

    def extract(self, text):

        profile = {

            "summary": "",

            "location": "",

            "linkedin": "",

            "github": ""

        }

        lines = [line.strip() for line in text.split("\n") if line.strip()]

        profile["summary"] = " ".join(lines)

        return profile