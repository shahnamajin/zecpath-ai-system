import json
from datetime import datetime, timezone
from pathlib import Path


class HiringReportGenerator:

    def __init__(self, output_dir="data/hiring_reports/output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _list(value):
        return value if isinstance(value, list) else []

    def build_report(self, candidate_data, evaluations):
        if not isinstance(candidate_data, dict):
            raise ValueError("candidate_data must be a dictionary.")

        if not isinstance(evaluations, dict):
            raise ValueError("evaluations must be a dictionary.")

        section_names = [
            "ats",
            "screening",
            "hr_interview",
            "technical_interview",
            "behavioral",
            "integrity",
            "final_decision"
        ]

        sections = {}

        for name in section_names:
            section = evaluations.get(name, {})
            if not isinstance(section, dict):
                raise ValueError(f"{name} must be a dictionary.")
            sections[name] = section

        decision = sections["final_decision"]

        strengths = []
        weaknesses = []

        for name in [
            "ats",
            "screening",
            "hr_interview",
            "technical_interview"
        ]:
            strengths.extend(self._list(sections[name].get("strengths")))
            weaknesses.extend(self._list(sections[name].get("weaknesses")))

        strengths.extend(self._list(evaluations.get("overall_strengths")))
        weaknesses.extend(self._list(evaluations.get("overall_weaknesses")))

        risks = (
            self._list(sections["behavioral"].get("flags"))
            + self._list(sections["integrity"].get("flags"))
        )

        missing_sections = [
            name for name, section in sections.items()
            if not section
        ]

        return {
            "report_metadata": {
                "report_type": "candidate_hiring_intelligence_report",
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "generator_version": "1.0"
            },
            "candidate_profile": {
                "candidate_id": candidate_data.get("candidate_id"),
                "candidate_name": candidate_data.get("candidate_name"),
                "job_id": candidate_data.get("job_id"),
                "job_title": candidate_data.get("job_title"),
                "role_type": candidate_data.get("role_type"),
                "evaluation_status": candidate_data.get("evaluation_status")
            },
            "evaluation_summary": {
                "hiring_fit_score": decision.get("hiring_fit_score"),
                "decision_confidence": decision.get("confidence_score"),
                "recommendation": decision.get("recommendation_label"),
                "decision_type": decision.get("decision_type"),
                "missing_sections": missing_sections
            },
            "evaluation_details": sections,
            "candidate_assessment": {
                "strengths": strengths,
                "weaknesses": weaknesses,
                "risk_indicators": risks
            },
            "recruiter_review": {
                "requires_human_review": decision.get(
                    "requires_human_review", True
                ),
                "review_reasons": self._list(
                    decision.get("review_reasons")
                ),
                "recommendation_reasons": self._list(
                    decision.get("reasons")
                ),
                "recruiter_notes": evaluations.get(
                    "recruiter_notes", "Not available"
                )
            },
            "disclaimer": (
                "This is an AI-assisted report. It does not replace "
                "human recruiter judgment. Behavioral observations are "
                "contextual signals and are not proof of personality, "
                "honesty, or competence."
            )
        }

    def to_markdown(self, report):
        candidate = report["candidate_profile"]
        summary = report["evaluation_summary"]
        details = report["evaluation_details"]
        assessment = report["candidate_assessment"]
        review = report["recruiter_review"]

        lines = [
            "# Candidate Hiring Intelligence Report",
            "",
            "## Candidate Profile",
            f"- Candidate: {candidate['candidate_name']}",
            f"- Candidate ID: {candidate['candidate_id']}",
            f"- Job ID: {candidate['job_id']}",
            f"- Position: {candidate['job_title']}",
            f"- Role: {candidate['role_type']}",
            "",
            "## Executive Summary",
            f"- Hiring Fit Score: {summary['hiring_fit_score']}",
            f"- Decision Confidence: {summary['decision_confidence']}",
            f"- Recommendation: {summary['recommendation']}",
            f"- Human Review Required: {review['requires_human_review']}",
            ""
        ]

        titles = {
            "ats": "ATS Summary",
            "screening": "Screening Results",
            "hr_interview": "HR Interview Insights",
            "technical_interview": "Technical Performance",
            "behavioral": "Behavioral Observations",
            "integrity": "Integrity Review",
            "final_decision": "Final Recommendation Details"
        }

        for key, title in titles.items():
            lines.extend(["## " + title, ""])
            section = details[key]

            if not section:
                lines.append("Not available.")
            else:
                for field, value in section.items():
                    lines.append(
                        f"- **{field.replace('_', ' ').title()}:** "
                        f"{json.dumps(value, ensure_ascii=False)}"
                    )

            lines.append("")

        lines.extend(["## Strengths", ""])
        lines.extend(
            [f"- {item}" for item in assessment["strengths"]]
            or ["- No explicit strengths supplied."]
        )

        lines.extend(["", "## Weaknesses", ""])
        lines.extend(
            [f"- {item}" for item in assessment["weaknesses"]]
            or ["- No explicit weaknesses supplied."]
        )

        lines.extend(["", "## Risk Indicators", ""])
        lines.extend(
            [f"- {item}" for item in assessment["risk_indicators"]]
            or ["- No risk indicators supplied."]
        )

        lines.extend(["", "## Recruiter Review", ""])
        lines.append(
            f"- Human review required: {review['requires_human_review']}"
        )

        for reason in review["review_reasons"]:
            lines.append(f"- {reason}")

        lines.extend([
            "",
            "## Important Notice",
            report["disclaimer"]
        ])

        return "\n".join(lines)

    def export_report(self, report, filename):
        safe_name = Path(filename).stem

        json_path = self.output_dir / f"{safe_name}.json"
        markdown_path = self.output_dir / f"{safe_name}.md"

        json_path.write_text(
            json.dumps(report, indent=4, ensure_ascii=False),
            encoding="utf-8"
        )

        markdown_path.write_text(
            self.to_markdown(report),
            encoding="utf-8"
        )

        return {
            "json_path": str(json_path),
            "markdown_path": str(markdown_path)
        }