
"""ZECPath AI - End-to-End HR Interview Simulation Engine."""

import json
from pathlib import Path


class HRInterviewSimulator:
    def __init__(self, sessions_path=None, config_path=None):
        base = Path(__file__).resolve().parent.parent
        sessions_path = sessions_path or base / "data/hr_simulation/simulation_sessions.json"
        config_path = config_path or base / "data/hr_simulation/evaluation_config.json"

        with open(sessions_path, encoding="utf-8") as f:
            self.sessions = json.load(f)["sessions"]

        with open(config_path, encoding="utf-8") as f:
            self.config = json.load(f)

    @staticmethod
    def _clamp(value):
        return round(max(0.0, min(100.0, float(value))), 2)

    def ai_decision(self, score):
        if score >= self.config["decision_thresholds"]["continue"]:
            return "continue"
        if score >= self.config["decision_thresholds"]["clarify"]:
            return "clarify"
        return "review"

    def simulate_session(self, session):
        score = self._clamp(session["hr_score"])
        return {
            "session_id": session["session_id"],
            "candidate_id": session["candidate_id"],
            "candidate_type": session["candidate_type"],
            "ai_score": score,
            "ai_decision": self.ai_decision(score),
            "communication": self._clamp(session["communication"]),
            "confidence": self._clamp(session["confidence"]),
            "consistency": self._clamp(session["consistency"]),
            "aptitude_logic": self._clamp(session["aptitude_logic"]),
            "response_count": len(session.get("responses", []))
        }

    def run_all(self):
        return [self.simulate_session(session) for session in self.sessions]

    def compare_manual_evaluation(self):
        comparisons = []

        for session in self.sessions:
            ai = self.simulate_session(session)
            score_difference = round(ai["ai_score"] - session["manual_score"], 2)
            within_tolerance = abs(score_difference) <= self.config["tolerance_for_score_difference"]

            comparisons.append({
                **ai,
                "manual_score": self._clamp(session["manual_score"]),
                "manual_decision": session["manual_decision"],
                "score_difference": score_difference,
                "within_score_tolerance": within_tolerance,
                "decision_agreement": ai["ai_decision"] == session["manual_decision"]
            })

        return comparisons

    def evaluation_metrics(self):
        comparisons = self.compare_manual_evaluation()

        if not comparisons:
            return {
                "session_count": 0,
                "decision_accuracy": 0.0,
                "score_within_tolerance": 0.0,
                "mean_absolute_score_difference": 0.0,
                "decision_disagreements": 0
            }

        decision_accuracy = (
            sum(x["decision_agreement"] for x in comparisons)
            / len(comparisons)
            * 100
        )

        score_tolerance_rate = (
            sum(x["within_score_tolerance"] for x in comparisons)
            / len(comparisons)
            * 100
        )

        mean_absolute_difference = sum(
            abs(x["score_difference"]) for x in comparisons
        ) / len(comparisons)

        return {
            "session_count": len(comparisons),
            "decision_accuracy": round(decision_accuracy, 2),
            "score_within_tolerance": round(score_tolerance_rate, 2),
            "mean_absolute_score_difference": round(mean_absolute_difference, 2),
            "decision_disagreements": sum(
                not x["decision_agreement"] for x in comparisons
            )
        }

    def identify_inconsistencies(self):
        issues = []

        for item in self.compare_manual_evaluation():
            if not item["decision_agreement"]:
                issues.append({
                    "session_id": item["session_id"],
                    "candidate_type": item["candidate_type"],
                    "issue": "AI and manual decision differ",
                    "ai_decision": item["ai_decision"],
                    "manual_decision": item["manual_decision"],
                    "score_difference": item["score_difference"]
                })

            if not item["within_score_tolerance"]:
                issues.append({
                    "session_id": item["session_id"],
                    "candidate_type": item["candidate_type"],
                    "issue": "AI and manual scores exceed configured tolerance",
                    "ai_score": item["ai_score"],
                    "manual_score": item["manual_score"],
                    "score_difference": item["score_difference"]
                })

        return issues

    def recommendations(self):
        metrics = self.evaluation_metrics()
        issues = self.identify_inconsistencies()
        recommendations = []

        if metrics["decision_disagreements"]:
            recommendations.append(
                "Review decision thresholds and add candidate-type context before final decisions."
            )

        if metrics["mean_absolute_score_difference"] > 5:
            recommendations.append(
                "Calibrate component weights against additional human-reviewed interview samples."
            )

        if any(x["candidate_type"] == "overqualified" for x in issues):
            recommendations.append(
                "Add a role-alignment and overqualification review signal rather than relying only on score."
            )

        if any(x["candidate_type"] == "hesitant" for x in issues):
            recommendations.append(
                "Separate hesitation/communication signals from overall suitability and allow clarification."
            )

        if not recommendations:
            recommendations.append(
                "Continue validation with a larger and more diverse manually reviewed dataset."
            )

        return recommendations
