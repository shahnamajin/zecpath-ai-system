
from interview_ai.hr_interview_simulator import HRInterviewSimulator


def test_sessions_load():
    simulator = HRInterviewSimulator()
    assert len(simulator.sessions) == 8


def test_all_candidate_types_present():
    simulator = HRInterviewSimulator()
    types = {session["candidate_type"] for session in simulator.sessions}
    assert {"confident", "hesitant", "inexperienced", "overqualified"} <= types


def test_simulation_count():
    simulator = HRInterviewSimulator()
    assert len(simulator.run_all()) == 8


def test_ai_score_range():
    simulator = HRInterviewSimulator()
    for result in simulator.run_all():
        assert 0 <= result["ai_score"] <= 100


def test_ai_decision_values():
    simulator = HRInterviewSimulator()
    assert simulator.ai_decision(90) == "continue"
    assert simulator.ai_decision(70) == "clarify"
    assert simulator.ai_decision(50) == "review"


def test_manual_comparison_fields():
    simulator = HRInterviewSimulator()
    results = simulator.compare_manual_evaluation()
    assert len(results) == 8
    assert all("manual_score" in x for x in results)
    assert all("score_difference" in x for x in results)


def test_accuracy_is_normalized():
    metrics = HRInterviewSimulator().evaluation_metrics()
    assert 0 <= metrics["decision_accuracy"] <= 100
    assert 0 <= metrics["score_within_tolerance"] <= 100


def test_mean_difference_is_non_negative():
    metrics = HRInterviewSimulator().evaluation_metrics()
    assert metrics["mean_absolute_score_difference"] >= 0


def test_inconsistencies_are_identified():
    simulator = HRInterviewSimulator()
    issues = simulator.identify_inconsistencies()
    assert len(issues) >= 1


def test_recommendations_exist():
    recommendations = HRInterviewSimulator().recommendations()
    assert len(recommendations) >= 1


def test_report_can_be_generated():
    simulator = HRInterviewSimulator()
    report = {
        "simulation_results": simulator.run_all(),
        "manual_comparison": simulator.compare_manual_evaluation(),
        "accuracy_evaluation": simulator.evaluation_metrics(),
        "scoring_inconsistencies": simulator.identify_inconsistencies(),
        "improvement_recommendations": simulator.recommendations()
    }
    assert len(report["simulation_results"]) == 8
    assert "decision_accuracy" in report["accuracy_evaluation"]
