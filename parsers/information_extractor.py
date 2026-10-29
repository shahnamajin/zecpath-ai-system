from datetime import datetime

from parsers.section_extractor import SectionExtractor
from parsers.header_extractor import HeaderExtractor
from parsers.profile_extractor import ProfileExtractor
from parsers.skill_extractor import SkillExtractor
from parsers.education_extractor import EducationExtractor
from parsers.experience_extractor import ExperienceExtractor
from parsers.project_extractor import ProjectExtractor
from parsers.certification_extractor import CertificationExtractor
from parsers.language_extractor import LanguageExtractor

from utils.id_generator import IDGenerator
from utils.logger import logger


class InformationExtractor:

    def __init__(self):

        self.section = SectionExtractor()
        self.header = HeaderExtractor()
        self.profile = ProfileExtractor()

        self.skill = SkillExtractor()
        self.education = EducationExtractor()
        self.experience = ExperienceExtractor()
        self.project = ProjectExtractor()
        self.certification = CertificationExtractor()
        self.language = LanguageExtractor()

    def extract(self, text):

        logger.info("Extracting candidate information...")

        # -----------------------------
        # Split Resume into Sections
        # -----------------------------
        sections = self.section.extract(text)

        # -----------------------------
        # Extract Header Information
        # -----------------------------
        header = self.header.extract(
            sections.get("HEADER", "")
        )

        # -----------------------------
        # Extract Profile
        # -----------------------------
        profile = self.profile.extract(
            sections.get("PROFILE", "")
        )

        # -----------------------------
        # Candidate JSON
        # -----------------------------
        candidate = {

            "candidate_id": IDGenerator.generate_candidate_id(),

            "created_at": datetime.now().isoformat(),

            "personal_information": {

                "full_name": header["full_name"],

                "email": header["email"],

                "phone": header["phone"],

                "location": header["location"],

                "linkedin": header["linkedin"],

                "github": header["github"]

            },

            "professional_summary": profile["summary"],

            "education": self.education.extract(
                sections.get("EDUCATION", "")
            ),

            "experience": self.experience.extract(
                sections.get("EXPERIENCE", "")
            ),

            "skills": self.skill.extract(
                sections.get("SKILLS", "")
            ),

            "projects": self.project.extract(
                sections.get("PROJECTS", "")
            ),

            "certifications": self.certification.extract(
                sections.get("CERTIFICATIONS", "")
            ),

            "languages": self.language.extract(
                sections.get("LANGUAGES", "")
            )

        }

        logger.success(
            "Candidate information extracted successfully."
        )

        return candidate