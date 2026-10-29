import os
import json

from parsers.section_extractor import SectionExtractor


INPUT_FOLDER = "data/test_resumes"
OUTPUT_FOLDER = "data/labeled_resumes"
REPORT_FILE = "docs/section_accuracy.md"


def count_detected_sections(sections):
    """
    Count sections that actually contain data.
    """

    detected = 0

    for value in sections.values():

        if isinstance(value, str):

            if value.strip():
                detected += 1

        elif isinstance(value, list):

            if len(value) > 0:
                detected += 1

        elif isinstance(value, dict):

            if len(value) > 0:
                detected += 1

    return detected


def count_expected_sections(text):
    """
    Count the expected sections present in the resume.
    """

    expected_headings = {

        "HEADER",

        "PROFILE",

        "SUMMARY",

        "PROFESSIONAL SUMMARY",

        "OBJECTIVE",

        "SKILLS",

        "TECHNICAL SKILLS",

        "CORE SKILLS",

        "EXPERIENCE",

        "WORK EXPERIENCE",

        "EMPLOYMENT HISTORY",

        "EDUCATION",

        "PROJECTS",

        "CERTIFICATIONS",

        "CERTIFICATES",

        "LANGUAGES"

    }

    text = text.upper()

    count = 0

    for heading in expected_headings:

        if heading in text:
            count += 1

    return count


def main():

    extractor = SectionExtractor()

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    os.makedirs("docs", exist_ok=True)

    report = []

    files = sorted(os.listdir(INPUT_FOLDER))

    print("=" * 60)
    print("DAY 8 - RESUME SECTION SEGMENTATION")
    print("=" * 60)

    for file in files:

        if not file.endswith(".txt"):
            continue

        path = os.path.join(INPUT_FOLDER, file)

        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        sections = extractor.extract(text)

        # ----------------------------
        # Save JSON
        # ----------------------------

        json_name = os.path.splitext(file)[0] + ".json"

        json_path = os.path.join(
            OUTPUT_FOLDER,
            json_name
        )

        with open(
            json_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                sections,
                f,
                indent=4,
                ensure_ascii=False
            )

        # ----------------------------
        # Accuracy
        # ----------------------------

        detected = count_detected_sections(sections)

        expected = count_expected_sections(text)

        if expected == 0:
            expected = detected

        accuracy = round(
            (detected / expected) * 100,
            2
        )

        # Accuracy cannot exceed 100%

        accuracy = min(accuracy, 100)

        report.append({

            "resume": file,

            "expected": expected,

            "detected": detected,

            "accuracy": accuracy

        })

        print(file)

        print("Expected :", expected)

        print("Detected :", detected)

        print("Accuracy :", accuracy, "%")

        print("-" * 50)

    # ----------------------------
    # Create Markdown Report
    # ----------------------------

    with open(
        REPORT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        f.write("# Resume Section Detection Accuracy Report\n\n")

        f.write("| Resume | Expected | Detected | Accuracy |\n")

        f.write("|--------|---------:|---------:|---------:|\n")

        total = 0

        for row in report:

            total += row["accuracy"]

            f.write(
                f"| {row['resume']} | "
                f"{row['expected']} | "
                f"{row['detected']} | "
                f"{row['accuracy']}% |\n"
            )

        average = round(total / len(report), 2)

        f.write("\n")

        f.write(f"## Average Accuracy\n\n")

        f.write(f"{average}%\n")

    print("\n")
    print("=" * 60)
    print("Day 8 Completed Successfully")
    print("=" * 60)
    print("JSON files saved to:", OUTPUT_FOLDER)
    print("Accuracy report:", REPORT_FILE)


if __name__ == "__main__":
    main()