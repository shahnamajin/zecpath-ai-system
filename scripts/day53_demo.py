import sys
from pathlib import Path
from pprint import pprint

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from hiring_ai.hiring_report_generator import HiringReportGenerator


def main():
    generator = HiringReportGenerator()

    candidate_data = {
        "candidate_id": "CAND_1001",
        "candidate_name": "Sample Candidate",
        "job_id": "JOB_2001",
        "job_title": "Python Developer",
        "role_type": "technical",
        "evaluation_status": "completed"
    }

    evaluations = {
        "ats": {
            "score": 85,
            "matched_skills": ["Python", "SQL", "Pandas"],
            "missing_skills": ["AWS"],
            "strengths": ["Strong Python skill alignment"],
            "weaknesses": ["Cloud skill gap"]
        },
        "screening": {
            "score": 80,
            "status": "completed",
            "summary": "Candidate completed HR screening.",
            "strengths": ["Relevant responses"],
            "weaknesses": ["Some answers need further clarification"]
        },
        "hr_interview": {
            "score": 90,
            "summary": "Strong communication and relevant experience.",
            "strengths": ["Clear communication"],
            "weaknesses": []
        },
        "technical_interview": {
            "score": 88,
            "summary": "Good technical understanding.",
            "skill_ratings": {
                "Python": 4,
                "SQL": 3,
                "Problem Solving": 4
            },
            "strengths": ["Strong problem-solving"],
            "weaknesses": ["SQL depth can be improved"]
        },
        "behavioral": {
            "flags": [
                {
                    "category": "behavior",
                    "severity": "low",
                    "status": "observed",
                    "description": "Repeated gaze changes during the session."
                }
            ]
        },
        "integrity": {
            "flags": []
        },
        "final_decision": {
            "recommendation": "selected",
            "recommendation_label": "Selected",
            "hiring_fit_score": 87.30,
            "confidence_score": 87.30,
            "requires_human_review": False,
            "reasons": [
                "Hiring Fit Score meets the selection threshold."
            ],
            "review_reasons": [],
            "decision_type": "AI recommendation"
        },
        "overall_strengths": [
            "Good alignment with the technical role",
            "Strong problem-solving ability"
        ],
        "overall_weaknesses": [
            "Cloud experience needs improvement"
        ],
        "recruiter_notes": "Review technical project experience during final discussion."
    }

    report = generator.build_report(
        candidate_data,
        evaluations
    )

    exported = generator.export_report(
        report,
        "CAND_1001_hiring_report"
    )

    print("\n========== DAY 53: HIRING INTELLIGENCE REPORT ==========")
    print("\nCandidate:", candidate_data["candidate_name"])
    print("Recommendation:", report["evaluation_summary"]["recommendation"])
    print("Hiring Fit:", report["evaluation_summary"]["hiring_fit_score"])
    print("\nExported files:")
    pprint(exported)


if __name__ == "__main__":
    main()