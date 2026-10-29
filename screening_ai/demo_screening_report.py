from .screening_report_builder import ScreeningReportBuilder
from .report_formatter import ReportFormatter


def main():

    candidate = {
        "candidate_id": "CAND_1001",
        "name": "Sample Candidate",
        "job_id": "JOB_2001",
        "role": "Python Developer",
    }

    answers = [

        {
            "question_id": "HR_SKILL_PY_001",

            "answer": {
                "intent": "skills",
                "raw_text":
                    "I use Python, Flask, SQL and machine learning.",
            },

            "entities": {
                "skills": [
                    "Python",
                    "Flask",
                    "SQL",
                    "Machine Learning",
                ]
            },
        },

        {
            "question_id": "HR_EXP_001",

            "answer": {
                "intent": "experience",
                "raw_text":
                    "I have two years of Python development experience.",
            },

            "entities": {
                "skills": ["Python"],

                "experience": {
                    "years": 2.0,
                    "types": ["work"],
                },
            },
        },

        {
            "question_id": "HR_SAL_001",

            "answer": {
                "intent": "salary_expectation",
                "raw_text":
                    "I expect around 5 LPA.",
            },

            "entities": {
                "salary_expectation": {
                    "mentioned": True,

                    "values": [
                        {
                            "value": 5.0,
                            "unit": "lpa",
                        }
                    ],
                }
            },
        },

        {
            "question_id": "HR_NOTICE_001",

            "answer": {
                "intent": "availability",
                "raw_text":
                    "I can join in two weeks.",
            },

            "entities": {
                "availability": "2 weeks",
            },
        },

        {
            "question_id": "HR_SKILL_002",

            "answer": {
                "intent": "off_topic",
                "raw_text":
                    "I enjoy watching movies.",
            },

            "quality": {
                "is_off_topic": True,
            },
        },
    ]

    screening = {
        "final_screening_score": 72.92,
        "total_questions": 5,
    }

    behavioral = {

        "communication_signals": {
            "communication_strength": 80.0,
        },

        "sentiment": {
            "sentiment": "positive",
            "score": 100.0,
        },

        "contradiction": {
            "detected": False,
            "details": [],
        },
    }

    builder = ScreeningReportBuilder()

    report = builder.build(
        candidate,
        answers,
        screening,
        behavioral,
        "RPT_20261001_001",
    )

    print("=" * 70)
    print("ZECPath AI Screening Report Generator Demo")
    print("=" * 70)

    print(
        ReportFormatter.to_text(report)
    )

    print("\n" + "=" * 70)
    print("JSON EXPORT")
    print("=" * 70)

    print(
        ReportFormatter.to_json(report)
    )

    print("=" * 70)

    print(
        "AI screening report generation completed successfully."
    )

    print("=" * 70)


if __name__ == "__main__":
    main()