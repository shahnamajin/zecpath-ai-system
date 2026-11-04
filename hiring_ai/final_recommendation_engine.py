import json
from pathlib import Path


class FinalRecommendationEngine:
    """
    Produces an explainable hiring recommendation from
    the unified Day 51 candidate score and risk observations.

    Recommendations are decision support, not final
    autonomous employment decisions.
    """

    VALID_CATEGORIES = {"behavior", "integrity"}
    VALID_SEVERITIES = {"low", "medium", "high"}
    VALID_STATUSES = {"observed", "unverified", "confirmed", "resolved"}

    def __init__(self, config_path="config/recommendation_policy.json"):
        path = Path(config_path)

        with path.open("r", encoding="utf-8") as file:
            self.policy = json.load(file)

    def _validate_score(self, score):
        if isinstance(score, bool) or not isinstance(score, (int, float)):
            raise ValueError("Hiring Fit Score must be numeric.")

        if not 0 <= score <= 100:
            raise ValueError("Hiring Fit Score must be between 0 and 100.")

    def _validate_risks(self, risk_factors):
        if not isinstance(risk_factors, list):
            raise ValueError("risk_factors must be a list.")

        for risk in risk_factors:
            if not isinstance(risk, dict):
                raise ValueError("Each risk factor must be an object.")

            if risk.get("category") not in self.VALID_CATEGORIES:
                raise ValueError("Invalid risk category.")

            if risk.get("severity") not in self.VALID_SEVERITIES:
                raise ValueError("Invalid risk severity.")

            if risk.get("status") not in self.VALID_STATUSES:
                raise ValueError("Invalid risk status.")

            if not risk.get("description"):
                raise ValueError("Risk description is required.")

    def _calculate_confidence(self, score, complete, risks):
        config = self.policy["confidence"]

        confidence = config["base_score"]

        if complete:
            confidence += config["complete_evaluation_bonus"]

            margin = min(abs(score - 60), abs(score - 80))
            confidence += min(
                margin,
                config["maximum_margin_bonus"]
            )

        integrity_concerns = [
            risk for risk in risks
            if risk["category"] == "integrity"
            and risk["status"] in {"observed", "unverified", "confirmed"}
            and risk["severity"] in {"medium", "high"}
        ]

        penalty = (
            len(integrity_concerns)
            * config["unresolved_integrity_penalty"]
        )

        penalty = min(
            penalty,
            config["maximum_integrity_penalty"]
        )

        confidence -= penalty

        return round(max(0, min(100, confidence)), 2)

    def recommend(self, candidate_score, risk_factors=None):
        if not isinstance(candidate_score, dict):
            raise ValueError("candidate_score must be a dictionary.")

        if risk_factors is None:
            risk_factors = []

        self._validate_risks(risk_factors)

        status = candidate_score.get("status")
        score = candidate_score.get("hiring_fit_percentage")
        missing_stages = candidate_score.get("missing_stages", [])

        complete = (
            status == "completed"
            and not missing_stages
            and score is not None
        )

        reasons = []
        review_reasons = []

        if not complete:
            recommendation = "hold_review"
            reasons.append("Candidate evaluation is incomplete.")
            review_reasons.append("Complete all required evaluation stages.")

            return {
                "recommendation": recommendation,
                "recommendation_label": "Hold / Review",
                "hiring_fit_score": score,
                "confidence_score": 40.0,
                "evaluation_status": status or "unknown",
                "missing_stages": missing_stages,
                "risk_factors": risk_factors,
                "reasons": reasons,
                "review_reasons": review_reasons,
                "requires_human_review": True,
                "decision_type": "AI recommendation"
            }

        self._validate_score(score)

        thresholds = self.policy["decision_thresholds"]

        if score >= thresholds["selected_min"]:
            recommendation = "selected"
            reasons.append(
                f"Hiring Fit Score {score:.2f} meets the selection threshold."
            )
        elif score >= thresholds["hold_min"]:
            recommendation = "hold_review"
            reasons.append(
                f"Hiring Fit Score {score:.2f} falls in the review range."
            )
        else:
            recommendation = "rejected"
            reasons.append(
                f"Hiring Fit Score {score:.2f} is below the minimum threshold."
            )

        for risk in risk_factors:
            category = risk["category"]
            severity = risk["severity"]
            risk_status = risk["status"]

            if category == "behavior":
                reasons.append(
                    "Behavioral observation recorded for contextual review; "
                    "it does not change the Hiring Fit Score."
                )
                review_reasons.append(
                    "Human review of the behavioral observation, if relevant."
                )

            elif category == "integrity":
                if risk_status in {"observed", "unverified", "confirmed"}:
                    if severity in {"medium", "high"}:
                        recommendation = "hold_review"
                        review_reasons.append(
                            "Integrity concern requires human investigation."
                        )
                        reasons.append(
                            "Unresolved integrity concern routes the candidate "
                            "to human review; it is not proof of misconduct."
                        )

                elif risk_status == "resolved":
                    reasons.append(
                        "Integrity observation is marked as resolved."
                    )

        confidence = self._calculate_confidence(
            score,
            complete,
            risk_factors
        )

        requires_review = (
            recommendation == "hold_review"
            or bool(review_reasons)
        )

        labels = {
            "selected": "Selected",
            "hold_review": "Hold / Review",
            "rejected": "Rejected"
        }

        return {
            "recommendation": recommendation,
            "recommendation_label": labels[recommendation],
            "hiring_fit_score": round(float(score), 2),
            "confidence_score": confidence,
            "evaluation_status": "completed",
            "missing_stages": [],
            "risk_factors": risk_factors,
            "reasons": reasons,
            "review_reasons": review_reasons,
            "requires_human_review": requires_review,
            "decision_type": "AI recommendation"
        }