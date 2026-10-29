
"""Formats structured HR interview summaries for recruiter review."""

import json


class SummaryReportFormatter:
    def to_json(self, report):
        return json.dumps(report, indent=2)

    def to_text(self, report):
        c = report["candidate"]
        o = report["overall_performance"]
        i = report["insights"]

        lines = [
            "ZECPath AI - RECRUITER HR INTERVIEW SUMMARY",
            "=" * 55,
            f"Candidate ID : {c['candidate_id']}",
            f"Job Title    : {c['job_title']}",
            f"Session ID   : {c['session_id']}",
            "",
            "OVERALL PERFORMANCE",
            f"HR Score             : {o['hr_score']:.2f}/100",
            f"Aptitude / Logic     : {o['aptitude_logic_score']:.2f}/100",
            f"Communication        : {o['communication_score']:.2f}/100",
            f"Confidence           : {o['confidence_score']:.2f}/100",
            f"Consistency          : {o['consistency_score']:.2f}/100",
            f"Summary Score        : {o['summary_score']:.2f}/100",
            "",
            "STRENGTHS"
        ]

        lines += [f"- {x}" for x in i["strengths"]] or ["- None identified by the configured rules"]
        lines.append("")
        lines.append("WEAKNESSES")
        lines += [f"- {x}" for x in i["weaknesses"]] or ["- None identified by the configured rules"]
        lines.append("")
        lines.append("CULTURAL FIT INDICATORS")
        lines += [f"- {x}" for x in i["cultural_fit_indicators"]]
        lines.append("")
        lines.append("RISK FLAGS")
        lines += [f"- {x}" for x in i["risk_flags"]]
        lines.append("")
        lines.append("INCONSISTENCIES")
        lines += [f"- {x['question_id']}: {x['detail']}" for x in i["inconsistencies"]] or ["- None detected"]
        lines += ["", "NATURAL-LANGUAGE SUMMARY", report["natural_language_summary"]]
        return "\n".join(lines)
