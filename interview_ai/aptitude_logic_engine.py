
"""ZECPath AI - Aptitude and Logic Evaluation Engine."""

import json
from pathlib import Path

from interview_ai.logical_reasoning_scorer import LogicalReasoningScorer
from interview_ai.scenario_evaluator import ScenarioEvaluator


class AptitudeLogicEngine:
    def __init__(self):
        self.reasoning_scorer = LogicalReasoningScorer()
        self.scenario_evaluator = ScenarioEvaluator()

    def load_reasoning_questions(self):
        path = (
            Path(__file__).resolve().parent.parent
            / "data" / "aptitude_logic" / "reasoning_questions.json"
        )
        with open(path, encoding="utf-8") as file:
            return json.load(file)

    def load_scenarios(self):
        path = (
            Path(__file__).resolve().parent.parent
            / "data" / "aptitude_logic" / "situational_scenarios.json"
        )
        with open(path, encoding="utf-8") as file:
            return json.load(file)

    def evaluate_reasoning(self, answer, signals=None):
        return self.reasoning_scorer.score(answer, signals)

    def evaluate_scenario(self, answer, scenario):
        return self.scenario_evaluator.evaluate(answer, scenario)

    def get_overall_score(self, reasoning_results, scenario_results):
        scores = []

        if reasoning_results:
            scores.extend(result["final_score"] for result in reasoning_results)

        if scenario_results:
            scores.extend(result["final_score"] for result in scenario_results)

        if not scores:
            return 0.0

        return round(sum(scores) / len(scores), 2)
