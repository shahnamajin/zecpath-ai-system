
from interview_ai.aptitude_logic_engine import AptitudeLogicEngine
from interview_ai.logical_reasoning_scorer import LogicalReasoningScorer
from interview_ai.scenario_evaluator import ScenarioEvaluator


def test_reasoning_questions_load():
    data = AptitudeLogicEngine().load_reasoning_questions()
    assert len(data["questions"]) == 3


def test_scenarios_load():
    data = AptitudeLogicEngine().load_scenarios()
    assert len(data["scenarios"]) == 2


def test_reasoning_score_range():
    result = LogicalReasoningScorer().score(
        "First I identify the problem, then I compare the evidence and test the solution."
    )
    assert 0 <= result["final_score"] <= 100


def test_reasoning_breakdown_exists():
    result = LogicalReasoningScorer().score(
        "I would assess the impact, prioritize the issue, and verify the result."
    )
    assert "breakdown" in result
    assert len(result["breakdown"]) == 5


def test_reasoning_weights_sum_to_one():
    scorer = LogicalReasoningScorer()
    assert abs(sum(scorer.weights.values()) - 1.0) < 0.0001


def test_scenario_score_range():
    engine = AptitudeLogicEngine()
    scenario = engine.load_scenarios()["scenarios"][0]
    result = engine.evaluate_scenario(
        "I would understand both sides, compare evidence, prioritize the project need, "
        "communicate the decision, and follow up.",
        scenario
    )
    assert 0 <= result["final_score"] <= 100


def test_scenario_breakdown_exists():
    engine = AptitudeLogicEngine()
    scenario = engine.load_scenarios()["scenarios"][0]
    result = engine.evaluate_scenario("I would assess the problem and make a plan.", scenario)
    assert "breakdown" in result
    assert len(result["breakdown"]) == 5


def test_overall_score():
    engine = AptitudeLogicEngine()
    reasoning = engine.evaluate_reasoning("I would first identify the issue and then test the solution.")
    scenario = engine.load_scenarios()["scenarios"][0]
    situational = engine.evaluate_scenario(
        "I would assess the impact, compare options, choose an approach, and verify the result.",
        scenario
    )
    overall = engine.get_overall_score([reasoning], [situational])
    assert 0 <= overall <= 100


def test_short_response_has_lower_clarity_baseline():
    scorer = LogicalReasoningScorer()
    short = scorer.score("Yes.")
    detailed = scorer.score(
        "First I would identify the problem, assess the impact, compare possible solutions, "
        "test the selected approach, and verify the outcome."
    )
    assert detailed["components"]["clarity"] >= short["components"]["clarity"]


def test_empty_answer_safe():
    scorer = LogicalReasoningScorer()
    result = scorer.score("")
    assert 0 <= result["final_score"] <= 100
