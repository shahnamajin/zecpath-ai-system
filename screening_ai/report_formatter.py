import json
from typing import Any, Dict


class ReportFormatter:
    """Formats screening reports for export."""

    @staticmethod
    def to_json(
        report: Dict[str, Any],
        indent: int = 2,
    ) -> str:
        """Convert report to JSON string."""

        return json.dumps(
            report,
            indent=indent,
            ensure_ascii=False,
        )

    @staticmethod
    def to_text(
        report: Dict[str, Any],
    ) -> str:
        """Convert report into a recruiter-friendly text format."""

        candidate = report.get(
            "candidate",
            {},
        )

        summary = report.get(
            "screening_summary",
            {},
        )

        highlighted = report.get(
            "highlighted_information",
            {},
        )

        # Safely format final score
        final_score = summary.get("final_score")

        if final_score is not None:
            final_score_text = f"{final_score}/100"
        else:
            final_score_text = "N/A"

        # Safely format skills
        skills = highlighted.get(
            "confirmed_skills",
            [],
        )

        skills_text = (
            ", ".join(skills)
            if skills
            else "None"
        )

        # Safely format salary
        salary = highlighted.get(
            "salary_expectation"
        )

        salary_text = (
            str(salary)
            if salary
            else "Not provided"
        )

        # Safely format availability
        availability = highlighted.get(
            "availability"
        )

        availability_text = (
            str(availability)
            if availability
            else "Not provided"
        )

        lines = [
            "ZECPath AI SCREENING REPORT",
            "=" * 32,

            f"Candidate: "
            f"{candidate.get('name') or 'N/A'}",

            f"Candidate ID: "
            f"{candidate.get('candidate_id') or 'N/A'}",

            f"Role: "
            f"{candidate.get('role') or 'N/A'}",

            f"Final Screening Score: "
            f"{final_score_text}",

            "",

            "HIGHLIGHTED INFORMATION",
            "-" * 28,

            f"Confirmed Skills: "
            f"{skills_text}",

            f"Salary Expectation: "
            f"{salary_text}",

            f"Availability: "
            f"{availability_text}",

            "",

            "KEY ANSWERS",
            "-" * 28,
        ]

        # Add key answers
        for answer in report.get(
            "key_answers",
            [],
        ):
            question_id = answer.get(
                "question_id",
                "Unknown",
            )

            answer_text = answer.get(
                "answer"
            ) or "[No answer]"

            lines.append(
                f"- [{question_id}] "
                f"{answer_text}"
            )

        # Strengths
        lines.extend(
            [
                "",
                "STRENGTHS",
                "-" * 28,
            ]
        )

        strengths = report.get(
            "strengths",
            [],
        )

        if strengths:
            for item in strengths:
                if isinstance(item, dict):
                    lines.append(
                        f"- {item.get('reason', str(item))}"
                    )
                else:
                    lines.append(
                        f"- {item}"
                    )
        else:
            lines.append(
                "- No strength indicators identified."
            )

        # Risks
        lines.extend(
            [
                "",
                "RISKS",
                "-" * 28,
            ]
        )

        risks = report.get(
            "risks",
            [],
        )

        if risks:
            for item in risks:

                if isinstance(item, str):
                    lines.append(
                        f"- {item}"
                    )

                elif isinstance(item, dict):
                    reason = item.get(
                        "reason",
                        "Risk",
                    )

                    details = item.get(
                        "details"
                    )

                    if details:
                        lines.append(
                            f"- {reason}: "
                            f"{details}"
                        )
                    else:
                        lines.append(
                            f"- {reason}"
                        )

        else:
            lines.append(
                "- No risk indicators identified."
            )

        # Missing data
        lines.extend(
            [
                "",
                "MISSING DATA",
                "-" * 28,
            ]
        )

        missing_data = report.get(
            "missing_data",
            [],
        )

        if missing_data:

            for item in missing_data:

                field = (
                    item.get("field")
                    or item.get("question_id")
                    or "Unknown"
                )

                reason = item.get(
                    "reason",
                    "Not provided",
                )

                lines.append(
                    f"- {field}: {reason}"
                )

        else:

            lines.append(
                "- No missing data identified."
            )

        # Recruiter summary
        lines.extend(
            [
                "",
                "RECRUITER SUMMARY",
                "-" * 28,

                report.get(
                    "recruiter_summary",
                    "No summary available.",
                ),

                "",
                "=" * 32,
            ]
        )

        return "\n".join(lines)