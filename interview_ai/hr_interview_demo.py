"""Integrated ZECPath HR Interview demo using the existing scoring engine.

Run from repository root:
    python -m interview_ai.hr_interview_demo
Optional dataset:
    python -m interview_ai.hr_interview_demo --dataset data/hr_interview_demo/hr_interview_demo.json
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from interview_ai.hr_interview_scoring_engine import HRInterviewScoringEngine
from interview_ai.hr_score_report import HRScoreReport

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATASET = REPO_ROOT / "data" / "hr_interview_demo" / "hr_interview_demo.json"
OUTPUT_DIR = REPO_ROOT / "data" / "hr_interview_demo" / "output"


def recommendation_for(score: float, thresholds: dict) -> tuple[str, str]:
    """Map a score to a non-binding decision-support label."""
    strong = float(thresholds["strong"])
    moderate = float(thresholds["moderate"])
    review = float(thresholds["review"])
    if not (0 <= review <= moderate <= strong <= 100):
        raise ValueError("Thresholds must satisfy 0 <= review <= moderate <= strong <= 100.")
    if score >= strong:
        return "recommend_for_human_review", "Strong score band; recruiter/manager review is still required."
    if score >= moderate:
        return "consider_for_human_review", "Moderate score band; review evidence and role requirements."
    if score >= review:
        return "additional_review_required", "Developing score range; inspect responses and scoring evidence."
    return "human_review_required", "Below configured review threshold; do not automatically reject."


def run_demo(dataset_path: Path = DEFAULT_DATASET) -> dict:
    data = json.loads(Path(dataset_path).read_text(encoding="utf-8"))
    candidate = data["candidate"]
    engine = HRInterviewScoringEngine()
    result = engine.score_interview(
        candidate_id=candidate["candidate_id"],
        job_id=candidate["job_id"],
        session_id=candidate["session_id"],
        job_title=candidate["job_title"],
        responses=data["evaluated_responses"],
    )
    report = HRScoreReport().to_dict(result)
    label, rationale = recommendation_for(
        result["final_hr_interview_score"], data["recommendation_thresholds"]
    )
    report["decision_support"] = {
        "recommendation": label,
        "rationale": rationale,
        "human_decision_required": True,
        "notice": "Synthetic demonstration only; not an automated hiring decision."
    }
    report["demo_metadata"] = {
        "dataset_name": data.get("dataset_name"),
        "dataset_version": data.get("dataset_version"),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "input_type": "pre_evaluated_component_scores"
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the ZECPath HR Interview scoring demo.")
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    args = parser.parse_args()
    report = run_demo(args.dataset)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = OUTPUT_DIR / "hr_interview_demo_report.json"
    text_path = OUTPUT_DIR / "hr_interview_demo_summary.txt"
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    lines = [
        "ZECPath AI — HR INTERVIEW DEMO",
        "=" * 40,
        f"Candidate: {report['candidate']['candidate_id']}",
        f"Job: {report['candidate']['job_title']} ({report['candidate']['job_id']})",
        f"Session: {report['candidate']['session_id']}",
        f"Responses evaluated: {report['interview_summary']['responses_evaluated']}",
        "", "SCORING BREAKDOWN", "-" * 40
    ]
    for name, values in report["explainable_breakdown"].items():
        lines.append(
            f"{name}: {values['score']:.2f} x {values['weight']:.0%} = {values['weighted_score']:.2f}"
        )
    lines.extend([
        "", f"Final HR interview score: {report['score']['final']:.2f}/100",
        f"Score band: {report['score']['band']}",
        f"Demo recommendation: {report['decision_support']['recommendation']}",
        f"Rationale: {report['decision_support']['rationale']}",
        "", "Human review is required.",
        "Synthetic sample data; component scores are pre-evaluated inputs, not inferred from transcript text."
    ])
    summary = "\n".join(lines)
    text_path.write_text(summary + "\n", encoding="utf-8")
    print(summary)
    print(f"\nJSON report saved: {json_path.relative_to(REPO_ROOT)}")
    print(f"Text summary saved: {text_path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
