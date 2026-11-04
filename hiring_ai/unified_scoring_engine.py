import json
import math
from pathlib import Path


class UnifiedScoringEngine:
    """Aggregate five recruitment evaluation rounds."""

    REQUIRED_COMPONENTS = {
        "ats",
        "screening",
        "hr_interview",
        "technical_interview",
        "machine_test",
    }

    def __init__(self, config_dir="data/unified_scoring"):
        config_dir = Path(config_dir)

        weights_path = config_dir / "scoring_weights.json"
        roles_path = config_dir / "role_weights.json"

        if not weights_path.exists():
            raise FileNotFoundError(weights_path)

        if not roles_path.exists():
            raise FileNotFoundError(roles_path)

        with weights_path.open(encoding="utf-8") as file:
            self.config = json.load(file)

        with roles_path.open(encoding="utf-8") as file:
            self.role_config = json.load(file)

        if "default_weights" not in self.config:
            raise ValueError("default_weights configuration is required.")

        self._validate_weights(self.config["default_weights"])

        for role, weights in self.role_config.get("roles", {}).items():
            try:
                self._validate_weights(weights)
            except ValueError as exc:
                raise ValueError(
                    f"Invalid weights for role '{role}': {exc}"
                ) from exc

    @staticmethod
    def validate_score(score, name):
        """Validate a score in the range 0–100."""

        if isinstance(score, bool) or not isinstance(score, (int, float)):
            raise ValueError(f"{name} must be numeric.")

        if not math.isfinite(score) or not 0 <= score <= 100:
            raise ValueError(f"{name} must be between 0 and 100.")

        return float(score)

    @classmethod
    def _validate_weights(cls, weights):
        if not isinstance(weights, dict):
            raise ValueError("Weights must be a dictionary.")

        if set(weights) != cls.REQUIRED_COMPONENTS:
            raise ValueError(
                "Weights must contain exactly all five evaluation stages."
            )

        for name, weight in weights.items():
            if (
                isinstance(weight, bool)
                or not isinstance(weight, (int, float))
                or not math.isfinite(weight)
                or weight < 0
            ):
                raise ValueError(
                    f"Weight '{name}' must be finite and non-negative."
                )

        if not math.isclose(
            sum(weights.values()), 1.0, rel_tol=0.0, abs_tol=1e-9
        ):
            raise ValueError("All scoring weights must total 1.0.")

    def get_weights(self, role_type="default"):
        if not isinstance(role_type, str) or not role_type.strip():
            raise ValueError("role_type must be a non-empty string.")

        role = role_type.strip().lower()

        weights = (
            self.config["default_weights"]
            if role == "default"
            else self.role_config.get("roles", {}).get(
                role, self.config["default_weights"]
            )
        )

        self._validate_weights(weights)
        return dict(weights)

    def calculate(self, scores, role_type="default"):
        """
        Calculate a transparent cross-round score.

        Missing scores produce an incomplete result.
        They are never silently treated as zero.
        """

        if not isinstance(scores, dict):
            raise ValueError("scores must be a dictionary.")

        unknown = set(scores) - self.REQUIRED_COMPONENTS
        if unknown:
            raise ValueError(f"Unknown evaluation stages: {sorted(unknown)}")

        normalized_scores = {}

        for component, score in scores.items():
            if score is not None:
                normalized_scores[component] = self.validate_score(
                    score, component
                )

        weights = self.get_weights(role_type)

        missing = sorted(self.REQUIRED_COMPONENTS - set(normalized_scores))

        if missing:
            return {
                "scores": normalized_scores,
                "weights": weights,
                "weighted_contributions": {},
                "hiring_fit_percentage": None,
                "role_type": role_type.strip().lower(),
                "missing_stages": missing,
                "completed_stages": sorted(normalized_scores),
                "completion_percentage": round(
                    len(normalized_scores) / len(self.REQUIRED_COMPONENTS) * 100,
                    2,
                ),
                "status": "incomplete",
            }

        contributions = {
            component: normalized_scores[component] * weights[component]
            for component in self.REQUIRED_COMPONENTS
        }

        hiring_fit = round(sum(contributions.values()), 2)

        return {
            "scores": normalized_scores,
            "weights": weights,
            "weighted_contributions": {
                key: round(value, 2)
                for key, value in contributions.items()
            },
            "hiring_fit_percentage": hiring_fit,
            "role_type": role_type.strip().lower(),
            "missing_stages": [],
            "completed_stages": sorted(normalized_scores),
            "completion_percentage": 100.0,
            "status": "completed",
        }