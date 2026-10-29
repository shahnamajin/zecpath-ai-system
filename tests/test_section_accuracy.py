import os

from parsers.section_extractor import SectionExtractor

extractor = SectionExtractor()

folder = "data/test_resumes"

for file in os.listdir(folder):

    path = os.path.join(folder, file)

    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    sections = extractor.extract(text)

    print("=" * 60)
    print(file)

    for key in sections:
        print(key)