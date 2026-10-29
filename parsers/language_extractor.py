import re


class LanguageExtractor:

    def extract(self, text):

        languages = []

        matches = re.findall(r'([A-Za-z]+)\s*\((.*?)\)', text)

        for language, level in matches:

            languages.append({
                "language": language.strip(),
                "level": level.strip()
            })

        return languages