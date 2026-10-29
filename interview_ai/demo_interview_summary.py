
"""Day 39 - Interview Summary Generator Demo."""

import json
from pathlib import Path

from interview_ai.interview_summary_generator import InterviewSummaryGenerator
from interview_ai.summary_report_formatter import SummaryReportFormatter


def main():
    path = (
        Path(__file__).resolve().parent.parent
        / "data" / "interview_summary" / "sample_interview_analysis.json"
    )

    with open(path, encoding="utf-8") as file:
        data = json.load(file)

    generator = InterviewSummaryGenerator()
    formatter = SummaryReportFormatter()

    report = generator.generate(data)

    print(formatter.to_text(report))

    output = (
        Path(__file__).resolve().parent.parent
        / "data" / "interview_summary" / "sample_hr_summary_report.json"
    )
    output.write_text(formatter.to_json(report), encoding="utf-8")

    print("\nReport Export :", output.name)
    print("\nINTERVIEW SUMMARY GENERATOR COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    main()
