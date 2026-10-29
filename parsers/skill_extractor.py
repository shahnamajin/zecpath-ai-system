import re

from config.skills_dictionary import (
    TECHNICAL_SKILLS,
    SOFT_SKILLS,
    SKILL_SYNONYMS,
    SKILL_STACKS
)


class SkillExtractor:

    def __init__(self):
        pass

    # -----------------------------
    # Normalize Skill
    # -----------------------------
    def normalize(self, skill):

        skill = skill.strip()

        # Remove "(Basic)"
        skill = re.sub(r"\(.*?\)", "", skill).strip()

        return skill

    # -----------------------------
    # Search Whole Word
    # -----------------------------
    def contains(self, text, word):

        pattern = r"\b" + re.escape(word) + r"\b"

        return re.search(
            pattern,
            text,
            re.IGNORECASE
        ) is not None

    # -----------------------------
    # Extract Skills
    # -----------------------------
    def extract(self, text):

        result = {}

        # -----------------------------------
        # Technical Skills
        # -----------------------------------

        for category, skills in TECHNICAL_SKILLS.items():

            found = {}

            # -------------------------
            # Exact Match
            # -------------------------

            for skill in skills:

                if self.contains(text, skill):

                    found[skill] = 1.0

            # -------------------------
            # Synonym Match
            # -------------------------

            for synonym, original in SKILL_SYNONYMS.items():

                if original not in skills:
                    continue

                if self.contains(text, synonym):

                    if original not in found:

                        found[original] = 0.90

            # -------------------------
            # Skill Stack
            # -------------------------

            for stack, stack_skills in SKILL_STACKS.items():

                if self.contains(text, stack):

                    for stack_skill in stack_skills:

                        if stack_skill in skills:

                            if stack_skill not in found:

                                found[stack_skill] = 0.85

            # -------------------------
            # Store Category
            # -------------------------

            result[category] = []

            for skill in sorted(found.keys()):

                result[category].append({

                    "skill": self.normalize(skill),

                    "confidence": found[skill]

                })

        # -----------------------------------
        # Soft Skills
        # -----------------------------------

        result["Soft Skills"] = []

        found_soft = {}

        for skill in SOFT_SKILLS:

            if self.contains(text, skill):

                found_soft[skill] = 1.0

        for skill in sorted(found_soft.keys()):

            result["Soft Skills"].append({

                "skill": skill,

                "confidence": found_soft[skill]

            })

        return result