
import json
import math
from pathlib import Path


class UnifiedScoringEngine:
    """
    Combines ATS, AI screening, and HR interview scores
    into a unified hiring-fit percentage.
    """

    REQUIRED_COMPONENTS = {
        "ats",
        "screening",
        "hr_interview",
    }

    def __init__(self, config_dir="data/unified_scoring"):
        config_dir = Path(config_dir)

        weights_path = config_dir / "scoring_weights.json"
        roles_path = config_dir / "role_weights.json"

        if not weights_path.exists():
            raise FileNotFoundError(
                f"Scoring weights configuration not found: {weights_path}"
            )

        if not roles_path.exists():
            raise FileNotFoundError(
                f"Role weights configuration not found: {roles_path}"
            )

        with weights_path.open("r", encoding="utf-8") as file:
            self.config = json.load(file)

        with roles_path.open("r", encoding="utf-8") as file:
            self.role_config = json.load(file)

        if "default_weights" not in self.config:
            raise ValueError(
                "scoring_weights.json must define default_weights."
            )

        # Validate the default configuration during initialization.
        self._validate_weights(self.config["default_weights"])

        # Validate configured role weights as well.
        roles = self.role_config.get("roles", {})

        for role_name, weights in roles.items():
            try:
                self._validate_weights(weights)
            except ValueError as exc:
                raise ValueError(
                    f"Invalid weights for role '{role_name}': {exc}"
                ) from exc

    @staticmethod
    def validate_score(score, name):
        """Validate that a score is numeric and within 0–100."""

        if isinstance(score, bool) or not isinstance(score, (int, float)):
            raise ValueError(f"{name} must be a numeric value.")

        if not math.isfinite(score):
            raise ValueError(f"{name} must be finite.")

        if not 0 <= score <= 100:
            raise ValueError(f"{name} must be between 0 and 100.")

        return float(score)

    @classmethod
    def _validate_weights(cls, weights):
        """Validate weight keys, values, and total."""

        if not isinstance(weights, dict):
            raise ValueError("Weights must be a dictionary.")

        if set(weights) != cls.REQUIRED_COMPONENTS:
            raise ValueError(
                "Weights must contain exactly: "
                "ats, screening, and hr_interview."
            )

        for name, weight in weights.items():
            if (
                isinstance(weight, bool)
                or not isinstance(weight, (int, float))
                or not math.isfinite(weight)
                or weight < 0
            ):
                raise ValueError(
                    f"Weight '{name}' must be a finite, "
                    "non-negative number."
                )

        if not math.isclose(
            sum(weights.values()),
            1.0,
            rel_tol=0.0,
            abs_tol=1e-9,
        ):
            raise ValueError("Scoring weights must total 1.0.")

    def get_weights(self, role_type="default"):
        """
        Return the correct weights for a role.

        The default role uses scoring_weights.json.
        Other roles use role_weights.json when configured.
        Unknown roles fall back to the default weights.
        """

        if not isinstance(role_type, str) or not role_type.strip():
            raise ValueError("role_type must be a non-empty string.")

        normalized_role = role_type.strip().lower()

        if normalized_role == "default":
            weights = self.config["default_weights"]
        else:
            roles = self.role_config.get("roles", {})
            weights = roles.get(
                normalized_role,
                self.config["default_weights"],
            )

        self._validate_weights(weights)

        return dict(weights)

    def calculate(
        self,
        ats_score,
        screening_score,
        hr_interview_score,
        role_type="default",
    ):
        """
        Calculate the weighted hiring-fit percentage.

        Returns individual scores, weights, weighted contributions,
        the final hiring-fit percentage, and the role type.
        """

        scores = {
            "ats": self.validate_score(ats_score, "ATS score"),
            "screening": self.validate_score(
                screening_score, "Screening score"
            ),
            "hr_interview": self.validate_score(
                hr_interview_score, "HR interview score"
            ),
        }

        weights = self.get_weights(role_type)

        # Calculate each component's contribution without
        # rounding intermediate values.
        contributions = {
            name: scores[name] * weights[name]
            for name in self.REQUIRED_COMPONENTS
        }

        # Round only the final aggregate.
        hiring_fit = round(sum(contributions.values()), 2)

        return {
            "scores": scores,
            "weights": weights,
            "weighted_contributions": {
                name: round(value, 2)
                for name, value in contributions.items()
            },
            "hiring_fit_percentage": hiring_fit,
            "role_type": role_type.strip().lower(),
            "status": "completed",
        }
