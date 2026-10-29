from .answer_understanding import AnswerUnderstandingEngine


def print_result(index, result, original_text, question_id):

    print(f"\nAnswer {index}")
    print("-" * 65)

    print(f"Question ID: {question_id}")

    print(f"Answer: {original_text}")

    print(
        f"Intent: "
        f"{result['answer']['intent']}"
    )

    print(
        f"Confidence: "
        f"{result['answer']['confidence_level']}"
    )

    print(
        f"Skills: "
        f"{result['entities']['skills']}"
    )

    print(
        f"Experience: "
        f"{result['entities']['experience']}"
    )

    print(
        f"Availability: "
        f"{result['entities']['availability']}"
    )

    print(
        f"Salary: "
        f"{result['entities']['salary_expectation']}"
    )

    print(
        f"Quality: "
        f"{result['quality']}"
    )


def main():

    print("=" * 65)
    print("ZECPath Answer Intent & Understanding Engine Demo")
    print("=" * 65)

    engine = AnswerUnderstandingEngine()

    test_answers = [

        {
            "question_id": "HR_SKILL_PY_001",
            "category": "skills",
            "text": (
                "I have used Python for data analysis, "
                "machine learning and Flask applications."
            ),
        },

        {
            "question_id": "HR_EXP_001",
            "category": "experience",
            "text": (
                "I completed a six month internship where "
                "I worked on a Python project."
            ),
        },

        {
            "question_id": "HR_SAL_001",
            "category": "salary_expectation",
            "text": (
                "I expect around 5 LPA."
            ),
        },

        {
            "question_id": "HR_NOTICE_001",
            "category": "availability",
            "text": (
                "I can join immediately."
            ),
        },

        {
            "question_id": "HR_NOTICE_002",
            "category": "availability",
            "text": (
                "I can join in 2 weeks."
            ),
        },

        {
            "question_id": "HR_EXP_002",
            "category": "experience",
            "text": (
                "I have two years of work experience."
            ),
        },

        {
            "question_id": "HR_EXP_003",
            "category": "experience",
            "text": "Yes.",
        },

        {
            "question_id": "HR_SKILL_001",
            "category": "skills",
            "text": (
                "I enjoy watching movies during weekends."
            ),
        },

        {
            "question_id": "HR_EXP_004",
            "category": "experience",
            "text": "",
        },
    ]

    for index, item in enumerate(
        test_answers,
        start=1
    ):

        result = engine.understand(
            candidate_id="CAND_1001",
            job_id="JOB_2001",
            question_id=item["question_id"],
            question_category=item["category"],
            text=item["text"],
            confidence_level=0.95,
        )

        print_result(
            index,
            result,
            item["text"],
            item["question_id"]
        )

    print("\n" + "=" * 65)
    print("Answer understanding completed successfully")
    print("=" * 65)


if __name__ == "__main__":
    main()