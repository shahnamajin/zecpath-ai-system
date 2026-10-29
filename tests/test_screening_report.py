from screening_ai.screening_report_builder import (
    ScreeningReportBuilder,
)

from screening_ai.report_formatter import (
    ReportFormatter,
)


def sample_data():

    candidate = {
        "candidate_id": "C1",
        "name": "Test Candidate",
        "job_id": "J1",
        "role": "Python Developer",
    }

    answers = [

        {
            "question_id": "Q1",

            "answer": {
                "intent": "skills",
                "raw_text":
                    "I know Python and SQL.",
            },

            "entities": {
                "skills": [
                    "Python",
                    "SQL",
                ]
            },
        },

        {
            "question_id": "Q2",

            "answer": {
                "intent": "salary_expectation",
                "raw_text": "5 LPA",
            },

            "entities": {
                "salary_expectation": {
                    "mentioned": True,

                    "values": [
                        {
                            "value": 5,
                            "unit": "lpa",
                        }
                    ],
                }
            },
        },

        {
            "question_id": "Q3",

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
            "question_id": "Q4",

            "answer": {
                "intent": "vague",
                "raw_text": "Maybe.",
            },

            "quality": {
                "is_vague": True,
            },
        },

        {
            "question_id": "Q5",

            "answer": {
                "intent": "missing",
                "raw_text": "",
            },

            "quality": {
                "is_missing": True,
            },
        },
    ]

    screening = {
        "final_screening_score": 72.92,
        "total_questions": 5,
    }

    behavioral = {

        "communication_signals": {
            "communication_strength": 80,
        },

        "sentiment": {
            "sentiment": "positive",
            "score": 100,
        },

        "contradiction": {
            "detected": False,
            "details": [],
        },
    }

    return (
        candidate,
        answers,
        screening,
        behavioral,
    )


def test_report_contains_candidate():

    c, a, s, b = sample_data()

    report = ScreeningReportBuilder().build(
        c, a, s, b
    )

    assert (
        report["candidate"]["candidate_id"]
        == "C1"
    )


def test_report_extracts_score():

    c, a, s, b = sample_data()

    report = ScreeningReportBuilder().build(
        c, a, s, b
    )

    assert (
        report["screening_summary"]["final_score"]
        == 72.92
    )


def test_report_highlights_information():

    c, a, s, b = sample_data()

    report = ScreeningReportBuilder().build(
        c, a, s, b
    )

    highlighted = report[
        "highlighted_information"
    ]

    assert highlighted[
        "confirmed_skills"
    ] == [
        "Python",
        "SQL",
    ]

    assert (
        highlighted[
            "salary_expectation"
        ]["values"][0]["value"]
        == 5
    )

    assert (
        highlighted["availability"]
        == "2 weeks"
    )


def test_report_identifies_risks():

    c, a, s, b = sample_data()

    report = ScreeningReportBuilder().build(
        c, a, s, b
    )

    assert any(
        "Vague" in str(item)
        for item in report["risks"]
    )


def test_report_identifies_missing_data():

    c, a, s, b = sample_data()

    report = ScreeningReportBuilder().build(
        c, a, s, b
    )

    assert any(
        item.get("question_id") == "Q5"
        for item in report["missing_data"]
    )


def test_report_contains_key_answers():

    c, a, s, b = sample_data()

    report = ScreeningReportBuilder().build(
        c, a, s, b
    )

    assert len(
        report["key_answers"]
    ) == 5


def test_positive_behavioral_signal():

    c, a, s, b = sample_data()

    report = ScreeningReportBuilder().build(
        c, a, s, b
    )

    assert any(
        "Positive sentiment"
        in str(item)
        for item in report["strengths"]
    )


def test_json_export():

    c, a, s, b = sample_data()

    report = ScreeningReportBuilder().build(
        c, a, s, b
    )

    output = ReportFormatter.to_json(
        report
    )

    assert '"candidate"' in output

    assert (
        '"highlighted_information"'
        in output
    )


def test_text_export():

    c, a, s, b = sample_data()

    report = ScreeningReportBuilder().build(
        c, a, s, b
    )

    output = ReportFormatter.to_text(
        report
    )

    assert (
        "ZECPath AI SCREENING REPORT"
        in output
    )

    assert (
        "Salary Expectation"
        in output
    )

    assert (
        "Availability"
        in output
    )


def test_empty_answers():

    report = ScreeningReportBuilder().build(

        {
            "candidate_id": "C2"
        },

        [],

        {
            "final_screening_score": 0,
            "total_questions": 0,
        },

        {},
    )

    assert (
        report["key_answers"] == []
    )

    assert (
        report[
            "highlighted_information"
        ]["confirmed_skills"]
        == []
    )

    assert len(
        report["missing_data"]
    ) >= 3