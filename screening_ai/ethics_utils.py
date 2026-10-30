import json
from pathlib import Path


DEFAULT_POLICY_PATH = (
    Path(__file__).resolve().parent.parent
    / "config"
    / "ethics_policy.json"
)


def load_ethics_policy(policy_path=DEFAULT_POLICY_PATH):
    """Load and validate the ZECPath ethics policy."""
    with open(policy_path, "r", encoding="utf-8-sig") as file:
        policy = json.load(file)

    required_sections = [
        "consent",
        "fairness",
        "explainability",
        "data_retention",
        "compliance",
    ]

    for section in required_sections:
        if not isinstance(policy.get(section), dict):
            raise ValueError(
                f"Ethics policy section '{section}' is missing or invalid."
            )

    return policy


def remove_demographic_fields(candidate, policy=None):
    """
    Return a copy of a candidate profile without configured
    demographic fields. The original profile remains unchanged.
    """
    if not isinstance(candidate, dict):
        raise ValueError("Candidate profile must be a dictionary.")

    policy = policy or load_ethics_policy()
    excluded = {
        field.casefold()
        for field in policy["fairness"].get("exclude_from_scoring", [])
        if isinstance(field, str)
    }

    def sanitize(value):
        if isinstance(value, dict):
            return {
                key: sanitize(item)
                for key, item in value.items()
                if not (
                    isinstance(key, str)
                    and key.casefold() in excluded
                )
            }

        if isinstance(value, list):
            return [sanitize(item) for item in value]

        return value

    return sanitize(candidate)


def validate_retention_policy(policy=None):
    """
    Confirm that retention has a positive, documented number of days.
    Does not delete data or establish legal compliance.
    """
    policy = policy or load_ethics_policy()
    retention = policy["data_retention"]
    days = retention.get("retention_days")

    if isinstance(days, bool) or not isinstance(days, int) or days <= 0:
        raise ValueError(
            "Set data_retention.retention_days to a positive integer "
            "after the retention period has been approved."
        )

    return days
