from .screening_scoring_engine import (
    ScreeningScoringEngine
)


def print_question_result(result):

    print("\n" + "-" * 70)

    print(
        f"Question ID: "
        f"{result['question_id']}"
    )

    print(
        f"Category: "
        f"{result['question_category']}"
    )

    scores = result["scores"]

    print(
        f"Clarity: "
        f"{scores['clarity']}/100"
    )

    print(
        f"Relevance: "
        f"{scores['relevance']}/100"
    )

    print(
        f"Completeness: "
        f"{scores['completeness']}/100"
    )

    print(
        f"Consistency: "
        f"{scores['consistency']}/100"
    )

    print(
        f"Question Score: "
        f"{scores['total_score']}/100"
    )

    print("Explanation:")

    for explanation in result["explanation"]:
        print(
            f"  - {explanation}"
        )


def main():

    print("=" * 70)
    print("ZECPath Screening Scoring Engine Demo")
    print("=" * 70)

    engine = ScreeningScoringEngine()

    candidate_id = "CAND_1001"
    job_id = "JOB_2001"

    answers = [

        {
            "question_id": "HR_SKILL_PY_001",
            "category": "skills",

            "data": {
                "answer": {
                    "raw_text": (
                        "I have experience with Python, "
                        "SQL and Flask for data analysis "
                        "and web application development."
                    ),
                    "intent": "skills",
                    "confidence_level": 0.95
                },

                "entities": {
                    "skills": [
                        "python",
                        "sql",
                        "flask"
                    ],
                    "experience": {
                        "years": None,
                        "types": []
                    },
                    "availability": {
                        "immediately_available": False,
                        "notice_period": None
                    },
                    "salary_expectation": {
                        "mentioned": False,
                        "values": []
                    }
                },

                "quality": {
                    "is_missing": False,
                    "is_vague": False,
                    "is_off_topic": False
                }
            }
        },

        {
            "question_id": "HR_EXP_001",
            "category": "experience",

            "data": {
                "answer": {
                    "raw_text": (
                        "I have two years of work experience."
                    ),
                    "intent": "experience",
                    "confidence_level": 0.95
                },

                "entities": {
                    "skills": [],
                    "experience": {
                        "years": 2.0,
                        "types": ["work"]
                    },
                    "availability": {
                        "immediately_available": False,
                        "notice_period": None
                    },
                    "salary_expectation": {
                        "mentioned": False,
                        "values": []
                    }
                },

                "quality": {
                    "is_missing": False,
                    "is_vague": False,
                    "is_off_topic": False
                }
            }
        },

        {
            "question_id": "HR_SAL_001",
            "category": "salary_expectation",

            "data": {
                "answer": {
                    "raw_text": (
                        "I expect around 5 LPA."
                    ),
                    "intent": "salary_expectation",
                    "confidence_level": 0.95
                },

                "entities": {
                    "skills": [],
                    "experience": {
                        "years": None,
                        "types": []
                    },
                    "availability": {
                        "immediately_available": False,
                        "notice_period": None
                    },
                    "salary_expectation": {
                        "mentioned": True,
                        "values": [
                            {
                                "value": 5.0,
                                "unit": "lpa"
                            }
                        ]
                    }
                },

                "quality": {
                    "is_missing": False,
                    "is_vague": False,
                    "is_off_topic": False
                }
            }
        },

        {
            "question_id": "HR_NOTICE_001",
            "category": "availability",

            "data": {
                "answer": {
                    "raw_text": (
                        "I can join in 2 weeks."
                    ),
                    "intent": "availability",
                    "confidence_level": 0.95
                },

                "entities": {
                    "skills": [],
                    "experience": {
                        "years": None,
                        "types": []
                    },
                    "availability": {
                        "immediately_available": False,
                        "notice_period": "2 weeks"
                    },
                    "salary_expectation": {
                        "mentioned": False,
                        "values": []
                    }
                },

                "quality": {
                    "is_missing": False,
                    "is_vague": False,
                    "is_off_topic": False
                }
            }
        },

        {
            "question_id": "HR_SKILL_002",
            "category": "skills",

            "data": {
                "answer": {
                    "raw_text": (
                        "I enjoy watching movies during weekends."
                    ),
                    "intent": "off_topic",
                    "confidence_level": 0.95
                },

                "entities": {
                    "skills": [],
                    "experience": {
                        "years": None,
                        "types": []
                    },
                    "availability": {
                        "immediately_available": False,
                        "notice_period": None
                    },
                    "salary_expectation": {
                        "mentioned": False,
                        "values": []
                    }
                },

                "quality": {
                    "is_missing": False,
                    "is_vague": False,
                    "is_off_topic": True
                }
            }
        },

        {
            "question_id": "HR_EXP_002",
            "category": "experience",

            "data": {
                "answer": {
                    "raw_text": "Yes.",
                    "intent": "vague",
                    "confidence_level": 0.95
                },

                "entities": {
                    "skills": [],
                    "experience": {
                        "years": None,
                        "types": []
                    },
                    "availability": {
                        "immediately_available": False,
                        "notice_period": None
                    },
                    "salary_expectation": {
                        "mentioned": False,
                        "values": []
                    }
                },

                "quality": {
                    "is_missing": False,
                    "is_vague": True,
                    "is_off_topic": False
                }
            }
        }
    ]

    results = []

    for item in answers:

        result = engine.score_question(
            candidate_id=candidate_id,
            job_id=job_id,
            question_id=item["question_id"],
            question_category=item["category"],
            answer_data=item["data"]
        )

        results.append(result)

        print_question_result(result)

    final_result = engine.calculate_final_score(
        candidate_id=candidate_id,
        job_id=job_id,
        question_results=results
    )

    print("\n" + "=" * 70)
    print("FINAL SCREENING SCORE")
    print("=" * 70)

    print(
        f"Total Questions: "
        f"{final_result['score_summary']['total_questions']}"
    )

    print(
        f"Average Score: "
        f"{final_result['score_summary']['average_score']}/100"
    )

    print(
        f"Final Screening Score: "
        f"{final_result['final_screening_score']}/100"
    )

    print("\nScreening scoring completed successfully.")


if __name__ == "__main__":
    main()