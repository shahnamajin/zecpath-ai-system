import os
import json

from parsers.section_extractor import SectionExtractor

extractor = SectionExtractor()

input_folder = "data/test_resumes"
output_folder = "data/labeled_resumes"

os.makedirs(output_folder, exist_ok=True)

for file in os.listdir(input_folder):

    path = os.path.join(input_folder, file)

    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    sections = extractor.extract(text)

    filename = os.path.splitext(file)[0] + ".json"

    output_path = os.path.join(output_folder, filename)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(sections, f, indent=4)

    print(filename, "saved")