
import json
from pathlib import Path

from interview_ai.interview_summary_generator import InterviewSummaryGenerator
from interview_ai.summary_report_formatter import SummaryReportFormatter


def load_data():
    path = (
        Path(__file__).resolve().parent.parent
        / "data" / "interview_summary" / "sample_interview_analysis.json"
    )
    with open(path, encoding="utf-8") as file:
        return json.load(file)


def test_summary_contains_candidate():
    report = InterviewSummaryGenerator().generate(load_data())
    assert report["candidate"]["candidate_id"] == "CAND_1001"


def test_strengths_are_generated():
    report = InterviewSummaryGenerator().generate(load_data())
    assert len(report["insights"]["strengths"]) > 0


def test_weaknesses_field_exists():
    report = InterviewSummaryGenerator().generate(load_data())
    assert "weaknesses" in report["insights"]


def test_cultural_fit_indicators_are_generated():
    report = InterviewSummaryGenerator().generate(load_data())
    assert len(report["insights"]["cultural_fit_indicators"]) > 0


def test_inconsistency_is_highlighted():
    report = InterviewSummaryGenerator().generate(load_data())
    assert len(report["insights"]["inconsistencies"]) == 1


def test_risk_flags_are_generated():
    report = InterviewSummaryGenerator().generate(load_data())
    assert len(report["insights"]["risk_flags"]) > 0


def test_overall_score_range():
    report = InterviewSummaryGenerator().generate(load_data())
    score = report["overall_performance"]["summary_score"]
    assert 0 <= score <= 100


def test_natural_language_summary_exists():
    report = InterviewSummaryGenerator().generate(load_data())
    assert len(report["natural_language_summary"]) > 50


def test_json_formatter():
    report = InterviewSummaryGenerator().generate(load_data())
    text = SummaryReportFormatter().to_json(report)
    assert "CAND_1001" in text
    assert "natural_language_summary" in text


def test_text_formatter():
    report = InterviewSummaryGenerator().generate(load_data())
    text = SummaryReportFormatter().to_text(report)
    assert "STRENGTHS" in text
    assert "RISK FLAGS" in text
    assert "INCONSISTENCIES" in text


def test_score_is_normalized():
    data = load_data()
    data["hr_score"] = 150
    report = InterviewSummaryGenerator().generate(data)
    assert report["overall_performance"]["hr_score"] == 100.0
