import pytest

from hiring_ai.hiring_report_generator import HiringReportGenerator


@pytest.fixture
def generator(tmp_path):
    return HiringReportGenerator(output_dir=tmp_path)


@pytest.fixture
def candidate():
    return {
        "candidate_id": "CAND_1001",
        "candidate_name": "Sample Candidate",
        "job_id": "JOB_2001",
        "job_title": "Python Developer",
        "role_type": "technical",
        "evaluation_status": "completed"
    }


@pytest.fixture
def evaluations():
    return {
        "ats": {
            "score": 85,
            "strengths": ["Python skill alignment"],
            "weaknesses": ["Cloud skill gap"]
        },
        "screening": {"score": 80},
        "hr_interview": {"score": 90},
        "technical_interview": {"score": 88},
        "behavioral": {"flags": []},
        "integrity": {"flags": []},
        "final_decision": {
            "recommendation_label": "Selected",
            "hiring_fit_score": 87.4,
            "confidence_score": 85,
            "requires_human_review": False,
            "reasons": ["Score meets threshold"],
            "review_reasons": []
        }
    }


def test_report_contains_candidate_profile(generator, candidate, evaluations):
    report = generator.build_report(candidate, evaluations)

    assert report["candidate_profile"]["candidate_id"] == "CAND_1001"


def test_report_contains_all_evaluation_sections(generator, candidate, evaluations):
    report = generator.build_report(candidate, evaluations)

    assert set(report["evaluation_details"]) == {
        "ats",
        "screening",
        "hr_interview",
        "technical_interview",
        "behavioral",
        "integrity",
        "final_decision"
    }


def test_report_contains_strengths_and_weaknesses(generator, candidate, evaluations):
    report = generator.build_report(candidate, evaluations)

    assert "Python skill alignment" in report["candidate_assessment"]["strengths"]
    assert "Cloud skill gap" in report["candidate_assessment"]["weaknesses"]


def test_behavioral_flags_are_included(generator, candidate, evaluations):
    evaluations["behavioral"]["flags"] = [{
        "category": "behavior",
        "severity": "low",
        "status": "observed",
        "description": "Repeated gaze changes."
    }]

    report = generator.build_report(candidate, evaluations)

    assert len(report["candidate_assessment"]["risk_indicators"]) == 1


def test_markdown_report_is_generated(generator, candidate, evaluations):
    report = generator.build_report(candidate, evaluations)
    markdown = generator.to_markdown(report)

    assert "# Candidate Hiring Intelligence Report" in markdown
    assert "ATS Summary" in markdown
    assert "Final Recommendation Details" in markdown


def test_json_and_markdown_exports(generator, candidate, evaluations):
    report = generator.build_report(candidate, evaluations)
    files = generator.export_report(report, "test_candidate")

    assert files["json_path"].endswith(".json")
    assert files["markdown_path"].endswith(".md")


def test_missing_sections_are_identified(generator, candidate):
    report = generator.build_report(candidate, {})

    assert "ats" in report["evaluation_summary"]["missing_sections"]


def test_invalid_candidate_data_rejected(generator, evaluations):
    with pytest.raises(ValueError):
        generator.build_report("invalid", evaluations)