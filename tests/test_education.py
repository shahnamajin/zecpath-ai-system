from pprint import pprint

from parsers.education_extractor import EducationExtractor
from parsers.certification_extractor import CertificationExtractor

sample_text = """
Master of Computer Applications (MCA) – Pursuing 2025 – Present
LEAD College of Management (Autonomous), Palakkad

Bachelor of Computer Applications (BCA) 2022 – 2025
Malabar College of Advanced Studies, Vengara, Malappuram

GenAI Powered Data Analytics Job Simulation – Tata (Forage) Jan 2026
Android App Development using Flutter – NASSCOM Certified (36 hrs) 12 Jan – 16 Jan 2026
Web Development using React JS – NASSCOM Certified (36 hrs) 31 Jan – 04 Feb 2026
"""

print("\nEducation:\n")
pprint(EducationExtractor().extract(sample_text))

print("\nCertifications:\n")
pprint(CertificationExtractor().extract(sample_text))